"""Integration tests for autonomous (ReAct) graph.

Tests full graph execution from user input to final response.
"""

from unittest.mock import Mock, patch

import pytest
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage


class TestAutonomousGraphExecution:
    """Test autonomous graph end-to-end execution."""

    @patch("src.core.client.get_firewall_client")
    def test_simple_query_no_tools(self, mock_get_client, autonomous_graph, test_thread_id):
        """Test simple conversational query without tool calls."""
        # Setup mock
        mock_fw = Mock()
        mock_get_client.return_value = mock_fw

        # Execute graph
        result = autonomous_graph.invoke(
            {"messages": [HumanMessage(content="Hello, how are you?")]},
            config={"configurable": {"thread_id": test_thread_id}},
        )

        # Verify response structure
        assert "messages" in result
        assert len(result["messages"]) > 0

        # Last message should be AI response
        last_message = result["messages"][-1]
        assert isinstance(last_message, AIMessage)
        assert last_message.content  # Has content

        # Should not have tool calls for greeting
        assert not hasattr(last_message, "tool_calls") or not last_message.tool_calls

    @patch("src.core.client.get_firewall_client")
    @patch("src.tools.address_objects.address_list")
    def test_query_with_single_tool(
        self, mock_address_list, mock_get_client, autonomous_graph, test_thread_id
    ):
        """Test query that triggers single tool execution."""
        # Setup mocks
        mock_fw = Mock()
        mock_get_client.return_value = mock_fw

        # Mock tool response
        mock_address_list.invoke.return_value = "✅ Found 5 address objects"

        # Execute graph
        result = autonomous_graph.invoke(
            {"messages": [HumanMessage(content="List all address objects")]},
            config={"configurable": {"thread_id": test_thread_id}},
        )

        # Verify execution
        assert "messages" in result
        messages = result["messages"]

        # Should have: HumanMessage, AIMessage(tool_calls), ToolMessage, AIMessage(final)
        assert len(messages) >= 3

        # Check for tool execution
        has_tool_message = any(isinstance(msg, ToolMessage) for msg in messages)
        assert has_tool_message, "Should have executed a tool"

        # Final message should be AI response
        last_message = messages[-1]
        assert isinstance(last_message, AIMessage)

    @patch("src.core.client.get_firewall_client")
    def test_conversation_continuity(self, mock_get_client, autonomous_graph, test_thread_id):
        """Test that conversation history is maintained across invocations."""
        # Setup mock
        mock_fw = Mock()
        mock_get_client.return_value = mock_fw

        # First message
        result1 = autonomous_graph.invoke(
            {"messages": [HumanMessage(content="My name is Alice")]},
            config={"configurable": {"thread_id": test_thread_id}},
        )

        # Second message referencing first
        result2 = autonomous_graph.invoke(
            {"messages": [HumanMessage(content="What is my name?")]},
            config={"configurable": {"thread_id": test_thread_id}},
        )

        # Verify history is maintained
        assert "messages" in result2
        messages = result2["messages"]

        # Should have all messages from both invocations
        assert len(messages) >= 4  # 2 human + 2 AI minimum

        # Check that both human messages are present
        human_messages = [msg for msg in messages if isinstance(msg, HumanMessage)]
        assert len(human_messages) >= 2

    @patch("src.core.client.get_firewall_client")
    def test_fresh_thread_no_history(self, mock_get_client, autonomous_graph):
        """Test that different thread IDs create independent conversations."""
        # Setup mock
        mock_fw = Mock()
        mock_get_client.return_value = mock_fw

        # First conversation
        thread_id_1 = "test-thread-1"
        result1 = autonomous_graph.invoke(
            {"messages": [HumanMessage(content="My favorite color is blue")]},
            config={"configurable": {"thread_id": thread_id_1}},
        )

        # Second conversation with different thread
        thread_id_2 = "test-thread-2"
        result2 = autonomous_graph.invoke(
            {"messages": [HumanMessage(content="Hello")]},
            config={"configurable": {"thread_id": thread_id_2}},
        )

        # Second conversation should not have first conversation's messages
        messages = result2["messages"]
        human_messages = [msg for msg in messages if isinstance(msg, HumanMessage)]

        # Should only have one human message (the greeting)
        assert len(human_messages) == 1
        assert human_messages[0].content == "Hello"


class TestAutonomousGraphCheckpointing:
    """Test checkpoint and resume functionality."""

    @patch("src.core.client.get_firewall_client")
    def test_checkpoint_after_execution(self, mock_get_client, autonomous_graph, test_thread_id):
        """Test that state is checkpointed after execution."""
        # Setup mock
        mock_fw = Mock()
        mock_get_client.return_value = mock_fw

        # Execute graph
        autonomous_graph.invoke(
            {"messages": [HumanMessage(content="Test message")]},
            config={"configurable": {"thread_id": test_thread_id}},
        )

        # Get state to verify checkpoint exists
        config = {"configurable": {"thread_id": test_thread_id}}
        state = autonomous_graph.get_state(config)

        # Verify checkpoint was created
        assert state is not None
        assert hasattr(state, "values")
        assert "messages" in state.values

    @patch("src.core.client.get_firewall_client")
    def test_resume_from_checkpoint(self, mock_get_client, autonomous_graph, test_thread_id):
        """Test resuming conversation from checkpoint."""
        # Setup mock
        mock_fw = Mock()
        mock_get_client.return_value = mock_fw

        # First execution
        result1 = autonomous_graph.invoke(
            {"messages": [HumanMessage(content="Remember the number 42")]},
            config={"configurable": {"thread_id": test_thread_id}},
        )

        # Resume with same thread
        result2 = autonomous_graph.invoke(
            {"messages": [HumanMessage(content="What number did I tell you?")]},
            config={"configurable": {"thread_id": test_thread_id}},
        )

        # Verify conversation continuity
        messages = result2["messages"]
        assert len(messages) >= 4  # Both exchanges

        # Should have both human messages
        human_contents = [msg.content for msg in messages if isinstance(msg, HumanMessage)]
        assert "Remember the number 42" in human_contents
        assert "What number did I tell you?" in human_contents
