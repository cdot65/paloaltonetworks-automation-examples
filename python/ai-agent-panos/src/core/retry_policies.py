"""LangGraph retry policies for PAN-OS operations.

Defines retry policies using LangGraph's built-in RetryPolicy for automatic
retry handling at the node level. This is distinct from retry_helper.py which
provides function-based retry decorators.

Retry policies are applied to graph nodes during construction and handle
transient failures automatically without manual try/except blocks.
"""

from langgraph.types import RetryPolicy
from panos.errors import PanConnectionTimeout, PanURLError

# Retry policy for PAN-OS API operations
# Applied to nodes that interact with the firewall
PANOS_RETRY_POLICY = RetryPolicy(
    max_attempts=3,
    retry_on=(
        PanConnectionTimeout,  # Firewall connection timeouts
        PanURLError,  # Network/URL errors
        ConnectionError,  # Generic connection failures
        TimeoutError,  # Operation timeouts
    ),
    backoff_factor=2.0,  # Exponential backoff: 2s, 4s, 8s
)
"""Retry policy for PAN-OS API operations with exponential backoff.

**Retry behavior:**
- **Max attempts:** 3 (initial + 2 retries)
- **Backoff:** Exponential with factor 2.0 (delays: 2s, 4s, 8s)
- **Retryable errors:**
  - `PanConnectionTimeout` - Firewall connection timeouts
  - `PanURLError` - Network/URL errors (DNS, routing, etc.)
  - `ConnectionError` - Generic connection failures
  - `TimeoutError` - Operation timeouts

**Non-retryable errors:**
All other exceptions (e.g., `PanDeviceError` for validation/config errors)
will fail immediately without retry.

**Usage:**
```python
from langgraph.graph import StateGraph
from src.core.retry_policies import PANOS_RETRY_POLICY

graph = StateGraph(MyState)
graph.add_node("panos_operation", operation_fn, retry=PANOS_RETRY_POLICY)
```

**Logging:**
LangGraph automatically logs retry attempts. Node execution logs will show:
- Retry attempt number
- Error that triggered retry
- Backoff delay before next attempt
"""


# Retry policy for commit operations (shorter max delay for user feedback)
PANOS_COMMIT_RETRY_POLICY = RetryPolicy(
    max_attempts=2,  # Commits less likely to benefit from many retries
    retry_on=(
        PanConnectionTimeout,
        PanURLError,
        ConnectionError,
    ),
    backoff_factor=1.5,  # Shorter backoff: 1.5s, 2.25s
)
"""Retry policy for PAN-OS commit operations.

Commits are user-facing operations where quick failure is preferred over
long retry delays. This policy uses fewer attempts and shorter backoff.

**Retry behavior:**
- **Max attempts:** 2 (initial + 1 retry)
- **Backoff:** Exponential with factor 1.5 (delays: 1.5s, 2.25s)
- **Retryable errors:** Connection and network errors only

**Usage:**
Apply to commit-related nodes in the commit subgraph.
"""
