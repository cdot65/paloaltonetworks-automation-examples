"""Unit tests for PAN-OS tools."""

import pytest
from unittest.mock import Mock, MagicMock, patch


class TestAddressTools:
    """Tests for address object tools."""

    @patch("src.tools.address_objects.create_crud_subgraph")
    def test_address_create_success(self, mock_create_subgraph):
        """Test creating an address object successfully."""
        from src.tools.address_objects import address_create

        # Mock subgraph
        mock_subgraph = Mock()
        mock_subgraph.invoke.return_value = {
            "message": "✅ Created address: test-addr"
        }
        mock_create_subgraph.return_value = mock_subgraph

        result = address_create.invoke({"name": "test-addr", "value": "10.1.1.1"})

        # Should return success string
        assert isinstance(result, str)
        assert "✅" in result or "created" in result.lower()

    @patch("src.tools.address_objects.create_crud_subgraph")
    def test_address_read_success(self, mock_create_subgraph):
        """Test reading an address object."""
        from src.tools.address_objects import address_read

        # Mock subgraph
        mock_subgraph = Mock()
        mock_subgraph.invoke.return_value = {
            "message": "✅ Retrieved address: test-addr"
        }
        mock_create_subgraph.return_value = mock_subgraph

        result = address_read.invoke({"name": "test-addr"})

        # Should return success string
        assert isinstance(result, str)
        assert "test-addr" in result.lower() or "✅" in result

    @patch("src.tools.address_objects.create_crud_subgraph")
    def test_address_list_success(self, mock_create_subgraph):
        """Test listing address objects."""
        from src.tools.address_objects import address_list

        # Mock subgraph
        mock_subgraph = Mock()
        mock_subgraph.invoke.return_value = {
            "message": "✅ Found 2 address objects"
        }
        mock_create_subgraph.return_value = mock_subgraph

        result = address_list.invoke({})

        # Should return success string
        assert isinstance(result, str)
        assert "address" in result.lower()

    @patch("src.tools.address_objects.create_crud_subgraph")
    def test_address_delete_success(self, mock_create_subgraph):
        """Test deleting an address object."""
        from src.tools.address_objects import address_delete

        # Mock subgraph
        mock_subgraph = Mock()
        mock_subgraph.invoke.return_value = {
            "message": "✅ Deleted address: test-addr"
        }
        mock_create_subgraph.return_value = mock_subgraph

        result = address_delete.invoke({"name": "test-addr"})

        # Should return success string
        assert isinstance(result, str)
        assert "✅" in result or "deleted" in result.lower()


class TestServiceTools:
    """Tests for service object tools."""

    @patch("src.tools.services.create_crud_subgraph")
    def test_service_create_success(self, mock_create_subgraph):
        """Test creating a service object."""
        from src.tools.services import service_create

        # Mock subgraph
        mock_subgraph = Mock()
        mock_subgraph.invoke.return_value = {
            "message": "✅ Created service: http-8080"
        }
        mock_create_subgraph.return_value = mock_subgraph

        result = service_create.invoke({
            "name": "http-8080",
            "protocol": "tcp",
            "port": "8080",  # Fixed: use 'port' not 'destination_port'
        })

        # Should return success string
        assert isinstance(result, str)
        assert "✅" in result or "success" in result.lower()

    @patch("src.tools.services.create_crud_subgraph")
    def test_service_list_success(self, mock_create_subgraph):
        """Test listing service objects."""
        from src.tools.services import service_list

        # Mock subgraph
        mock_subgraph = Mock()
        mock_subgraph.invoke.return_value = {
            "message": "✅ Found 1 service objects"
        }
        mock_create_subgraph.return_value = mock_subgraph

        result = service_list.invoke({})

        # Should return success string
        assert isinstance(result, str)
        assert "service" in result.lower() or "✅" in result


class TestSecurityPolicyTools:
    """Tests for security policy tools."""

    @pytest.mark.skip(reason="pan-os-python policy mocking too complex - needs integration test")
    @patch("src.core.client.get_firewall_client")
    def test_security_policy_create_success(self, mock_get_client):
        """Test creating a security policy."""
        from src.tools.security_policies import security_policy_create

        # Mock firewall client
        mock_fw = MagicMock()
        mock_get_client.return_value = mock_fw

        result = security_policy_create.invoke({
            "name": "allow-web",
            "fromzone": ["trust"],
            "tozone": ["untrust"],
            "source": ["any"],
            "destination": ["any"],
            "service": ["application-default"],
            "action": "allow",
        })

        # Should return success string
        assert isinstance(result, str)
        assert "✅" in result or "created" in result.lower()


class TestNATPolicyTools:
    """Tests for NAT policy tools."""

    @pytest.mark.skip(reason="pan-os-python policy mocking too complex - needs integration test")
    @patch("src.core.client.get_firewall_client")
    def test_nat_policy_create_success(self, mock_get_client):
        """Test creating a NAT policy."""
        from src.tools.nat_policies import nat_policy_create_source

        # Mock firewall client
        mock_fw = MagicMock()
        mock_get_client.return_value = mock_fw

        result = nat_policy_create_source.invoke({
            "name": "nat-rule-1",
            "fromzone": ["trust"],
            "tozone": ["untrust"],
            "source": ["any"],
            "destination": ["any"],
        })

        # Should return success string
        assert isinstance(result, str)
        assert "✅" in result or "created" in result.lower()


class TestOrchestrationTools:
    """Tests for orchestration tools."""

    @patch("src.tools.orchestration.crud_operations.create_crud_subgraph")
    def test_crud_operation_create(self, mock_create_subgraph):
        """Test CRUD operation tool with create."""
        from src.tools.orchestration.crud_operations import crud_operation

        # Mock subgraph
        mock_subgraph = Mock()
        mock_subgraph.invoke.return_value = {
            "message": "✅ Created address: test-addr"
        }
        mock_create_subgraph.return_value = mock_subgraph

        result = crud_operation.invoke({
            "operation": "create",
            "object_type": "address",
            "name": "test-addr",
            "data": {"name": "test-addr", "value": "10.1.1.1"},
        })

        # Should return success string
        assert isinstance(result, str)
        assert "✅" in result or "created" in result.lower()

    @patch("src.tools.orchestration.crud_operations.create_crud_subgraph")
    def test_crud_operation_list(self, mock_create_subgraph):
        """Test CRUD operation tool with list."""
        from src.tools.orchestration.crud_operations import crud_operation

        # Mock subgraph
        mock_subgraph = Mock()
        mock_subgraph.invoke.return_value = {
            "message": "✅ Found 5 address objects"
        }
        mock_create_subgraph.return_value = mock_subgraph

        result = crud_operation.invoke({
            "operation": "list",
            "object_type": "address",
        })

        # Should return success string
        assert isinstance(result, str)
        assert "address" in result.lower()

    @patch("src.core.subgraphs.commit.create_commit_subgraph")
    def test_commit_changes_success(self, mock_create_subgraph):
        """Test commit_changes tool."""
        from src.tools.orchestration.commit_operations import commit_changes

        # Mock subgraph
        mock_subgraph = Mock()
        mock_subgraph.invoke.return_value = {
            "message": "✅ Commit completed successfully"
        }
        mock_create_subgraph.return_value = mock_subgraph

        result = commit_changes.invoke({"description": "Test commit"})

        # Should return success string
        assert isinstance(result, str)
        assert "✅" in result or "commit" in result.lower()

    @patch("src.core.subgraphs.commit.create_commit_subgraph")
    def test_commit_changes_with_error(self, mock_create_subgraph):
        """Test commit_changes tool with error."""
        from src.tools.orchestration.commit_operations import commit_changes

        # Mock subgraph that returns error
        mock_subgraph = Mock()
        mock_subgraph.invoke.return_value = {
            "message": "❌ Error: Commit failed"
        }
        mock_create_subgraph.return_value = mock_subgraph

        result = commit_changes.invoke({"description": "Test commit"})

        # Should return error string, not raise
        assert isinstance(result, str)
        assert "❌" in result or "error" in result.lower()


class TestToolErrorHandling:
    """Tests for tool error handling patterns."""

    @patch("src.tools.address_objects.create_crud_subgraph")
    def test_tool_handles_exceptions(self, mock_create_subgraph):
        """Test that tools catch exceptions and return error strings."""
        from src.tools.address_objects import address_list

        # Mock subgraph that raises exception
        mock_subgraph = Mock()
        mock_subgraph.invoke.side_effect = Exception("Connection error")
        mock_create_subgraph.return_value = mock_subgraph

        # Tool should catch exception and return error string
        result = address_list.invoke({})

        assert isinstance(result, str)
        assert "❌" in result or "error" in result.lower()

    @patch("src.tools.services.create_crud_subgraph")
    def test_tool_handles_subgraph_errors(self, mock_create_subgraph):
        """Test that tools handle subgraph error responses."""
        from src.tools.services import service_create

        # Mock subgraph that returns error message
        mock_subgraph = Mock()
        mock_subgraph.invoke.return_value = {
            "message": "❌ Error: API error"
        }
        mock_create_subgraph.return_value = mock_subgraph

        result = service_create.invoke({
            "name": "test-svc",
            "protocol": "tcp",
            "port": "80",  # Fixed: use 'port' not 'destination_port'
        })

        # Should return error string
        assert isinstance(result, str)
        assert "❌" in result or "error" in result.lower()
