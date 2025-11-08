"""Deterministic workflow executor subgraph.

Executes predefined workflows step-by-step with conditional routing.
LLM evaluates step results and decides whether to continue.
Supports HITL approval gates for critical operations.
"""

import logging
from typing import Literal

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, START, END
from langgraph.types import interrupt

from src.core.state_schemas import DeterministicWorkflowState
from src.core.config import get_settings
from src.tools import ALL_TOOLS

logger = logging.getLogger(__name__)


def load_workflow(state: DeterministicWorkflowState) -> DeterministicWorkflowState:
    """Load and initialize workflow steps.

    Args:
        state: Current workflow state

    Returns:
        Updated state with initialized steps
    """
    workflow_name = state["workflow_name"]
    logger.info(f"Loading workflow: {workflow_name}")

    # Workflows will be defined separately and passed in workflow_params
    steps = state.get("steps", [])

    if not steps:
        return {
            **state,
            "message": f"❌ Error: No steps defined for workflow '{workflow_name}'",
        }

    return {
        **state,
        "current_step": 0,
        "step_outputs": [],
    }


def execute_step(state: DeterministicWorkflowState) -> DeterministicWorkflowState:
    """Execute current workflow step.

    Args:
        state: Current workflow state

    Returns:
        Updated state with step execution result
    """
    current_step_idx = state["current_step"]
    steps = state["steps"]

    if current_step_idx >= len(steps):
        return {**state, "message": "✅ All steps completed"}

    step = steps[current_step_idx]
    step_name = step.get("name", f"Step {current_step_idx + 1}")
    step_type = step.get("type")  # 'tool_call', 'approval', 'conditional'

    logger.info(f"Executing step {current_step_idx + 1}/{len(steps)}: {step_name}")

    try:
        if step_type == "tool_call":
            # Execute tool with parameters
            tool_name = step["tool"]
            tool_params = step.get("params", {})

            # Apply workflow params as template variables
            for key, value in tool_params.items():
                if isinstance(value, str) and value.startswith("{{") and value.endswith("}}"):
                    # Template variable from workflow_params
                    var_name = value[2:-2].strip()
                    if var_name in state["workflow_params"]:
                        tool_params[key] = state["workflow_params"][var_name]

            # Find and execute tool
            tool = next((t for t in ALL_TOOLS if t.name == tool_name), None)
            if not tool:
                return {
                    **state,
                    "step_outputs": state["step_outputs"]
                    + [
                        {
                            "step": step_name,
                            "status": "error",
                            "error": f"Tool '{tool_name}' not found",
                        }
                    ],
                }

            # Execute tool
            result = tool.invoke(tool_params)

            # Add to step outputs
            output = {
                "step": step_name,
                "status": "success" if "✅" in result else "error",
                "result": result,
                "tool": tool_name,
                "params": tool_params,
            }

            return {
                **state,
                "step_outputs": state["step_outputs"] + [output],
            }

        elif step_type == "approval":
            # Request human approval
            message = step.get("message", "Approval required to continue")
            logger.info(f"Requesting approval: {message}")

            # Use LangGraph interrupt for HITL
            approval = interrupt(
                {
                    "type": "approval",
                    "message": message,
                    "step": step_name,
                }
            )

            output = {
                "step": step_name,
                "status": "approved" if approval else "rejected",
                "result": f"User {'approved' if approval else 'rejected'} continuation",
            }

            return {
                **state,
                "step_outputs": state["step_outputs"] + [output],
            }

        else:
            # Unknown step type
            return {
                **state,
                "step_outputs": state["step_outputs"]
                + [
                    {
                        "step": step_name,
                        "status": "error",
                        "error": f"Unknown step type: {step_type}",
                    }
                ],
            }

    except Exception as e:
        logger.error(f"Error executing step: {e}")
        return {
            **state,
            "step_outputs": state["step_outputs"]
            + [
                {
                    "step": step_name,
                    "status": "error",
                    "error": str(e),
                }
            ],
        }


def evaluate_step(state: DeterministicWorkflowState) -> DeterministicWorkflowState:
    """Use LLM to evaluate step result and decide next action.

    Args:
        state: Current workflow state

    Returns:
        Updated state with evaluation decision
    """
    settings = get_settings()
    llm = ChatAnthropic(
        model="claude-3-5-sonnet-20241022",
        temperature=0,
        api_key=settings.anthropic_api_key,
    )

    # Get last step output
    if not state["step_outputs"]:
        return {**state, "overall_result": {"decision": "error", "reason": "No step outputs"}}

    last_output = state["step_outputs"][-1]
    current_step = state["steps"][state["current_step"]]

    # Create evaluation prompt
    system_prompt = """You are evaluating the result of a workflow step execution.

Your task is to determine:
1. Did the step succeed?
2. Should the workflow continue to the next step?
3. If there was an error, is it recoverable?

Respond with a JSON object:
{
  "decision": "continue" | "stop" | "retry",
  "reason": "Brief explanation",
  "success": true | false
}

Guidelines:
- "continue": Step succeeded, move to next step
- "stop": Critical error, abort workflow
- "retry": Transient error, could retry (not yet implemented)
"""

    user_prompt = f"""Evaluate this workflow step execution:

Step: {current_step.get('name')}
Type: {current_step.get('type')}
Tool: {current_step.get('tool', 'N/A')}

Result:
{last_output.get('result', 'No result')}

Status: {last_output.get('status')}
Error: {last_output.get('error', 'None')}

Should we continue to the next step?"""

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt),
    ]

    try:
        response = llm.invoke(messages)
        content = response.content

        # Parse JSON response
        import json

        # Extract JSON from markdown code blocks if present
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()

        evaluation = json.loads(content)

        logger.info(f"Step evaluation: {evaluation['decision']} - {evaluation['reason']}")

        return {
            **state,
            "overall_result": evaluation,
        }

    except Exception as e:
        logger.error(f"Error evaluating step: {e}")
        return {
            **state,
            "overall_result": {
                "decision": "stop",
                "reason": f"Evaluation failed: {e}",
                "success": False,
            },
        }


def route_after_evaluation(
    state: DeterministicWorkflowState,
) -> Literal["increment_step", "format_result"]:
    """Route based on LLM evaluation decision.

    Args:
        state: Current workflow state

    Returns:
        Next node name
    """
    if not state.get("overall_result"):
        return "format_result"

    decision = state["overall_result"].get("decision", "stop")

    if decision == "continue":
        # Check if there are more steps
        if state["current_step"] + 1 < len(state["steps"]):
            return "increment_step"
        else:
            return "format_result"
    else:
        # Stop or error
        return "format_result"


def increment_step(state: DeterministicWorkflowState) -> DeterministicWorkflowState:
    """Increment to next workflow step.

    Args:
        state: Current workflow state

    Returns:
        Updated state with incremented step counter
    """
    return {
        **state,
        "current_step": state["current_step"] + 1,
    }


def format_result(state: DeterministicWorkflowState) -> DeterministicWorkflowState:
    """Format final workflow result.

    Args:
        state: Current workflow state

    Returns:
        Updated state with formatted message
    """
    total_steps = len(state["steps"])
    completed_steps = len(state["step_outputs"])
    successful_steps = sum(
        1 for output in state["step_outputs"] if output.get("status") == "success"
    )
    failed_steps = sum(1 for output in state["step_outputs"] if output.get("status") == "error")

    # Build result message
    message_parts = [
        f"📊 Workflow '{state['workflow_name']}' Execution Summary",
        f"",
        f"Steps: {completed_steps}/{total_steps}",
        f"✅ Successful: {successful_steps}",
        f"❌ Failed: {failed_steps}",
        f"",
        "Step Details:",
    ]

    for i, output in enumerate(state["step_outputs"], 1):
        status_icon = "✅" if output.get("status") == "success" else "❌"
        message_parts.append(f"  {i}. {status_icon} {output.get('step')}")
        if output.get("status") == "error":
            message_parts.append(f"     Error: {output.get('error')}")

    # Overall result
    if state.get("overall_result"):
        result = state["overall_result"]
        message_parts.extend(
            [
                "",
                f"Final Decision: {result.get('decision')}",
                f"Reason: {result.get('reason')}",
            ]
        )

    message = "\n".join(message_parts)

    return {**state, "message": message}


def create_deterministic_workflow_subgraph() -> StateGraph:
    """Create deterministic workflow executor subgraph.

    Returns:
        Compiled StateGraph for deterministic workflow execution
    """
    workflow = StateGraph(DeterministicWorkflowState)

    # Add nodes
    workflow.add_node("load_workflow", load_workflow)
    workflow.add_node("execute_step", execute_step)
    workflow.add_node("evaluate_step", evaluate_step)
    workflow.add_node("increment_step", increment_step)
    workflow.add_node("format_result", format_result)

    # Add edges
    workflow.add_edge(START, "load_workflow")
    workflow.add_edge("load_workflow", "execute_step")
    workflow.add_edge("execute_step", "evaluate_step")

    # Conditional routing after evaluation
    workflow.add_conditional_edges(
        "evaluate_step",
        route_after_evaluation,
        {
            "increment_step": "increment_step",
            "format_result": "format_result",
        },
    )

    # After incrementing, execute next step
    workflow.add_edge("increment_step", "execute_step")

    # End after formatting
    workflow.add_edge("format_result", END)

    return workflow.compile()
