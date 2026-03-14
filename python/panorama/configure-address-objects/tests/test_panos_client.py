"""Test cases for the PanosClient class."""

import ipaddress
from unittest.mock import MagicMock, patch

import pytest
from pan.xapi import PanXapiError

from models import AddressObject
from panos.errors import PanDeviceError
from panos.panorama import DeviceGroup
from panos_client import PanosClient


@pytest.fixture
def client() -> PanosClient:
    """Create a PanosClient instance with a mocked Panorama."""
    mock_panorama = MagicMock()
    return PanosClient(mock_panorama)


def test_connect_success() -> None:
    """Test successful connection to Panorama."""
    hostname = "test-host"
    api_key = "test-api-key"

    with patch("panos_client.Panorama") as mock_panorama, patch(
        "panos_client.DeviceGroup"
    ) as mock_device_group:
        mock_panorama.return_value.refresh_system_info.return_value = None
        mock_device_group.refreshall.return_value = []
        client = PanosClient.connect(hostname=hostname, api_key=api_key)
        assert client.panorama == mock_panorama.return_value
        mock_device_group.refreshall.assert_called_once_with(mock_panorama.return_value)


def test_connect_failure() -> None:
    """Test connection failure to Panorama."""
    hostname = "test-host"
    api_key = "test-api-key"

    with patch("panos_client.Panorama") as mock_panorama:
        mock_panorama.return_value.refresh_system_info.side_effect = PanDeviceError(
            "Connection failed"
        )
        with pytest.raises(PanDeviceError):
            PanosClient.connect(hostname=hostname, api_key=api_key)


def test_get_or_create_device_group_existing(client: PanosClient) -> None:
    """Test getting an existing device group."""
    mock_device_group = MagicMock()
    client.panorama.find.return_value = mock_device_group

    result = client.get_or_create_device_group("test-group")
    assert result == mock_device_group
    client.panorama.find.assert_called_once_with("test-group", DeviceGroup)


def test_get_or_create_device_group_new(client: PanosClient) -> None:
    """Test creating a new device group."""
    client.panorama.find.return_value = None
    mock_device_group = MagicMock()
    with patch("panos_client.DeviceGroup", return_value=mock_device_group) as mock_dg:
        result = client.get_or_create_device_group("test-group")
        mock_dg.assert_called_once_with(name="test-group")
        client.panorama.add.assert_called_once_with(mock_device_group)
        mock_device_group.create.assert_called_once()
        assert result == mock_device_group


def test_get_or_create_device_group_failure(client: PanosClient) -> None:
    """Test device group creation failure."""
    client.panorama.find.return_value = None
    client.panorama.add.side_effect = PanXapiError("Failed to create device group")

    result = client.get_or_create_device_group("test-group")
    assert result is None


def test_create_address_object_success(client: PanosClient) -> None:
    """Test successful address object creation."""
    mock_device_group = MagicMock()
    mock_device_group.add.return_value = None
    addr_obj = AddressObject(
        name="test-addr",
        value=ipaddress.ip_network("1.1.1.1/32"),
        description="Test address",
        tags=["test"],
    )

    with patch("panos_client.PanAddressObject") as mock_pan_addr:
        mock_pan_addr_instance = mock_pan_addr.return_value
        mock_pan_addr_instance.create.return_value = None

        result = client.create_address_object(mock_device_group, addr_obj)
        assert result is True
        mock_device_group.add.assert_called_once_with(mock_pan_addr_instance)
        mock_pan_addr_instance.create.assert_called_once()


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
    client.panorama.commit.return_value = {"result": "ok"}
    with patch("panos_client.PanoramaCommit") as mock_commit:
        result = client.commit_to_panorama()
        assert result is True
        client.panorama.commit.assert_called_once_with(cmd=mock_commit.return_value)


def test_commit_to_panorama_failure(client: PanosClient) -> None:
    """Test commit to Panorama failure."""
    client.panorama.commit.side_effect = PanXapiError("Commit failed")
    result = client.commit_to_panorama()
    assert result is False


def test_commit_all_success(client: PanosClient) -> None:
    """Test successful commit all."""
    client.panorama.commit_all.return_value = {"result": "ok"}
    with patch("panos_client.PanoramaCommitAll") as mock_commit_all:
        result = client.commit_all(["test-group"])
        assert result is True
        client.panorama.commit_all.assert_called_once_with(
            cmd=mock_commit_all.return_value
        )


def test_commit_all_failure(client: PanosClient) -> None:
    """Test commit all failure."""
    client.panorama.commit_all.side_effect = PanXapiError("Commit failed")
    with patch("panos_client.PanoramaCommitAll"):
        result = client.commit_all(["test-group"])
        assert result is False
