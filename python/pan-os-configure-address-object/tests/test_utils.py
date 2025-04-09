"""
Tests for the utilities module.

This module contains unit tests for the logging and utility functions.
"""

import logging
import os
from unittest.mock import MagicMock, patch

from utils import Logger, get_env_var, set_log_level, validate_ip_address


def test_logger_singleton() -> None:
    """Test that Logger implements the singleton pattern correctly."""
    logger1 = Logger()
    logger2 = Logger()
    assert logger1 is logger2


def test_logger_set_level() -> None:
    """Test setting log levels on the logger."""
    logger = Logger()

    # Test valid log levels
    valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    for level in valid_levels:
        logger.set_level(level)
        assert logger._logger and logger._logger.getEffectiveLevel() == getattr(
            logging, level
        )

    # Test invalid log level defaults to INFO
    logger.set_level("INVALID")
    assert logger._logger and logger._logger.getEffectiveLevel() == logging.INFO


def test_logger_methods() -> None:
    """Test all logging methods work correctly."""
    logger = Logger()
    mock_logger = MagicMock()
    logger._logger = mock_logger

    # Test each logging method
    test_msg = "Test message"
    test_args = ("arg1", "arg2")
    test_kwargs = {"key1": "value1", "key2": "value2"}

    logger.debug(test_msg, *test_args, **test_kwargs)
    mock_logger.debug.assert_called_with(test_msg, *test_args, **test_kwargs)

    logger.info(test_msg, *test_args, **test_kwargs)
    mock_logger.info.assert_called_with(test_msg, *test_args, **test_kwargs)

    logger.warning(test_msg, *test_args, **test_kwargs)
    mock_logger.warning.assert_called_with(test_msg, *test_args, **test_kwargs)

    logger.error(test_msg, *test_args, **test_kwargs)
    mock_logger.error.assert_called_with(test_msg, *test_args, **test_kwargs)

    logger.critical(test_msg, *test_args, **test_kwargs)
    mock_logger.critical.assert_called_with(test_msg, *test_args, **test_kwargs)


def test_file_logging() -> None:
    """Test that file logging works when PANORAMA_LOG_FILE is set."""
    test_log_file = "test.log"
    with patch.dict(os.environ, {"PANORAMA_LOG_FILE": test_log_file}):
        logger = Logger()
        assert logger._logger
        handlers = logger._logger.handlers
        file_handlers = [h for h in handlers if isinstance(h, logging.FileHandler)]
        assert len(file_handlers) > 0
        assert file_handlers[0].baseFilename == test_log_file


def test_set_log_level() -> None:
    """Test the set_log_level convenience function."""
    with patch("utils.logger") as mock_logger:
        set_log_level("DEBUG")
        mock_logger.set_level.assert_called_once_with("DEBUG")


def test_validate_ip_address() -> None:
    """Test IP address validation."""
    # Valid IPv4 addresses
    valid_ipv4 = [
        "192.168.1.1",
        "10.0.0.0/8",
        "172.16.0.0/16",
        "192.168.1.0/24",
    ]
    for ip in valid_ipv4:
        assert validate_ip_address(ip) is True

    # Invalid IPv4 addresses
    invalid_ipv4 = [
        "256.1.2.3",
        "1.2.3.4/33",
        "192.168.1",
        "invalid",
    ]
    for ip in invalid_ipv4:
        assert validate_ip_address(ip) is False


def test_get_env_var() -> None:
    """Test environment variable retrieval."""
    test_var = "TEST_VAR"
    test_value = "test_value"
    test_default = "default_value"

    # Test getting existing variable
    with patch.dict(os.environ, {test_var: test_value}):
        assert get_env_var(test_var) == test_value

    # Test getting non-existent variable with default
    assert get_env_var(test_var, test_default) == test_default

    # Test getting non-existent variable without default
    assert get_env_var(test_var) is None
