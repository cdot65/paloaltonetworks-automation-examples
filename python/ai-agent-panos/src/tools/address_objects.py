"""Address object tools for PAN-OS.

Tools for creating, reading, updating, deleting, and listing address objects.
Thin wrappers around CRUD subgraph for backward compatibility.
"""

import uuid
from typing import Optional

from langchain_core.tools import tool
from src.core.subgraphs.crud import create_crud_subgraph


@tool
def address_create(
    name: str,
    value: str,
    address_type: str = "ip-netmask",
    description: Optional[str] = None,
    tag: Optional[list[str]] = None,
    mode: str = "strict",
) -> str:
    """Create a new address object on PAN-OS firewall.

    Args:
        name: Name of the address object
        value: IP address, network, or FQDN (e.g., "10.1.1.1", "10.1.1.0/24", "example.com")
        address_type: Type of address (ip-netmask, ip-range, fqdn) - default: ip-netmask
        description: Optional description
        tag: Optional list of tags to apply
        mode: Error handling mode - "strict" (fail if exists) or "skip_if_exists" (skip if exists)

    Returns:
        Success/failure message

    Example:
        address_create(name="web-server", value="10.1.1.100", description="Web server")
        address_create(name="web-server", value="10.1.1.100", mode="skip_if_exists")
    """
    crud_graph = create_crud_subgraph()

    data = {
        "name": name,
        "value": value,
        "type": address_type,
    }

    if description:
        data["description"] = description
    if tag:
        data["tag"] = tag

    try:
        result = crud_graph.invoke(
            {
                "operation_type": "create",
                "object_type": "address",
                "data": data,
                "object_name": name,
                "mode": mode,
            },
            config={"configurable": {"thread_id": str(uuid.uuid4())}},
        )
        return result["message"]
    except Exception as e:
        return f"❌ Error: {type(e).__name__}: {e}"


@tool
def address_read(name: str) -> str:
    """Read an existing address object from PAN-OS firewall.

    Args:
        name: Name of the address object to retrieve

    Returns:
        Address object details or error message

    Example:
        address_read(name="web-server")
    """
    crud_graph = create_crud_subgraph()

    try:
        result = crud_graph.invoke(
            {
                "operation_type": "read",
                "object_type": "address",
                "object_name": name,
                "data": None,
            },
            config={"configurable": {"thread_id": str(uuid.uuid4())}},
        )
        return result["message"]
    except Exception as e:
        return f"❌ Error: {type(e).__name__}: {e}"


@tool
def address_update(
    name: str,
    value: Optional[str] = None,
    description: Optional[str] = None,
    tag: Optional[list[str]] = None,
) -> str:
    """Update an existing address object on PAN-OS firewall.

    Args:
        name: Name of the address object to update
        value: New IP address, network, or FQDN (optional)
        description: New description (optional)
        tag: New list of tags (optional)

    Returns:
        Success/failure message

    Example:
        address_update(name="web-server", value="10.1.1.101", description="Updated web server")
    """
    crud_graph = create_crud_subgraph()

    data = {}
    if value:
        data["value"] = value
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
                "object_type": "address",
                "object_name": name,
                "data": data,
            },
            config={"configurable": {"thread_id": str(uuid.uuid4())}},
        )
        return result["message"]
    except Exception as e:
        return f"❌ Error: {type(e).__name__}: {e}"


@tool
def address_delete(name: str, mode: str = "strict") -> str:
    """Delete an address object from PAN-OS firewall.

    Args:
        name: Name of the address object to delete
        mode: Error handling mode - "strict" (fail if missing) or "skip_if_missing" (skip if missing)

    Returns:
        Success/failure message

    Example:
        address_delete(name="web-server")
        address_delete(name="web-server", mode="skip_if_missing")
    """
    crud_graph = create_crud_subgraph()

    try:
        result = crud_graph.invoke(
            {
                "operation_type": "delete",
                "object_type": "address",
                "object_name": name,
                "data": None,
                "mode": mode,
            },
            config={"configurable": {"thread_id": str(uuid.uuid4())}},
        )
        return result["message"]
    except Exception as e:
        return f"❌ Error: {type(e).__name__}: {e}"


@tool
def address_list() -> str:
    """List all address objects on PAN-OS firewall.

    Returns:
        List of address objects or error message

    Example:
        address_list()
    """
    crud_graph = create_crud_subgraph()

    try:
        result = crud_graph.invoke(
            {
                "operation_type": "list",
                "object_type": "address",
                "object_name": None,
                "data": None,
            },
            config={"configurable": {"thread_id": str(uuid.uuid4())}},
        )
        return result["message"]
    except Exception as e:
        return f"❌ Error: {type(e).__name__}: {e}"


# Export all tools
ADDRESS_TOOLS = [
    address_create,
    address_read,
    address_update,
    address_delete,
    address_list,
]
