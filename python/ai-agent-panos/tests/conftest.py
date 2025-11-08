"""Pytest configuration and shared fixtures for PAN-OS agent tests."""

from unittest.mock import MagicMock, Mock

import pytest


@pytest.fixture
def mock_firewall():
    """Mock PAN-OS firewall client."""
    fw = MagicMock()
    fw.hostname = "192.168.1.1"
    fw.version = "10.2.3"
    fw.serial = "123456789"
    fw.refreshall = Mock()
    fw.find = Mock()
    fw.findall = Mock(return_value=[])
    fw.add = Mock()
    fw.commit = Mock()
    return fw


@pytest.fixture
def mock_address_object():
    """Mock address object."""
    addr = MagicMock()
    addr.name = "test-address"
    addr.value = "10.1.1.1"
    addr.type = "ip-netmask"
    addr.description = "Test address"
    addr.tag = []
    addr.create = Mock()
    addr.apply = Mock()
    addr.delete = Mock()
    return addr


@pytest.fixture
def mock_address_group():
    """Mock address group."""
    group = MagicMock()
    group.name = "test-group"
    group.static_value = ["addr-1", "addr-2"]
    group.description = "Test group"
    group.tag = []
    group.create = Mock()
    group.apply = Mock()
    group.delete = Mock()
    return group


@pytest.fixture
def mock_service_object():
    """Mock service object."""
    svc = MagicMock()
    svc.name = "test-service"
    svc.protocol = "tcp"
    svc.destination_port = "8080"
    svc.description = "Test service"
    svc.tag = []
    svc.create = Mock()
    svc.apply = Mock()
    svc.delete = Mock()
    return svc


@pytest.fixture
def mock_security_rule():
    """Mock security policy rule."""
    rule = MagicMock()
    rule.name = "test-rule"
    rule.fromzone = ["trust"]
    rule.tozone = ["untrust"]
    rule.source = ["any"]
    rule.destination = ["any"]
    rule.service = ["application-default"]
    rule.action = "allow"
    rule.create = Mock()
    rule.apply = Mock()
    rule.delete = Mock()
    return rule


@pytest.fixture
def sample_addresses():
    """Sample address objects for batch tests."""
    return [
        {"name": "addr-1", "value": "10.1.1.1"},
        {"name": "addr-2", "value": "10.1.1.2"},
        {"name": "addr-3", "value": "10.1.1.3"},
    ]


@pytest.fixture
def mock_commit_result():
    """Mock commit job result."""
    result = MagicMock()
    result.id = 123
    result.status = "FIN"
    result.result = "OK"
    return result
