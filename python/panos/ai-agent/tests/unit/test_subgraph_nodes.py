"""Unit tests for subgraph node functions."""

import pytest
from unittest.mock import Mock, MagicMock, patch

from src.core.subgraphs.crud import (
    validate_input,
    check_existence,
    route_operation,
)
from src.core.subgraphs.commit import (
    validate_commit_input,
    check_approval_required,
)
from src.core.subgraphs.deterministic import (
    load_workflow,
    execute_step,
    route_after_evaluation,
)
from src.core.state_schemas import CRUDState, CommitState, DeterministicWorkflowState


class TestCRUDSubgraph:
    """Tests for CRUD subgraph nodes."""

    def test_validate_input_success_create(self):
        """Test validation passes for valid create operation."""
        state: CRUDState = {
            "operation_type": "create",
            "object_type": "address",
            "object_name": None,
            "data": {"name": "test-addr", "value": "10.1.1.1"},
            "validation_result": None,
            "exists": None,
            "operation_result": None,
            "message": "",
            "error": None,
        }

        result = validate_input(state)

        assert result["validation_result"] == "✅ Validation passed"
        assert result["error"] is None

    def test_validate_input_missing_data_for_create(self):
        """Test validation fails when data missing for create."""
        state: CRUDState = {
            "operation_type": "create",
            "object_type": "address",
            "object_name": None,
            "data": None,  # Missing data
            "validation_result": None,
            "exists": None,
            "operation_result": None,
            "message": "",
            "error": None,
        }

        result = validate_input(state)

        assert "Missing required 'data' field" in result["validation_result"]
        assert result["error"] is not None

    def test_validate_input_missing_object_name_for_read(self):
        """Test validation fails when object_name missing for read."""
        state: CRUDState = {
            "operation_type": "read",
            "object_type": "address",
            "object_name": None,  # Missing for read
            "data": None,
            "validation_result": None,
            "exists": None,
            "operation_result": None,
            "message": "",
            "error": None,
        }

        result = validate_input(state)

        assert "Missing required 'object_name' field" in result["validation_result"]
        assert result["error"] is not None

    def test_validate_input_unsupported_object_type(self):
        """Test validation fails for unsupported object type."""
        state: CRUDState = {
            "operation_type": "create",
            "object_type": "unsupported_type",
            "object_name": None,
            "data": {"name": "test"},
            "validation_result": None,
            "exists": None,
            "operation_result": None,
            "message": "",
            "error": None,
        }

        result = validate_input(state)

        assert "Unsupported object_type" in result["validation_result"]
        assert result["error"] is not None

    @pytest.mark.skip(reason="pan-os-python mocking too complex - needs integration test")
    @patch("src.core.subgraphs.crud.get_firewall_client")
    @patch("src.core.subgraphs.crud.AddressObject")
    def test_check_existence_object_exists(self, mock_address_class, mock_get_client):
        """Test check_existence when object exists."""
        # Mock firewall client
        mock_fw = MagicMock()
        mock_fw.version = "11.1.0"  # Add version to avoid xpath errors
        mock_get_client.return_value = mock_fw

        # Mock refreshall to return list with one object
        mock_obj = Mock()
        mock_obj.name = "existing-addr"
        mock_address_class.refreshall = Mock(return_value=[mock_obj])

        state: CRUDState = {
            "operation_type": "read",
            "object_type": "address",
            "object_name": "existing-addr",
            "data": None,
            "validation_result": None,
            "exists": None,
            "operation_result": None,
            "message": "",
            "error": None,
        }

        result = check_existence(state)

        # Verify refreshall was called
        mock_address_class.refreshall.assert_called_once_with(mock_fw)
        assert result["exists"] is True
        assert result["error"] is None

    @pytest.mark.skip(reason="pan-os-python mocking too complex - needs integration test")
    @patch("src.core.subgraphs.crud.get_firewall_client")
    @patch("src.core.subgraphs.crud.AddressObject")
    def test_check_existence_object_not_exists(self, mock_address_class, mock_get_client):
        """Test check_existence when object doesn't exist."""
        # Mock firewall client
        mock_fw = MagicMock()
        mock_fw.version = "11.1.0"
        mock_get_client.return_value = mock_fw

        # Mock refreshall to return empty list
        mock_address_class.refreshall = Mock(return_value=[])

        state: CRUDState = {
            "operation_type": "create",
            "object_type": "address",
            "object_name": "new-addr",
            "data": {"name": "new-addr", "value": "10.1.1.1"},
            "validation_result": None,
            "exists": None,
            "operation_result": None,
            "message": "",
            "error": None,
        }

        result = check_existence(state)

        # Verify refreshall was called
        mock_address_class.refreshall.assert_called_once_with(mock_fw)
        assert result["exists"] is False
        assert result["error"] is None

    def test_route_operation_create(self):
        """Test routing to create_object for create operation."""
        state: CRUDState = {
            "operation_type": "create",
            "object_type": "address",
            "object_name": None,
            "data": {},
            "validation_result": None,
            "exists": False,
            "operation_result": None,
            "message": "",
            "error": None,
        }

        result = route_operation(state)

        assert result == "create_object"

    def test_route_operation_to_format_on_error(self):
        """Test routing to format_response when error exists."""
        state: CRUDState = {
            "operation_type": "create",
            "object_type": "address",
            "object_name": None,
            "data": None,
            "validation_result": None,
            "exists": None,
            "operation_result": None,
            "message": "",
            "error": "Validation error",
        }

        result = route_operation(state)

        assert result == "format_response"


class TestCommitSubgraph:
    """Tests for Commit subgraph nodes."""

    def test_validate_commit_input_success(self):
        """Test validation passes for valid commit."""
        state: CommitState = {
            "description": "Test commit",
            "force": False,
            "approval_required": False,
            "approved": None,
            "job_id": None,
            "commit_result": None,
            "message": "",
            "error": None,
        }

        from src.core.subgraphs.commit import validate_commit_input

        result = validate_commit_input(state)

        assert "✅" in result["message"] or result["error"] is None

    def test_check_approval_not_required_by_default(self):
        """Test that approval is not required by default."""
        state: CommitState = {
            "description": "Normal commit",
            "force": False,
            "approval_required": False,
            "approved": None,
            "job_id": None,
            "commit_result": None,
            "message": "",
            "error": None,
        }

        result = check_approval_required(state)

        # When require_approval is False or not set, approval_granted should be True
        assert result.get("approval_granted") is True

    def test_check_approval_not_required_when_force_false(self):
        """Test that approval not required when force=False."""
        state: CommitState = {
            "description": "Normal commit",
            "force": False,
            "approval_required": False,
            "approved": None,
            "job_id": None,
            "commit_result": None,
            "message": "",
            "error": None,
        }

        result = check_approval_required(state)

        assert result["approval_required"] is False


class TestDeterministicWorkflowSubgraph:
    """Tests for Deterministic workflow subgraph nodes."""

    def test_load_workflow_success(self):
        """Test loading workflow with valid steps."""
        state: DeterministicWorkflowState = {
            "workflow_name": "test_workflow",
            "workflow_params": {},
            "steps": [
                {"name": "Step 1", "type": "tool_call", "tool": "address_create"}
            ],
            "current_step": 0,
            "step_outputs": [],
            "overall_result": None,
            "message": "",
        }

        result = load_workflow(state)

        assert result["current_step"] == 0
        assert result["step_outputs"] == []
        assert result.get("message") != "❌ Error"

    def test_load_workflow_no_steps(self):
        """Test loading workflow with no steps."""
        state: DeterministicWorkflowState = {
            "workflow_name": "empty_workflow",
            "workflow_params": {},
            "steps": [],  # Empty steps
            "current_step": 0,
            "step_outputs": [],
            "overall_result": None,
            "message": "",
        }

        result = load_workflow(state)

        assert "❌ Error" in result["message"]
        assert "No steps defined" in result["message"]

    @patch("src.core.subgraphs.deterministic.ALL_TOOLS")
    def test_execute_step_tool_call_success(self, mock_all_tools):
        """Test executing a tool call step successfully."""
        # Mock tool
        mock_tool = Mock()
        mock_tool.name = "address_create"
        mock_tool.invoke.return_value = "✅ Created address"
        mock_all_tools.__iter__.return_value = [mock_tool]

        state: DeterministicWorkflowState = {
            "workflow_name": "test",
            "workflow_params": {},
            "steps": [
                {
                    "name": "Create address",
                    "type": "tool_call",
                    "tool": "address_create",
                    "params": {"name": "test-addr"},
                }
            ],
            "current_step": 0,
            "step_outputs": [],
            "overall_result": None,
            "message": "",
        }

        result = execute_step(state)

        assert len(result["step_outputs"]) == 1
        assert result["step_outputs"][0]["status"] == "success"
        assert "✅" in result["step_outputs"][0]["result"]

    def test_route_after_evaluation_continue(self):
        """Test routing to increment_step when decision is continue."""
        state: DeterministicWorkflowState = {
            "workflow_name": "test",
            "workflow_params": {},
            "steps": [{"name": "Step 1"}, {"name": "Step 2"}],
            "current_step": 0,
            "step_outputs": [],
            "overall_result": {"decision": "continue", "reason": "Success"},
            "message": "",
        }

        result = route_after_evaluation(state)

        assert result == "increment_step"

    def test_route_after_evaluation_stop(self):
        """Test routing to format_result when decision is stop."""
        state: DeterministicWorkflowState = {
            "workflow_name": "test",
            "workflow_params": {},
            "steps": [{"name": "Step 1"}],
            "current_step": 0,
            "step_outputs": [],
            "overall_result": {"decision": "stop", "reason": "Error occurred"},
            "message": "",
        }

        result = route_after_evaluation(state)

        assert result == "format_result"

    def test_route_after_evaluation_last_step(self):
        """Test routing to format_result when on last step with continue."""
        state: DeterministicWorkflowState = {
            "workflow_name": "test",
            "workflow_params": {},
            "steps": [{"name": "Step 1"}],
            "current_step": 0,  # Last step (index 0 of 1 step)
            "step_outputs": [],
            "overall_result": {"decision": "continue", "reason": "Success"},
            "message": "",
        }

        result = route_after_evaluation(state)

        # Should route to format_result since no more steps
        assert result == "format_result"
