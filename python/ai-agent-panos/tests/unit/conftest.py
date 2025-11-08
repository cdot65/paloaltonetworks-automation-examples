"""Shared fixtures for unit tests."""

import pytest
from langchain_core.messages import AIMessage, HumanMessage
from unittest.mock import Mock, MagicMock


@pytest.fixture
def mock_llm():
    """Mock ChatAnthropic LLM for testing."""
    llm = Mock()
    # Mock response without tool calls
    mock_response = AIMessage(content="Hello! I'm a PAN-OS automation agent.")
    llm.invoke.return_value = mock_response
    return llm


@pytest.fixture
def mock_llm_with_tool_call():
    """Mock LLM that returns a tool call."""
    llm = Mock()
    # Mock response with tool calls
    mock_response = AIMessage(
        content="",
        tool_calls=[
            {
                "name": "address_list",
                "args": {},
                "id": "call_123",
            }
        ],
    )
    llm.invoke.return_value = mock_response
    return llm


@pytest.fixture
def mock_state_autonomous():
    """Sample AutonomousState fixture."""
    return {
        "messages": [HumanMessage(content="List all address objects")],
    }


@pytest.fixture
def mock_state_deterministic():
    """Sample DeterministicState fixture."""
    return {
        "messages": [HumanMessage(content="simple_address")],
        "workflow_steps": [
            {
                "name": "Create address object",
                "type": "tool_call",
                "tool": "address_create",
                "params": {
                    "name": "demo-server",
                    "value": "192.168.1.100",
                },
            }
        ],
        "current_step_index": 0,
        "step_results": [],
        "continue_workflow": True,
        "workflow_complete": False,
        "error_occurred": False,
    }


@pytest.fixture
def mock_state_crud():
    """Sample CRUDState fixture."""
    return {
        "operation_type": "create",
        "object_type": "address",
        "object_name": "test-server",
        "data": {
            "name": "test-server",
            "value": "192.168.1.100",
        },
        "validation_result": None,
        "exists": False,
        "operation_result": None,
        "message": "",
        "error": None,
    }


@pytest.fixture
def mock_state_commit():
    """Sample CommitState fixture."""
    return {
        "description": "Test commit",
        "force": False,
        "approval_required": True,
        "approved": None,
        "job_id": None,
        "commit_result": None,
        "message": "",
        "error": None,
    }


@pytest.fixture
def mock_state_workflow():
    """Sample DeterministicWorkflowState fixture."""
    return {
        "workflow_name": "test_workflow",
        "workflow_params": {},
        "steps": [
            {
                "name": "Step 1",
                "type": "tool_call",
                "tool": "address_create",
                "params": {
                    "name": "{{server_name}}",
                    "value": "{{server_ip}}",
                },
            }
        ],
        "current_step": 0,
        "step_outputs": [],
        "overall_result": None,
        "message": "",
    }


@pytest.fixture
def mock_firewall_client(monkeypatch):
    """Mock PAN-OS firewall client globally."""
    mock_fw = MagicMock()
    mock_fw.hostname = "192.168.1.1"
    mock_fw.serial = "021201109830"
    mock_fw.version = "11.1.4-h7"

    # Mock get_firewall_client function
    def mock_get_client():
        return mock_fw

    monkeypatch.setattr("src.core.client.get_firewall_client", mock_get_client)
    return mock_fw


@pytest.fixture
def mock_tool():
    """Mock tool for testing."""
    tool = Mock()
    tool.name = "test_tool"
    tool.invoke.return_value = "✅ Tool executed successfully"
    return tool


@pytest.fixture
def sample_workflow_definition():
    """Sample workflow definition for testing."""
    return {
        "name": "test_workflow",
        "description": "Test workflow for unit tests",
        "steps": [
            {
                "name": "Create address",
                "type": "tool_call",
                "tool": "address_create",
                "params": {
                    "name": "test-addr",
                    "value": "10.1.1.1",
                },
            },
            {
                "name": "Verify creation",
                "type": "tool_call",
                "tool": "address_read",
                "params": {
                    "name": "test-addr",
                },
            },
        ],
    }
