"""Retry helper with exponential backoff for PAN-OS operations.

Classifies errors as transient (retryable) vs permanent (fail-fast).
Adapted from SCM agent retry patterns for PAN-OS XML API.
"""

import logging
import time
from typing import Any, Callable, Optional

from panos.errors import PanConnectionTimeout, PanDeviceError, PanURLError

logger = logging.getLogger(__name__)


class RetryableError(Exception):
    """Transient error that should be retried."""

    pass


class PermanentError(Exception):
    """Permanent error that should not be retried."""

    pass


def classify_panos_error(error: Exception) -> type[Exception]:
    """Classify PAN-OS error as transient or permanent.

    Args:
        error: Exception from pan-os-python operation

    Returns:
        RetryableError if transient, PermanentError if not retryable
    """
    error_str = str(error).lower()

    # Transient errors (network/timeout issues)
    if isinstance(error, (PanConnectionTimeout, PanURLError)):
        return RetryableError

    if isinstance(error, PanDeviceError):
        # Check error message for transient indicators
        transient_indicators = [
            "timeout",
            "connection",
            "temporary",
            "try again",
            "rate limit",
            "too many requests",
        ]

        for indicator in transient_indicators:
            if indicator in error_str:
                return RetryableError

        # Permanent errors (validation, not found, etc.)
        permanent_indicators = [
            "invalid",
            "does not exist",
            "not found",
            "already exists",
            "duplicate",
            "malformed",
            "permission denied",
        ]

        for indicator in permanent_indicators:
            if indicator in error_str:
                return PermanentError

    # Default to permanent (don't retry unknown errors)
    return PermanentError


def with_retry(
    operation: Callable[..., Any],
    *args: Any,
    max_retries: int = 3,
    initial_delay: float = 1.0,
    max_delay: float = 10.0,
    backoff_factor: float = 2.0,
    **kwargs: Any,
) -> Any:
    """Execute operation with exponential backoff retry.

    Args:
        operation: Function to execute
        *args: Positional arguments for operation
        max_retries: Maximum retry attempts (default 3)
        initial_delay: Initial delay in seconds (default 1.0)
        max_delay: Maximum delay in seconds (default 10.0)
        backoff_factor: Multiplier for delay (default 2.0)
        **kwargs: Keyword arguments for operation

    Returns:
        Result from operation

    Raises:
        PermanentError: If error is not retryable
        Exception: If max retries exceeded
    """
    last_error: Optional[Exception] = None
    delay = initial_delay

    for attempt in range(max_retries + 1):
        try:
            result = operation(*args, **kwargs)
            if attempt > 0:
                logger.info(f"Operation succeeded after {attempt} retries")
            return result

        except Exception as e:
            last_error = e
            error_class = classify_panos_error(e)

            # Don't retry permanent errors
            if error_class == PermanentError:
                logger.error(f"Permanent error (not retrying): {type(e).__name__}: {e}")
                raise PermanentError(str(e)) from e

            # Last attempt - raise original error
            if attempt >= max_retries:
                logger.error(f"Max retries ({max_retries}) exceeded: {type(e).__name__}: {e}")
                raise

            # Retry with backoff
            logger.warning(
                f"Attempt {attempt + 1}/{max_retries} failed: {type(e).__name__}: {e}. "
                f"Retrying in {delay:.1f}s..."
            )
            time.sleep(delay)
            delay = min(delay * backoff_factor, max_delay)

    # Should never reach here
    raise last_error or Exception("Unknown error in retry logic")


def with_retry_async(
    operation: Callable[..., Any],
    *args: Any,
    max_retries: int = 3,
    initial_delay: float = 1.0,
    max_delay: float = 10.0,
    backoff_factor: float = 2.0,
    **kwargs: Any,
) -> Any:
    """Async version of with_retry.

    TODO: Implement async retry logic if needed for async operations.
    Currently pan-os-python is synchronous, so this is a placeholder.
    """
    raise NotImplementedError("Async retry not yet implemented")
