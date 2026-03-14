"""Deterministic mode graph - Step-by-step workflow execution.

Executes predefined workflows with LLM-based conditional routing.
More predictable than autonomous mode, similar to Ansible playbooks.
"""

import logging
import uuid
from typing import Literal

from langgraph.graph import END, START, StateGraph
from src.core.checkpoint_manager import get_checkpointer
from src.core.state_schemas import DeterministicState
from src.core.subgraphs.deterministic import create_deterministic_workflow_subgraph

logger = logging.getLogger(__name__)

# Import workflow definitions (will create this module next)
try:
    from src.workflows.definitions import WORKFLOWS
except ImportError:
    logger.warning("Workflow definitions not found, using empty dict")
    WORKFLOWS = {}


def load_workflow_definition(state: DeterministicState) -> DeterministicState:
    """Load workflow definition from user message.

    Extracts workflow name from last message and loads definition.

    Args:
        state: Current deterministic state

    Returns:
        Updated state with workflow steps loaded
    """
    # Extract workflow name from last message
    last_message = state["messages"][-1]
    user_input = last_message.content

    # Try to extract workflow name (format: "run workflow: <name>")
    workflow_name = None
    if "workflow:" in user_input.lower():
        workflow_name = user_input.lower().split("workflow:")[1].strip()
    else:
        # Assume entire message is workflow name
        workflow_name = user_input.strip()

    logger.info(f"Loading workflow: {workflow_name}")

    # Look up workflow definition
    if workflow_name not in WORKFLOWS:
        available = ", ".join(WORKFLOWS.keys()) if WORKFLOWS else "None"
        return {
            **state,
            "workflow_steps": [],
            "current_step_index": 0,
            "step_results": [],
            "continue_workflow": False,
            "workflow_complete": True,
            "error_occurred": True,
            "messages": state["messages"]
            + [
                {
                    "role": "assistant",
                    "content": f"❌ Error: Workflow '{workflow_name}' not found.\n\nAvailable workflows: {available}",
                }
            ],
        }

    workflow_def = WORKFLOWS[workflow_name]

    return {
        **state,
        "workflow_steps": workflow_def["steps"],
        "current_step_index": 0,
        "step_results": [],
        "continue_workflow": True,
        "workflow_complete": False,
        "error_occurred": False,
    }


def execute_workflow(state: DeterministicState) -> DeterministicState:
    """Execute workflow using deterministic workflow subgraph.

    Args:
        state: Current deterministic state

    Returns:
        Updated state with workflow execution results
    """
    if state.get("error_occurred"):
        return state  # Skip if error during load

    # Create workflow subgraph
    workflow_subgraph = create_deterministic_workflow_subgraph()

    # Extract workflow name (from loading step)
    last_message = state["messages"][-1]
    user_input = last_message.content
    workflow_name = (
        user_input.lower().split("workflow:")[-1].strip()
        if "workflow:" in user_input.lower()
        else user_input.strip()
    )

    # Invoke workflow subgraph
    try:
        result = workflow_subgraph.invoke(
            {
                "workflow_name": workflow_name,
                "workflow_params": {},  # Could extract from user message
                "steps": state["workflow_steps"],
                "current_step": 0,
                "step_outputs": [],
                "overall_result": None,
                "message": "",
            },
            config={"configurable": {"thread_id": str(uuid.uuid4())}},
        )

        # Update state with results
        return {
            **state,
            "step_results": result.get("step_outputs", []),
            "workflow_complete": True,
            "messages": state["messages"] + [{"role": "assistant", "content": result["message"]}],
        }

    except Exception as e:
        logger.error(f"Workflow execution failed: {e}")
        return {
            **state,
            "error_occurred": True,
            "workflow_complete": True,
            "messages": state["messages"]
            + [{"role": "assistant", "content": f"❌ Workflow execution failed: {e}"}],
        }


def route_after_load(state: DeterministicState) -> Literal["execute_workflow", "END"]:
    """Route based on whether workflow loaded successfully.

    Args:
        state: Current deterministic state

    Returns:
        Next node name
    """
    if state.get("error_occurred"):
        return END
    return "execute_workflow"


def create_deterministic_graph() -> StateGraph:
    """Create deterministic workflow execution graph.

    Returns:
        Compiled StateGraph with checkpointer for deterministic mode
    """
    workflow = StateGraph(DeterministicState)

    # Add nodes
    workflow.add_node("load_workflow_definition", load_workflow_definition)
    workflow.add_node("execute_workflow", execute_workflow)

    # Add edges
    workflow.add_edge(START, "load_workflow_definition")

    # Conditional routing after load
    workflow.add_conditional_edges(
        "load_workflow_definition",
        route_after_load,
        {
            "execute_workflow": "execute_workflow",
            END: END,
        },
    )

    # End after execution
    workflow.add_edge("execute_workflow", END)

    # Compile with persistent SQLite checkpointer
    checkpointer = get_checkpointer()
    return workflow.compile(checkpointer=checkpointer)
