"""Tests for the PanosClient class."""

import ipaddress
from unittest.mock import MagicMock, patch

import pytest
from pan.xapi import PanXapiError

from models import AddressObject
from panos_client import PanosClient


@pytest.fixture
def mock_panorama() -> MagicMock:
    """Create a mock Panorama instance."""
    return MagicMock()


@pytest.fixture
def client(mock_panorama: MagicMock) -> PanosClient:
    """Create a PanosClient instance with a mock Panorama."""
    return PanosClient(mock_panorama)


def test_create_client_success() -> None:
    """Test successful client creation."""
    with patch("panos_client.Panorama") as mock_panorama:
        mock_instance = MagicMock()
        mock_panorama.return_value = mock_instance

        hostname = "panorama.example.com"
        api_key = "test-api-key"

        client = PanosClient.connect(hostname=hostname, api_key=api_key)
        assert client is not None
        assert client.panorama == mock_instance


def test_create_client_failure() -> None:
    """Test client creation failure."""
    with patch("panos_client.Panorama") as mock_panorama:
        mock_panorama.side_effect = PanXapiError("Connection failed")

        hostname = "panorama.example.com"
        api_key = "test-api-key"

        with pytest.raises(PanXapiError):
            PanosClient.connect(hostname=hostname, api_key=api_key)


def test_get_or_create_device_group_existing(client: PanosClient) -> None:
    """Test getting an existing device group."""
    mock_device_group = MagicMock()
    client.panorama.find.return_value = mock_device_group

    result = client.get_or_create_device_group("test-group")
    assert result == mock_device_group
    client.panorama.find.assert_called_once_with("test-group")


def test_get_or_create_device_group_new(client: PanosClient) -> None:
    """Test creating a new device group."""
    client.panorama.find.return_value = None

    result = client.get_or_create_device_group("test-group")
    assert result is not None
    client.panorama.add.assert_called_once()


def test_get_or_create_device_group_failure(client: PanosClient) -> None:
    """Test device group creation failure."""
    client.panorama.find.return_value = None
    client.panorama.add.side_effect = PanXapiError("Failed to create device group")

    result = client.get_or_create_device_group("test-group")
    assert result is None


def test_create_address_object_success(client: PanosClient) -> None:
    """Test successful address object creation."""
    mock_device_group = MagicMock()
    addr_obj = AddressObject(
        name="test-addr",
        value=ipaddress.ip_network("1.1.1.1/32"),
        description="Test address",
        tags=["test"],
    )

    result = client.create_address_object(mock_device_group, addr_obj)
    assert result is True
    mock_device_group.add.assert_called_once()


def test_create_address_object_failure(client: PanosClient) -> None:
    """Test address object creation failure."""
    mock_device_group = MagicMock()
    mock_device_group.add.side_effect = PanXapiError("Failed to create object")

    addr_obj = AddressObject(
        name="test-addr",
        value=ipaddress.ip_network("1.1.1.1/32"),
        description="Test address",
        tags=["test"],
    )

    result = client.create_address_object(mock_device_group, addr_obj)
    assert result is False


def test_commit_to_panorama_success(client: PanosClient) -> None:
    """Test successful commit to Panorama."""
    result = client.commit_to_panorama()
    assert result is True
    client.panorama.commit.assert_called_once()


def test_commit_to_panorama_failure(client: PanosClient) -> None:
    """Test commit to Panorama failure."""
    client.panorama.commit.side_effect = PanXapiError("Commit failed")
    result = client.commit_to_panorama()
    assert result is False


def test_commit_all_success(client: PanosClient) -> None:
    """Test successful commit all."""
    result = client.commit_all("test-group")
    assert result is True
    client.panorama.commit.assert_called_once()


def test_commit_all_failure(client: PanosClient) -> None:
    """Test commit all failure."""
    client.panorama.commit.side_effect = PanXapiError("Commit failed")
    result = client.commit_all("test-group")
    assert result is False


def test_address_object_input_validation() -> None:
    """Test address object input validation."""
    # Test valid input
    addr_obj = AddressObject(
        name="test-addr",
        value=ipaddress.ip_network("192.168.1.0/24"),
        description="Test address",
        tags=["test"],
    )
    assert addr_obj.name == "test-addr"
    assert str(addr_obj.value) == "192.168.1.0/24"

    # Test invalid IP
    with pytest.raises(ValueError):
        AddressObject(
            name="test-addr",
            value=ipaddress.ip_network("invalid"),
            description="Test address",
            tags=["test"],
        )
