"""
Utility functions for the Palo Alto Networks Panorama configuration tool.

This module provides logging setup and other utility functions.
"""

import ipaddress
import logging
import os
from typing import Any, Optional


class Logger:
    """
    A singleton logger class for consistent logging across the application.

    This class ensures that only one logger instance is created and used
    throughout the application, with consistent formatting and log levels.
    """

    _instance: Optional["Logger"] = None
    _logger: Optional[logging.Logger] = None

    def __new__(cls) -> "Logger":
        """Create or return the singleton logger instance."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._setup_logger()
        return cls._instance

    def _setup_logger(self) -> None:
        """Set up the logger with handlers and formatters."""
        # Reset handlers if they exist
        if self._logger:
            for handler in self._logger.handlers[:]:
                self._logger.removeHandler(handler)

        self._logger = logging.getLogger("panorama")
        self._logger.setLevel(logging.INFO)

        # Create formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        # Create console handler
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        self._logger.addHandler(handler)

        # Add file handler if PANORAMA_LOG_FILE is set
        log_file = os.getenv("PANORAMA_LOG_FILE")
        if log_file:
            try:
                file_handler = logging.FileHandler(log_file)
                file_handler.setFormatter(formatter)
                self._logger.addHandler(file_handler)
            except (IOError, PermissionError) as e:
                # Log to console if file handler creation fails
                handler.setLevel(logging.ERROR)
                self._logger.error("Failed to create file handler: %s", e)

    def debug(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log a debug message."""
        if self._logger:
            self._logger.debug(msg, *args, **kwargs)

    def info(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log an info message."""
        if self._logger:
            self._logger.info(msg, *args, **kwargs)

    def error(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log an error message."""
        if self._logger:
            self._logger.error(msg, *args, **kwargs)

    def warning(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log a warning message."""
        if self._logger:
            self._logger.warning(msg, *args, **kwargs)

    def critical(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log a critical message."""
        if self._logger:
            self._logger.critical(msg, *args, **kwargs)

    def set_level(self, level: str) -> None:
        """Set the logging level."""
        if self._logger:
            try:
                self._logger.setLevel(getattr(logging, level.upper()))
            except AttributeError:
                # Default to INFO if invalid level
                self._logger.setLevel(logging.INFO)


# Create a global logger instance
logger = Logger()


def set_log_level(level: str) -> None:
    """
    Set the global logging level.

    Args:
        level: The logging level to set (e.g., 'DEBUG', 'INFO', etc.)
    """
    logger.set_level(level)


def validate_ip_address(ip_str: str) -> bool:
    """
    Validate an IP address or network.

    Args:
        ip_str: The IP address or network to validate
               (e.g., '192.168.1.1' or '10.0.0.0/24')

    Returns:
        bool: True if valid, False otherwise
    """
    try:
        ipaddress.ip_network(ip_str)
        return True
    except ValueError:
        return False


def get_env_var(key: str, default: Optional[str] = None) -> Optional[str]:
    """
    Get an environment variable value.

    Args:
        key: The environment variable key
        default: Optional default value if key is not found

    Returns:
        Optional[str]: The environment variable value or default
    """
    return os.getenv(key, default)
