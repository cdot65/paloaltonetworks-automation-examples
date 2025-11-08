"""Unit tests for autonomous graph nodes."""

import pytest
from langchain_core.messages import AIMessage, HumanMessage
from unittest.mock import Mock, patch
from langgraph.graph import END

from src.autonomous_graph import call_agent, route_after_agent
from src.core.state_schemas import AutonomousState


class TestCallAgent:
    """Tests for call_agent node."""

    @patch("src.autonomous_graph.ChatAnthropic")
    @patch("src.autonomous_graph.get_settings")
    def test_call_agent_returns_response(self, mock_settings, mock_chat_anthropic):
        """Test that call_agent returns AIMessage response."""
        # Setup mocks
        mock_settings.return_value.anthropic_api_key = "test-key"
        mock_llm = Mock()
        mock_response = AIMessage(content="I'll list the address objects for you.")
        mock_llm.invoke.return_value = mock_response
        mock_chat_anthropic.return_value.bind_tools.return_value = mock_llm

        # Create state
        state: AutonomousState = {"messages": [HumanMessage(content="List address objects")]}

        # Call function
        result = call_agent(state)

        # Assertions
        assert "messages" in result
        assert len(result["messages"]) == 1
        assert isinstance(result["messages"][0], AIMessage)
        assert result["messages"][0].content == "I'll list the address objects for you."

    @patch("src.autonomous_graph.ChatAnthropic")
    @patch("src.autonomous_graph.get_settings")
    def test_call_agent_with_tool_call(self, mock_settings, mock_chat_anthropic):
        """Test that call_agent handles tool calls."""
        # Setup mocks
        mock_settings.return_value.anthropic_api_key = "test-key"
        mock_llm = Mock()
        mock_response = AIMessage(
            content="",
            tool_calls=[{"name": "address_list", "args": {}, "id": "call_123"}],
        )
        mock_llm.invoke.return_value = mock_response
        mock_chat_anthropic.return_value.bind_tools.return_value = mock_llm

        # Create state
        state: AutonomousState = {"messages": [HumanMessage(content="List address objects")]}

        # Call function
        result = call_agent(state)

        # Assertions
        assert "messages" in result
        assert len(result["messages"]) == 1
        assert hasattr(result["messages"][0], "tool_calls")
        assert len(result["messages"][0].tool_calls) == 1
        assert result["messages"][0].tool_calls[0]["name"] == "address_list"

    @patch("src.autonomous_graph.ChatAnthropic")
    @patch("src.autonomous_graph.get_settings")
    def test_call_agent_prepends_system_message(self, mock_settings, mock_chat_anthropic):
        """Test that call_agent prepends system message to conversation."""
        # Setup mocks
        mock_settings.return_value.anthropic_api_key = "test-key"
        mock_llm = Mock()
        mock_response = AIMessage(content="Response")
        mock_llm.invoke.return_value = mock_response
        mock_chat_anthropic.return_value.bind_tools.return_value = mock_llm

        # Create state
        state: AutonomousState = {"messages": [HumanMessage(content="Hello")]}

        # Call function
        call_agent(state)

        # Verify LLM was called with system message prepended
        assert mock_llm.invoke.called
        call_args = mock_llm.invoke.call_args[0][0]
        assert len(call_args) == 2  # System message + user message
        assert "autonomous mode" in call_args[0].content.lower()


class TestRouteAfterAgent:
    """Tests for route_after_agent routing function."""

    def test_route_to_tools_with_tool_calls(self):
        """Test routing to 'tools' when agent makes tool calls."""
        # Create state with tool calls
        state: AutonomousState = {
            "messages": [
                HumanMessage(content="List address objects"),
                AIMessage(
                    content="",
                    tool_calls=[{"name": "address_list", "args": {}, "id": "call_123"}],
                ),
            ]
        }

        # Call routing function
        result = route_after_agent(state)

        # Should route to tools
        assert result == "tools"

    def test_route_to_end_without_tool_calls(self):
        """Test routing to END when agent doesn't make tool calls."""
        # Create state without tool calls
        state: AutonomousState = {
            "messages": [
                HumanMessage(content="Hello"),
                AIMessage(content="Hello! I'm a PAN-OS automation agent."),
            ]
        }

        # Call routing function
        result = route_after_agent(state)

        # Should route to END
        assert result == END

    def test_route_to_end_with_empty_tool_calls(self):
        """Test routing to END when tool_calls is empty list."""
        # Create message with empty tool_calls
        message = AIMessage(content="Done!")
        message.tool_calls = []

        state: AutonomousState = {
            "messages": [HumanMessage(content="Test"), message]
        }

        # Call routing function
        result = route_after_agent(state)

        # Should route to END
        assert result == END

    def test_route_to_tools_with_multiple_tool_calls(self):
        """Test routing to 'tools' with multiple tool calls."""
        # Create state with multiple tool calls
        state: AutonomousState = {
            "messages": [
                HumanMessage(content="Create three address objects"),
                AIMessage(
                    content="",
                    tool_calls=[
                        {"name": "address_create", "args": {"name": "addr1"}, "id": "call_1"},
                        {"name": "address_create", "args": {"name": "addr2"}, "id": "call_2"},
                        {"name": "address_create", "args": {"name": "addr3"}, "id": "call_3"},
                    ],
                ),
            ]
        }

        # Call routing function
        result = route_after_agent(state)

        # Should route to tools
        assert result == "tools"
