"""State schemas for all graphs and subgraphs.

All TypedDict state definitions in single source of truth.
Follows LangGraph best practices for state management.
"""

import operator
from typing import Annotated, Literal, Optional, Sequence, TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

# ============================================================================
# Main Agent States (for top-level graphs)
# ============================================================================


class AutonomousState(TypedDict):
    """State for autonomous ReAct agent mode.

    ReAct pattern: agent → tools → agent loop with full tool access.
    Messages accumulate conversation history.

    Attributes:
        messages: Conversation history (user prompts, agent responses, tool calls)
    """

    messages: Annotated[Sequence[BaseMessage], add_messages]


class DeterministicState(TypedDict):
    """State for deterministic workflow mode.

    Step-by-step execution with conditional routing and HITL approval gates.
    Similar to Ansible playbook execution.

    Attributes:
        messages: Conversation history
        workflow_steps: List of steps to execute [{step: "create_address", params: {...}}]
        current_step_index: Current step being executed
        step_results: Accumulated results from each step
        continue_workflow: Whether to continue to next step (LLM decision)
        workflow_complete: Whether all steps finished
        error_occurred: Whether any step failed critically
    """

    messages: Annotated[Sequence[BaseMessage], add_messages]
    workflow_steps: list[dict]
    current_step_index: int
    step_results: Annotated[list[dict], operator.add]
    continue_workflow: bool
    workflow_complete: bool
    error_occurred: bool


# ============================================================================
# Subgraph States (transactional operations)
# ============================================================================


class CRUDState(TypedDict):
    """State for single object CRUD operations.

    Workflow: validate → check_existence → create/update/delete → verify → format

    Attributes:
        operation_type: CRUD operation (create, read, update, delete, list)
        object_type: PAN-OS object type (address, service, security_policy, etc.)
        object_name: Name of the object
        data: Object data dictionary (for create/update)
        mode: Error handling mode (strict, skip_if_exists, skip_if_missing)
        validation_result: Result of input validation
        exists: Whether object exists (from check_existence)
        operation_result: Result from create/update/delete operation
        verification_result: Verification after operation
        message: Final formatted message to return
        error: Error message if operation failed
    """

    operation_type: Literal["create", "read", "update", "delete", "list"]
    object_type: str  # address, service, address_group, etc.
    object_name: Optional[str]
    data: Optional[dict]
    mode: Optional[str]  # strict, skip_if_exists, skip_if_missing
    validation_result: Optional[str]
    exists: Optional[bool]
    operation_result: Optional[dict]
    verification_result: Optional[str]
    message: str
    error: Optional[str]


class BatchState(TypedDict):
    """State for parallel batch operations with dependency resolution.

    Workflow: validate → split_into_batches → process_batches (parallel) → aggregate

    Attributes:
        operation_type: CRUD operation for all items
        object_type: PAN-OS object type for all items
        items: List of objects to process
        max_parallelism: Max parallel operations (default 10)
        continue_on_error: Whether to continue after individual failures
        dependency_levels: Items grouped by dependency level [[level0], [level1], ...]
        current_batch_index: Current dependency level being processed
        current_batch_results: Results from current batch (uses operator.add for parallel writes)
        total_items: Total number of items to process
        completed_items: Number of items processed
        successful_items: Number of successful operations
        failed_items: Number of failed operations
        failure_details: List of failure details [{name, error}, ...]
        result_message: Final formatted result message
    """

    operation_type: Literal["create", "read", "update", "delete"]
    object_type: str
    items: list[dict]
    max_parallelism: int
    continue_on_error: bool
    dependency_levels: list[list[dict]]
    current_batch_index: int
    current_batch_results: Annotated[list[dict], operator.add]
    total_items: int
    completed_items: int
    successful_items: int
    failed_items: int
    failure_details: list[dict]
    result_message: str


class CommitState(TypedDict):
    """State for PAN-OS commit operations.

    Workflow: validate → check_approval → execute_commit → poll_jobs → format

    Attributes:
        description: Commit description/message
        sync: Wait for commit completion (True) or return immediately (False)
        require_approval: Whether HITL approval required
        approval_granted: User approval status
        commit_job_id: Job ID from firewall commit
        job_status: Current job status (PEND, ACT, FIN, ERROR)
        job_result: Final job result details
        message: Formatted result message
        error: Error message if commit failed
    """

    description: Optional[str]
    sync: bool
    require_approval: bool
    approval_granted: Optional[bool]
    commit_job_id: Optional[int]
    job_status: Optional[str]
    job_result: Optional[dict]
    message: str
    error: Optional[str]


class DeterministicWorkflowState(TypedDict):
    """State for individual deterministic workflow execution.

    Invoked by deterministic graph to execute pre-defined workflows.

    Attributes:
        workflow_name: Name of workflow to execute
        workflow_params: Parameters for workflow execution
        steps: List of steps in workflow
        current_step: Current step index
        step_outputs: Accumulated outputs from each step (manually managed, no reducer)
        overall_result: Final workflow result
        message: Formatted result message
    """

    workflow_name: str
    workflow_params: dict
    steps: list[dict]
    current_step: int
    step_outputs: list[dict]  # Removed operator.add - manual management
    overall_result: Optional[dict]
    message: str


# ============================================================================
# Helper Reducers
# ============================================================================


def clear_on_empty_reducer(current: list, new: list) -> list:
    """Reducer that clears list if new value is empty.

    Used for batch results - allows clearing accumulator between batches.

    Args:
        current: Current list value
        new: New list value

    Returns:
        Empty list if new is empty, otherwise current + new
    """
    if not new:
        return []
    return current + new
