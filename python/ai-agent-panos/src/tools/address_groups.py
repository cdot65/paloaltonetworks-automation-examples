"""Address group tools for PAN-OS.

Tools for creating, reading, updating, deleting, and listing address groups.
"""

import uuid
from typing import Optional

from langchain_core.tools import tool
from src.core.subgraphs.crud import create_crud_subgraph


@tool
def address_group_create(
    name: str,
    static_members: list[str],
    description: Optional[str] = None,
    tag: Optional[list[str]] = None,
) -> str:
    """Create a new address group on PAN-OS firewall.

    Args:
        name: Name of the address group
        static_members: List of address object names to include in group
        description: Optional description
        tag: Optional list of tags to apply

    Returns:
        Success/failure message

    Example:
        address_group_create(
            name="web-servers",
            static_members=["web-1", "web-2"],
            description="Web server group"
        )
    """
    crud_graph = create_crud_subgraph()

    data = {
        "name": name,
        "static_value": static_members,
    }

    if description:
        data["description"] = description
    if tag:
        data["tag"] = tag

    try:
        result = crud_graph.invoke(
            {
                "operation_type": "create",
                "object_type": "address_group",
                "data": data,
                "object_name": name,
            },
            config={"configurable": {"thread_id": str(uuid.uuid4())}},
        )
        return result["message"]
    except Exception as e:
        return f"❌ Error: {type(e).__name__}: {e}"


@tool
def address_group_read(name: str) -> str:
    """Read an existing address group from PAN-OS firewall.

    Args:
        name: Name of the address group to retrieve

    Returns:
        Address group details or error message

    Example:
        address_group_read(name="web-servers")
    """
    crud_graph = create_crud_subgraph()

    try:
        result = crud_graph.invoke(
            {
                "operation_type": "read",
                "object_type": "address_group",
                "object_name": name,
                "data": None,
            },
            config={"configurable": {"thread_id": str(uuid.uuid4())}},
        )
        return result["message"]
    except Exception as e:
        return f"❌ Error: {type(e).__name__}: {e}"


@tool
def address_group_update(
    name: str,
    static_members: Optional[list[str]] = None,
    description: Optional[str] = None,
    tag: Optional[list[str]] = None,
) -> str:
    """Update an existing address group on PAN-OS firewall.

    Args:
        name: Name of the address group to update
        static_members: New list of address object names (optional)
        description: New description (optional)
        tag: New list of tags (optional)

    Returns:
        Success/failure message

    Example:
        address_group_update(name="web-servers", static_members=["web-1", "web-2", "web-3"])
    """
    crud_graph = create_crud_subgraph()

    data = {}
    if static_members:
        data["static_value"] = static_members
    if description:
        data["description"] = description
    if tag is not None:
        data["tag"] = tag

    if not data:
        return "❌ Error: No fields provided for update"

    try:
        result = crud_graph.invoke(
            {
                "operation_type": "update",
                "object_type": "address_group",
                "object_name": name,
                "data": data,
            },
            config={"configurable": {"thread_id": str(uuid.uuid4())}},
        )
        return result["message"]
    except Exception as e:
        return f"❌ Error: {type(e).__name__}: {e}"


@tool
def address_group_delete(name: str) -> str:
    """Delete an address group from PAN-OS firewall.

    Args:
        name: Name of the address group to delete

    Returns:
        Success/failure message

    Example:
        address_group_delete(name="web-servers")
    """
    crud_graph = create_crud_subgraph()

    try:
        result = crud_graph.invoke(
            {
                "operation_type": "delete",
                "object_type": "address_group",
                "object_name": name,
                "data": None,
            },
            config={"configurable": {"thread_id": str(uuid.uuid4())}},
        )
        return result["message"]
    except Exception as e:
        return f"❌ Error: {type(e).__name__}: {e}"


@tool
def address_group_list() -> str:
    """List all address groups on PAN-OS firewall.

    Returns:
        List of address groups or error message

    Example:
        address_group_list()
    """
    crud_graph = create_crud_subgraph()

    try:
        result = crud_graph.invoke(
            {
                "operation_type": "list",
                "object_type": "address_group",
                "object_name": None,
                "data": None,
            },
            config={"configurable": {"thread_id": str(uuid.uuid4())}},
        )
        return result["message"]
    except Exception as e:
        return f"❌ Error: {type(e).__name__}: {e}"


# Export all tools
ADDRESS_GROUP_TOOLS = [
    address_group_create,
    address_group_read,
    address_group_update,
    address_group_delete,
    address_group_list,
]
