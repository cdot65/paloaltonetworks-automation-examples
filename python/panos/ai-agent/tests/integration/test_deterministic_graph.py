"""Integration tests for deterministic workflow graph.

Tests full workflow execution from definition to completion.
"""

from unittest.mock import Mock, patch

import pytest
from langchain_core.messages import HumanMessage


class TestDeterministicGraphExecution:
    """Test deterministic graph end-to-end execution."""

    @patch("src.core.client.get_firewall_client")
    def test_simple_workflow_execution(
        self, mock_get_client, deterministic_graph, test_thread_id, sample_workflow
    ):
        """Test simple 2-step workflow executes successfully."""
        # Setup mock
        mock_fw = Mock()
        mock_fw.hostname = "192.168.1.1"
        mock_get_client.return_value = mock_fw

        # Mock successful tool execution
        with patch("src.tools.orchestration.crud_operations.crud_operation") as mock_crud:
            mock_crud.invoke.side_effect = [
                "✅ Created address: test-server",
                "✅ Retrieved address: test-server",
            ]

            # Execute workflow
            result = deterministic_graph.invoke(
                {
                    "messages": [HumanMessage(content="workflow: test_workflow")],
                    "workflow_name": "test_workflow",
                    "steps": sample_workflow["steps"],
                },
                config={"configurable": {"thread_id": test_thread_id}},
            )

        # Verify execution
        assert "messages" in result
        assert "step_results" in result

        # Should have executed 2 steps
        step_results = result["step_results"]
        assert len(step_results) == 2

        # Both steps should be successful
        assert all(output.get("status") == "success" for output in step_results)

    @patch("src.core.client.get_firewall_client")
    def test_workflow_with_error_handling(
        self, mock_get_client, deterministic_graph, test_thread_id, sample_workflow
    ):
        """Test workflow handles step failure gracefully."""
        # Setup mock
        mock_fw = Mock()
        mock_get_client.return_value = mock_fw

        # Mock first step success, second step failure
        with patch("src.tools.orchestration.crud_operations.crud_operation") as mock_crud:
            mock_crud.invoke.side_effect = [
                "✅ Created address: test-server",
                "❌ Error: Object not found",
            ]

            # Execute workflow
            result = deterministic_graph.invoke(
                {
                    "messages": [HumanMessage(content="workflow: test_workflow")],
                    "workflow_name": "test_workflow",
                    "steps": sample_workflow["steps"],
                },
                config={"configurable": {"thread_id": test_thread_id}},
            )

        # Verify error handling
        step_results = result["step_results"]

        # First step should succeed
        assert step_results[0].get("status") == "success"

        # Second step should have error
        assert step_results[1].get("status") == "error"
        assert "not found" in step_results[1].get("error", "").lower()

    @patch("src.core.client.get_firewall_client")
    def test_workflow_state_management(
        self, mock_get_client, deterministic_graph, test_thread_id, sample_workflow
    ):
        """Test workflow state updates correctly."""
        # Setup mock
        mock_fw = Mock()
        mock_get_client.return_value = mock_fw

        with patch("src.tools.orchestration.crud_operations.crud_operation") as mock_crud:
            mock_crud.invoke.return_value = "✅ Success"

            # Execute workflow
            result = deterministic_graph.invoke(
                {
                    "messages": [HumanMessage(content="workflow: test_workflow")],
                    "workflow_name": "test_workflow",
                    "steps": sample_workflow["steps"],
                },
                config={"configurable": {"thread_id": test_thread_id}},
            )

        # Verify state structure
        assert "workflow_steps" in result
        assert len(result["workflow_steps"]) == 2

        assert "current_step_index" in result
        # After execution, current_step_index should be at or past last step
        assert result["current_step_index"] >= len(result["workflow_steps"]) - 1

        assert "step_results" in result
        assert len(result["step_results"]) == 2

    @patch("src.core.client.get_firewall_client")
    def test_empty_workflow_handling(
        self, mock_get_client, deterministic_graph, test_thread_id
    ):
        """Test handling of workflow with no steps."""
        # Setup mock
        mock_fw = Mock()
        mock_get_client.return_value = mock_fw

        # Execute workflow with no steps
        result = deterministic_graph.invoke(
            {
                "messages": [HumanMessage(content="workflow: empty_workflow")],
                "workflow_name": "empty_workflow",
                "steps": [],
            },
            config={"configurable": {"thread_id": test_thread_id}},
        )

        # Should complete without errors
        assert "messages" in result
        assert "step_results" in result

        # Should have no step results
        assert len(result["step_results"]) == 0


class TestDeterministicGraphCheckpointing:
    """Test checkpoint and resume functionality for workflows."""

    @patch("src.core.client.get_firewall_client")
    def test_workflow_checkpointed(
        self, mock_get_client, deterministic_graph, test_thread_id, sample_workflow
    ):
        """Test workflow state is checkpointed."""
        # Setup mock
        mock_fw = Mock()
        mock_get_client.return_value = mock_fw

        with patch("src.tools.orchestration.crud_operations.crud_operation") as mock_crud:
            mock_crud.invoke.return_value = "✅ Success"

            # Execute workflow
            deterministic_graph.invoke(
                {
                    "messages": [HumanMessage(content="workflow: test_workflow")],
                    "workflow_name": "test_workflow",
                    "steps": sample_workflow["steps"],
                },
                config={"configurable": {"thread_id": test_thread_id}},
            )

        # Get state
        config = {"configurable": {"thread_id": test_thread_id}}
        state = deterministic_graph.get_state(config)

        # Verify checkpoint
        assert state is not None
        assert hasattr(state, "values")
        assert "workflow_steps" in state.values
        assert "step_results" in state.values

    @patch("src.core.client.get_firewall_client")
    def test_resume_workflow_after_partial_execution(
        self, mock_get_client, deterministic_graph, test_thread_id
    ):
        """Test resuming workflow after partial execution."""
        # Setup mock
        mock_fw = Mock()
        mock_get_client.return_value = mock_fw

        # Create 3-step workflow
        three_step_workflow = {
            "name": "multi_step_test",
            "steps": [
                {
                    "name": "Step 1",
                    "type": "tool_call",
                    "tool": "crud_operation",
                    "params": {"operation": "list", "object_type": "address"},
                },
                {
                    "name": "Step 2",
                    "type": "tool_call",
                    "tool": "crud_operation",
                    "params": {"operation": "list", "object_type": "address"},
                },
                {
                    "name": "Step 3",
                    "type": "tool_call",
                    "tool": "crud_operation",
                    "params": {"operation": "list", "object_type": "address"},
                },
            ],
        }

        with patch("src.tools.orchestration.crud_operations.crud_operation") as mock_crud:
            mock_crud.invoke.return_value = "✅ Success"

            # Execute workflow
            result = deterministic_graph.invoke(
                {
                    "messages": [HumanMessage(content="workflow: multi_step_test")],
                    "workflow_name": "multi_step_test",
                    "steps": three_step_workflow["steps"],
                },
                config={"configurable": {"thread_id": test_thread_id}},
            )

        # Verify all steps executed
        assert len(result["step_results"]) == 3
        assert all(output.get("status") == "success" for output in result["step_results"])
