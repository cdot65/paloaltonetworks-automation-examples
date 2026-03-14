"""Autonomous mode graph - ReAct agent for PAN-OS automation.

ReAct pattern: agent → tools → agent loop with full tool access.
Natural language interface for exploratory PAN-OS automation.
"""

import logging
from typing import Literal

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import SystemMessage
from langchain_core.messages.base import BaseMessage
from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode
from src.core.checkpoint_manager import get_checkpointer
from src.core.config import get_settings
from src.core.retry_policies import PANOS_RETRY_POLICY
from src.core.state_schemas import AutonomousState
from src.tools import ALL_TOOLS

logger = logging.getLogger(__name__)

# System prompt for autonomous agent
AUTONOMOUS_SYSTEM_PROMPT = """You are an AI assistant specialized in automating Palo Alto Networks PAN-OS firewalls.

You have access to tools for managing:
- Address objects and groups
- Service objects and groups
- Security policies
- NAT policies

**Your capabilities:**
- Create, read, update, delete, and list PAN-OS objects
- Answer questions about firewall configuration
- Provide recommendations for security best practices
- Execute complex multi-step automation workflows

**Important guidelines:**
- Always verify object existence before creating to avoid errors
- Use descriptive names for objects (e.g., "web-server-10.1.1.100" not "obj1")
- Tag objects appropriately for organization
- Provide clear explanations of what you're doing
- Ask for clarification if requirements are ambiguous
- NEVER delete objects without user confirmation

**Error handling:**
- If an operation fails, explain why and suggest alternatives
- Check dependencies before deleting objects (e.g., address groups reference addresses)

**Response format:**
- Be concise but informative
- Use bullet points for lists
- Provide examples when helpful
- Always confirm successful operations

You are in **autonomous mode** - you have full tool access and can make decisions independently.
Use your judgment to complete tasks efficiently while following security best practices.
"""


def call_agent(state: AutonomousState) -> AutonomousState:
    """Call LLM agent with tools.

    Args:
        state: Current autonomous state

    Returns:
        Updated state with agent response
    """
    settings = get_settings()

    # Initialize LLM with tools
    llm = ChatAnthropic(
        model="claude-haiku-4-5",
        temperature=0,
        api_key=settings.anthropic_api_key,
    )
    llm_with_tools = llm.bind_tools(ALL_TOOLS)

    # Prepend system message
    messages = [SystemMessage(content=AUTONOMOUS_SYSTEM_PROMPT)] + list[BaseMessage](
        state["messages"]
    )

    # Get response
    response = llm_with_tools.invoke(messages)

    return {"messages": [response]}


def route_after_agent(
    state: AutonomousState,
) -> Literal["tools", "END"]:
    """Route based on whether agent called tools.

    Args:
        state: Current autonomous state

    Returns:
        Next node name
    """
    last_message = state["messages"][-1]

    # Check if agent made tool calls
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        logger.info(f"Agent called {len(last_message.tool_calls)} tools")
        return "tools"

    # Agent finished - no more tool calls
    logger.info("Agent finished (no tool calls)")
    return END


def create_autonomous_graph() -> StateGraph:
    """Create autonomous ReAct agent graph.

    Returns:
        Compiled StateGraph with checkpointer for autonomous mode
    """
    workflow = StateGraph(AutonomousState)

    # Create tool node
    tool_node = ToolNode(ALL_TOOLS)

    # Add nodes
    workflow.add_node("agent", call_agent)
    workflow.add_node("tools", tool_node, retry=PANOS_RETRY_POLICY)

    # Add edges
    workflow.add_edge(START, "agent")

    # Conditional routing after agent
    workflow.add_conditional_edges(
        "agent",
        route_after_agent,
        {
            "tools": "tools",
            END: END,
        },
    )

    # After tools, always return to agent
    workflow.add_edge("tools", "agent")

    # Compile with persistent SQLite checkpointer for conversation memory
    checkpointer = get_checkpointer()
    return workflow.compile(checkpointer=checkpointer)
