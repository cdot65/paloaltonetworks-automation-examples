"""Integration tests for subgraphs (CRUD and Commit).

Tests subgraph invocation from parent graphs.
"""

from unittest.mock import Mock, MagicMock, patch

import pytest
from panos.objects import AddressObject


class TestCRUDSubgraphIntegration:
    """Test CRUD subgraph execution in graph context."""

    @patch("src.core.client.get_firewall_client")
    def test_crud_create_operation(self, mock_get_client):
        """Test CRUD subgraph create operation."""
        # Setup mock firewall
        mock_fw = Mock()
        mock_fw.hostname = "192.168.1.1"
        mock_fw.id = "192.168.1.1"
        mock_get_client.return_value = mock_fw

        # Mock AddressObject
        with patch("src.core.subgraphs.crud.AddressObject") as mock_addr_class:
            mock_addr = Mock(spec=AddressObject)
            mock_addr.name = "test-server"
            mock_addr_class.return_value = mock_addr
            mock_addr_class.refreshall = Mock(return_value=[])

            # Create and invoke CRUD subgraph
            from src.core.subgraphs.crud import create_crud_subgraph

            subgraph = create_crud_subgraph()

            result = subgraph.invoke({
                "operation_type": "create",
                "object_type": "address",
                "object_name": "test-server",
                "data": {
                    "name": "test-server",
                    "value": "10.1.1.1",
                    "type": "ip-netmask",
                },
                "validation_result": None,
                "exists": None,
                "operation_result": None,
                "message": "",
                "error": None,
            })

            # Verify successful creation
            assert "message" in result
            assert "✅" in result["message"] or "success" in result["message"].lower()

    @patch("src.core.client.get_firewall_client")
    def test_crud_read_operation(self, mock_get_client):
        """Test CRUD subgraph read operation."""
        # Setup mock firewall
        mock_fw = Mock()
        mock_fw.hostname = "192.168.1.1"
        mock_fw.id = "192.168.1.1"
        mock_get_client.return_value = mock_fw

        # Mock existing object
        with patch("src.core.subgraphs.crud.AddressObject") as mock_addr_class:
            mock_addr = Mock(spec=AddressObject)
            mock_addr.name = "test-server"
            mock_addr.value = "10.1.1.1"
            mock_addr.type = "ip-netmask"
            mock_addr_class.refreshall = Mock(return_value=[mock_addr])

            # Create and invoke CRUD subgraph
            from src.core.subgraphs.crud import create_crud_subgraph

            subgraph = create_crud_subgraph()

            result = subgraph.invoke({
                "operation_type": "read",
                "object_type": "address",
                "object_name": "test-server",
                "data": None,
                "validation_result": None,
                "exists": None,
                "operation_result": None,
                "message": "",
                "error": None,
            })

            # Verify successful read
            assert "message" in result
            assert "test-server" in result["message"]

    @patch("src.core.client.get_firewall_client")
    def test_crud_list_operation(self, mock_get_client):
        """Test CRUD subgraph list operation."""
        # Setup mock firewall
        mock_fw = Mock()
        mock_fw.hostname = "192.168.1.1"
        mock_fw.id = "192.168.1.1"
        mock_get_client.return_value = mock_fw

        # Mock multiple objects
        with patch("src.core.subgraphs.crud.AddressObject") as mock_addr_class:
            mock_objs = [
                Mock(spec=AddressObject, name=f"server-{i}", value=f"10.1.1.{i}")
                for i in range(1, 4)
            ]
            mock_addr_class.refreshall = Mock(return_value=mock_objs)

            # Create and invoke CRUD subgraph
            from src.core.subgraphs.crud import create_crud_subgraph

            subgraph = create_crud_subgraph()

            result = subgraph.invoke({
                "operation_type": "list",
                "object_type": "address",
                "object_name": None,
                "data": None,
                "validation_result": None,
                "exists": None,
                "operation_result": None,
                "message": "",
                "error": None,
            })

            # Verify successful list
            assert "message" in result
            assert "3" in result["message"] or "found" in result["message"].lower()

    @patch("src.core.client.get_firewall_client")
    def test_crud_delete_operation(self, mock_get_client):
        """Test CRUD subgraph delete operation."""
        # Setup mock firewall
        mock_fw = Mock()
        mock_fw.hostname = "192.168.1.1"
        mock_fw.id = "192.168.1.1"
        mock_get_client.return_value = mock_fw

        # Mock existing object
        with patch("src.core.subgraphs.crud.AddressObject") as mock_addr_class:
            mock_addr = Mock(spec=AddressObject)
            mock_addr.name = "test-server"
            mock_addr_class.refreshall = Mock(return_value=[mock_addr])

            # Create and invoke CRUD subgraph
            from src.core.subgraphs.crud import create_crud_subgraph

            subgraph = create_crud_subgraph()

            result = subgraph.invoke({
                "operation_type": "delete",
                "object_type": "address",
                "object_name": "test-server",
                "data": None,
                "validation_result": None,
                "exists": None,
                "operation_result": None,
                "message": "",
                "error": None,
            })

            # Verify successful deletion
            assert "message" in result
            assert "✅" in result["message"] or "deleted" in result["message"].lower()


class TestCommitSubgraphIntegration:
    """Test commit subgraph execution."""

    @patch("src.core.client.get_firewall_client")
    def test_commit_without_approval(self, mock_get_client):
        """Test commit subgraph without approval gate."""
        # Setup mock firewall
        mock_fw = MagicMock()
        mock_fw.hostname = "192.168.1.1"
        mock_fw.commit.return_value = Mock(result="success", jobid=123)
        mock_get_client.return_value = mock_fw

        # Mock job status polling
        with patch("src.core.subgraphs.commit.time.sleep"):
            # Create and invoke commit subgraph
            from src.core.subgraphs.commit import create_commit_subgraph

            subgraph = create_commit_subgraph()

            result = subgraph.invoke({
                "description": "Test commit",
                "sync": False,
                "require_approval": False,
                "approval_granted": None,
                "commit_job_id": None,
                "job_status": None,
                "job_result": None,
                "message": "",
                "error": None,
            })

            # Verify commit executed
            assert "message" in result
            assert "commit" in result["message"].lower()

    @patch("src.core.client.get_firewall_client")
    def test_commit_sync_mode(self, mock_get_client):
        """Test commit subgraph with job polling."""
        # Setup mock firewall
        mock_fw = MagicMock()
        mock_fw.hostname = "192.168.1.1"

        # Mock commit response
        commit_result = Mock()
        commit_result.result = "success"
        commit_result.jobid = 123
        mock_fw.commit.return_value = commit_result

        # Mock job polling - complete immediately
        job_status = Mock()
        job_status.result = "OK"
        job_status.status = "FIN"
        mock_fw.op.return_value = job_status

        mock_get_client.return_value = mock_fw

        with patch("src.core.subgraphs.commit.time.sleep"):
            # Create and invoke commit subgraph
            from src.core.subgraphs.commit import create_commit_subgraph

            subgraph = create_commit_subgraph()

            result = subgraph.invoke({
                "description": "Test commit with polling",
                "sync": True,
                "require_approval": False,
                "approval_granted": None,
                "commit_job_id": None,
                "job_status": None,
                "job_result": None,
                "message": "",
                "error": None,
            })

            # Verify commit completed
            assert "message" in result
            assert "success" in result["message"].lower() or "✅" in result["message"]


class TestSubgraphErrorHandling:
    """Test subgraph error handling and retry behavior."""

    @patch("src.core.client.get_firewall_client")
    def test_crud_handles_connection_error(self, mock_get_client):
        """Test CRUD subgraph handles connection errors with retry."""
        # Setup mock that fails
        mock_fw = Mock()
        mock_fw.hostname = "192.168.1.1"
        mock_get_client.return_value = mock_fw

        # Mock connection error
        from panos.errors import PanConnectionTimeout

        with patch("src.core.subgraphs.crud.AddressObject") as mock_addr_class:
            mock_addr_class.refreshall = Mock(side_effect=PanConnectionTimeout("Connection timeout"))

            # Create and invoke CRUD subgraph
            from src.core.subgraphs.crud import create_crud_subgraph

            subgraph = create_crud_subgraph()

            result = subgraph.invoke({
                "operation_type": "list",
                "object_type": "address",
                "object_name": None,
                "data": None,
                "validation_result": None,
                "exists": None,
                "operation_result": None,
                "message": "",
                "error": None,
            })

            # Should handle error gracefully
            assert "message" in result
            # Error message should be present (retry policy will retry 3 times then fail)
            assert "❌" in result["message"] or "error" in result["message"].lower()

    @patch("src.core.client.get_firewall_client")
    def test_crud_handles_validation_error(self, mock_get_client):
        """Test CRUD subgraph handles validation errors without retry."""
        # Setup mock firewall
        mock_fw = Mock()
        mock_fw.hostname = "192.168.1.1"
        mock_fw.id = "192.168.1.1"
        mock_get_client.return_value = mock_fw

        # Mock validation error
        from panos.errors import PanDeviceError

        with patch("src.core.subgraphs.crud.AddressObject") as mock_addr_class:
            mock_addr = Mock(spec=AddressObject)
            mock_addr_class.return_value = mock_addr
            mock_addr_class.refreshall = Mock(return_value=[])
            mock_addr.create.side_effect = PanDeviceError("Invalid IP address")

            # Create and invoke CRUD subgraph
            from src.core.subgraphs.crud import create_crud_subgraph

            subgraph = create_crud_subgraph()

            result = subgraph.invoke({
                "operation_type": "create",
                "object_type": "address",
                "object_name": "invalid-server",
                "data": {
                    "name": "invalid-server",
                    "value": "256.1.1.1",  # Invalid IP
                    "type": "ip-netmask",
                },
                "validation_result": None,
                "exists": None,
                "operation_result": None,
                "message": "",
                "error": None,
            })

            # Should handle error without retry (validation errors are non-retryable)
            assert "message" in result
            assert "❌" in result["message"] or "error" in result["message"].lower()
            assert "invalid" in result["message"].lower()
