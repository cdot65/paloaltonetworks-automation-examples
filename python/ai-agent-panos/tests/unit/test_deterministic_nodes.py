"""Unit tests for deterministic graph nodes."""

import pytest
from langchain_core.messages import HumanMessage
from unittest.mock import Mock, patch
from langgraph.graph import END

from src.deterministic_graph import load_workflow_definition, execute_workflow, route_after_load
from src.core.state_schemas import DeterministicState


# Sample workflow definitions for testing
VALID_WORKFLOW = {
    "steps": [
        {
            "name": "Create address",
            "type": "tool_call",
            "tool": "address_create",
            "params": {"name": "test-addr", "value": "10.1.1.1"},
        }
    ]
}

WORKFLOWS_MOCK = {
    "simple_address": VALID_WORKFLOW,
    "test_workflow": {
        "steps": [
            {"name": "Step 1", "type": "tool_call", "tool": "address_create", "params": {}},
            {"name": "Step 2", "type": "tool_call", "tool": "address_read", "params": {}},
        ]
    },
}


class TestLoadWorkflowDefinition:
    """Tests for load_workflow_definition node."""

    @patch("src.deterministic_graph.WORKFLOWS", WORKFLOWS_MOCK)
    def test_load_valid_workflow(self):
        """Test loading a valid workflow."""
        state: DeterministicState = {
            "messages": [HumanMessage(content="simple_address")],
            "workflow_steps": [],
            "current_step_index": 0,
            "step_results": [],
            "continue_workflow": False,
            "workflow_complete": False,
            "error_occurred": False,
        }

        result = load_workflow_definition(state)

        # Assertions
        assert result["workflow_steps"] == VALID_WORKFLOW["steps"]
        assert result["current_step_index"] == 0
        assert result["step_results"] == []
        assert result["continue_workflow"] is True
        assert result["workflow_complete"] is False
        assert result["error_occurred"] is False

    @patch("src.deterministic_graph.WORKFLOWS", WORKFLOWS_MOCK)
    def test_load_workflow_with_workflow_prefix(self):
        """Test loading workflow with 'workflow:' prefix in message."""
        state: DeterministicState = {
            "messages": [HumanMessage(content="run workflow: simple_address")],
            "workflow_steps": [],
            "current_step_index": 0,
            "step_results": [],
            "continue_workflow": False,
            "workflow_complete": False,
            "error_occurred": False,
        }

        result = load_workflow_definition(state)

        # Should successfully load workflow
        assert result["workflow_steps"] == VALID_WORKFLOW["steps"]
        assert result["error_occurred"] is False

    @patch("src.deterministic_graph.WORKFLOWS", WORKFLOWS_MOCK)
    def test_load_nonexistent_workflow(self):
        """Test loading a workflow that doesn't exist."""
        state: DeterministicState = {
            "messages": [HumanMessage(content="nonexistent_workflow")],
            "workflow_steps": [],
            "current_step_index": 0,
            "step_results": [],
            "continue_workflow": False,
            "workflow_complete": False,
            "error_occurred": False,
        }

        result = load_workflow_definition(state)

        # Should set error flags
        assert result["workflow_steps"] == []
        assert result["continue_workflow"] is False
        assert result["workflow_complete"] is True
        assert result["error_occurred"] is True
        # Should have error message appended
        assert len(result["messages"]) == 2
        assert "not found" in result["messages"][1]["content"].lower()

    @patch("src.deterministic_graph.WORKFLOWS", {})
    def test_load_workflow_empty_workflows(self):
        """Test loading when no workflows are defined."""
        state: DeterministicState = {
            "messages": [HumanMessage(content="any_workflow")],
            "workflow_steps": [],
            "current_step_index": 0,
            "step_results": [],
            "continue_workflow": False,
            "workflow_complete": False,
            "error_occurred": False,
        }

        result = load_workflow_definition(state)

        # Should return error with "None" available workflows
        assert result["error_occurred"] is True
        assert "Available workflows: None" in result["messages"][1]["content"]


class TestRouteAfterLoad:
    """Tests for route_after_load routing function."""

    def test_route_to_execute_workflow_on_success(self):
        """Test routing to execute_workflow when no error occurred."""
        state: DeterministicState = {
            "messages": [HumanMessage(content="simple_address")],
            "workflow_steps": [{"name": "test"}],
            "current_step_index": 0,
            "step_results": [],
            "continue_workflow": True,
            "workflow_complete": False,
            "error_occurred": False,
        }

        result = route_after_load(state)

        assert result == "execute_workflow"

    def test_route_to_end_on_error(self):
        """Test routing to END when error occurred."""
        state: DeterministicState = {
            "messages": [HumanMessage(content="bad_workflow")],
            "workflow_steps": [],
            "current_step_index": 0,
            "step_results": [],
            "continue_workflow": False,
            "workflow_complete": True,
            "error_occurred": True,
        }

        result = route_after_load(state)

        assert result == END


class TestExecuteWorkflow:
    """Tests for execute_workflow node."""

    @patch("src.deterministic_graph.create_deterministic_workflow_subgraph")
    def test_execute_workflow_success(self, mock_create_subgraph):
        """Test successful workflow execution."""
        # Mock subgraph
        mock_subgraph = Mock()
        mock_subgraph.invoke.return_value = {
            "step_outputs": [
                {"step": "Create address", "status": "success", "result": "✅ Created"}
            ],
            "message": "✅ Workflow complete",
        }
        mock_create_subgraph.return_value = mock_subgraph

        state: DeterministicState = {
            "messages": [HumanMessage(content="simple_address")],
            "workflow_steps": [
                {"name": "Create address", "type": "tool_call", "tool": "address_create"}
            ],
            "current_step_index": 0,
            "step_results": [],
            "continue_workflow": True,
            "workflow_complete": False,
            "error_occurred": False,
        }

        result = execute_workflow(state)

        # Assertions
        assert result["workflow_complete"] is True
        assert len(result["step_results"]) == 1
        assert result["step_results"][0]["status"] == "success"
        # Should have assistant response appended
        assert len(result["messages"]) == 2
        assert "Workflow complete" in result["messages"][1]["content"]

    @patch("src.deterministic_graph.create_deterministic_workflow_subgraph")
    def test_execute_workflow_with_error(self, mock_create_subgraph):
        """Test workflow execution with error."""
        # Mock subgraph that raises exception
        mock_subgraph = Mock()
        mock_subgraph.invoke.side_effect = Exception("Test error")
        mock_create_subgraph.return_value = mock_subgraph

        state: DeterministicState = {
            "messages": [HumanMessage(content="simple_address")],
            "workflow_steps": [{"name": "Create address", "type": "tool_call"}],
            "current_step_index": 0,
            "step_results": [],
            "continue_workflow": True,
            "workflow_complete": False,
            "error_occurred": False,
        }

        result = execute_workflow(state)

        # Should set error flags
        assert result["error_occurred"] is True
        assert result["workflow_complete"] is True
        # Should have error message
        assert "failed" in result["messages"][1]["content"].lower()

    def test_execute_workflow_skips_on_prior_error(self):
        """Test that execute_workflow skips if error already occurred."""
        state: DeterministicState = {
            "messages": [HumanMessage(content="test")],
            "workflow_steps": [],
            "current_step_index": 0,
            "step_results": [],
            "continue_workflow": False,
            "workflow_complete": True,
            "error_occurred": True,
        }

        result = execute_workflow(state)

        # Should return state unchanged
        assert result == state
