"""Shared fixtures for integration tests.

Provides compiled graph fixtures and mock firewall client.
"""

import uuid
from unittest.mock import MagicMock, Mock, patch

import pytest
from panos.firewall import Firewall
from panos.objects import AddressObject


@pytest.fixture
def mock_firewall():
    """Mock PAN-OS firewall client for integration tests.

    Returns:
        Mock firewall with common methods and attributes
    """
    fw = MagicMock(spec=Firewall)
    fw.hostname = "192.168.1.1"
    fw.api_key = "test-api-key"
    fw.serial = "021201109830"
    fw.version = "11.1.4-h7"

    # Mock refreshall to avoid xpath errors
    def mock_refreshall(obj_class, fw_instance):
        """Mock refreshall to return empty list."""
        return []

    # Patch at class level
    AddressObject.refreshall = Mock(side_effect=mock_refreshall)

    return fw


@pytest.fixture
def autonomous_graph(mock_firewall):
    """Create autonomous graph with mocked firewall.

    Returns:
        Compiled autonomous StateGraph
    """
    with patch("src.core.client.get_firewall_client", return_value=mock_firewall):
        from src.autonomous_graph import create_autonomous_graph

        graph = create_autonomous_graph()
        return graph


@pytest.fixture
def deterministic_graph(mock_firewall):
    """Create deterministic graph with mocked firewall.

    Returns:
        Compiled deterministic StateGraph
    """
    with patch("src.core.client.get_firewall_client", return_value=mock_firewall):
        from src.deterministic_graph import create_deterministic_graph

        graph = create_deterministic_graph()
        return graph


@pytest.fixture
def test_thread_id():
    """Generate unique thread ID for test isolation.

    Returns:
        UUID string for thread ID
    """
    return f"test-{uuid.uuid4()}"


@pytest.fixture
def sample_workflow():
    """Sample workflow definition for deterministic tests.

    Returns:
        Dict with workflow steps
    """
    return {
        "name": "test_workflow",
        "description": "Test workflow for integration tests",
        "steps": [
            {
                "name": "Create test address",
                "type": "tool_call",
                "tool": "crud_operation",
                "params": {
                    "operation": "create",
                    "object_type": "address",
                    "name": "test-server",
                    "data": {
                        "name": "test-server",
                        "value": "10.1.1.1",
                        "type": "ip-netmask",
                        "description": "Test address",
                    },
                },
            },
            {
                "name": "Verify address exists",
                "type": "tool_call",
                "tool": "crud_operation",
                "params": {
                    "operation": "read",
                    "object_type": "address",
                    "name": "test-server",
                },
            },
        ],
    }
