"""Orchestration tool for CRUD operations.

High-level tool that delegates to CRUD subgraph.
Provides unified interface for all object types.
"""

import uuid
from typing import Literal, Optional

from langchain_core.tools import tool
from src.core.subgraphs.crud import create_crud_subgraph


@tool
def crud_operation(
    operation: Literal["create", "read", "update", "delete", "list"],
    object_type: Literal[
        "address", "address_group", "service", "service_group", "security_policy", "nat_policy"
    ],
    object_name: Optional[str] = None,
    data: Optional[dict] = None,
) -> str:
    """Execute CRUD operation on PAN-OS object.

    Unified interface for all CRUD operations across all object types.
    Delegates to CRUD subgraph for execution.

    Args:
        operation: CRUD operation to perform
        object_type: Type of PAN-OS object
        object_name: Name of object (required for read/update/delete)
        data: Object data dictionary (required for create/update)

    Returns:
        Success/failure message from CRUD subgraph

    Examples:
        # Create address object
        crud_operation(
            operation="create",
            object_type="address",
            data={"name": "web-server", "value": "10.1.1.100"}
        )

        # Read address object
        crud_operation(
            operation="read",
            object_type="address",
            object_name="web-server"
        )

        # Update address object
        crud_operation(
            operation="update",
            object_type="address",
            object_name="web-server",
            data={"value": "10.1.1.101"}
        )

        # Delete address object
        crud_operation(
            operation="delete",
            object_type="address",
            object_name="web-server"
        )

        # List all address objects
        crud_operation(
            operation="list",
            object_type="address"
        )
    """
    crud_graph = create_crud_subgraph()

    try:
        result = crud_graph.invoke(
            {
                "operation_type": operation,
                "object_type": object_type,
                "object_name": object_name,
                "data": data,
            },
            config={"configurable": {"thread_id": str(uuid.uuid4())}},
        )
        return result["message"]
    except Exception as e:
        return f"❌ Error: {type(e).__name__}: {e}"
