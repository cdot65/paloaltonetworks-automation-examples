"""Batch operations orchestration tool.

High-level tool for parallel batch operations with dependency resolution.
Provides 4-10x speedup for bulk object creation.
"""

import uuid
from typing import Literal

from langchain_core.tools import tool

from src.core.subgraphs.batch import create_batch_subgraph


@tool
def batch_operation(
    operation: Literal["create", "update", "delete"],
    object_type: Literal["address", "address_group", "service", "service_group"],
    items: list[dict],
    max_parallelism: int = 10,
    continue_on_error: bool = True,
) -> str:
    """Execute batch operation with parallel execution and dependency resolution.

    Automatically detects dependencies between items and executes in correct order.
    Items within same dependency level execute in parallel for maximum speed.

    Args:
        operation: Operation to perform on all items (create, update, delete)
        object_type: Type of objects to operate on
        items: List of object dictionaries with 'name' and other fields
        max_parallelism: Maximum concurrent operations (default 10)
        continue_on_error: Continue processing if individual items fail (default True)

    Returns:
        Detailed summary of batch operation results

    Examples:
        # Create multiple addresses (no dependencies)
        batch_operation(
            operation="create",
            object_type="address",
            items=[
                {"name": "server-1", "value": "10.1.1.1"},
                {"name": "server-2", "value": "10.1.1.2"},
                {"name": "server-3", "value": "10.1.1.3"},
            ]
        )

        # Create with dependencies (tags created first, then addresses)
        batch_operation(
            operation="create",
            object_type="address",
            items=[
                {"name": "prod-tag", "color": "Red"},  # Level 0
                {"name": "web-1", "value": "10.1.1.1", "tag": ["prod-tag"]},  # Level 1
                {"name": "web-2", "value": "10.1.1.2", "tag": ["prod-tag"]},  # Level 1
            ]
        )

        # Create address group with members (addresses created first)
        batch_operation(
            operation="create",
            object_type="address_group",
            items=[
                {"name": "web-1", "value": "10.1.1.1"},  # Level 0
                {"name": "web-2", "value": "10.1.1.2"},  # Level 0
                {"name": "web-servers", "static_members": ["web-1", "web-2"]},  # Level 1
            ]
        )

        # Delete multiple objects
        batch_operation(
            operation="delete",
            object_type="address",
            items=[
                {"name": "old-server-1"},
                {"name": "old-server-2"},
            ]
        )
    """
    batch_graph = create_batch_subgraph()

    try:
        result = batch_graph.invoke(
            {
                "operation_type": operation,
                "object_type": object_type,
                "items": items,
                "max_parallelism": max_parallelism,
                "continue_on_error": continue_on_error,
                "dependency_levels": [],
                "current_batch_index": 0,
                "current_batch_results": [],
                "total_items": 0,
                "completed_items": 0,
                "successful_items": 0,
                "failed_items": 0,
                "failure_details": [],
                "result_message": "",
            },
            config={"configurable": {"thread_id": str(uuid.uuid4())}},
        )
        return result["result_message"]
    except Exception as e:
        return f"❌ Batch operation error: {type(e).__name__}: {e}"


@tool
def commit_changes(
    description: str = "Changes via PAN-OS Agent",
    sync: bool = True,
    require_approval: bool = False,
) -> str:
    """Commit pending changes to PAN-OS firewall.

    Args:
        description: Commit description/message
        sync: Wait for commit to complete (True) or return immediately (False)
        require_approval: Require human approval before committing

    Returns:
        Commit operation result

    Examples:
        # Simple commit
        commit_changes(description="Added web servers")

        # Async commit (return immediately)
        commit_changes(description="Policy updates", sync=False)

        # With approval gate
        commit_changes(
            description="Critical security policy changes",
            require_approval=True
        )
    """
    from src.core.subgraphs.commit import create_commit_subgraph

    commit_graph = create_commit_subgraph()

    try:
        result = commit_graph.invoke(
            {
                "description": description,
                "sync": sync,
                "require_approval": require_approval,
                "approval_granted": None,
                "commit_job_id": None,
                "job_status": None,
                "job_result": None,
                "message": "",
                "error": None,
            },
            config={"configurable": {"thread_id": str(uuid.uuid4())}},
        )
        return result["message"]
    except Exception as e:
        return f"❌ Commit error: {type(e).__name__}: {e}"
