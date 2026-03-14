"""Service group tools for PAN-OS.

Tools for creating, reading, updating, deleting, and listing service groups.
"""

import uuid
from typing import Optional

from langchain_core.tools import tool
from src.core.subgraphs.crud import create_crud_subgraph


@tool
def service_group_create(
    name: str,
    members: list[str],
    description: Optional[str] = None,
    tag: Optional[list[str]] = None,
    mode: str = "strict",
) -> str:
    """Create a new service group on PAN-OS firewall.

    Args:
        name: Name of the service group
        members: List of service object names to include in group
        description: Optional description
        tag: Optional list of tags to apply
        mode: Error handling mode - "strict" (fail if exists) or "skip_if_exists" (skip if exists)

    Returns:
        Success/failure message

    Example:
        service_group_create(
            name="web-services",
            members=["web-http", "web-https"],
            description="Web service group"
        )
        service_group_create(name="web-services", members=["web-http"], mode="skip_if_exists")
    """
    crud_graph = create_crud_subgraph()

    data = {
        "name": name,
        "value": members,
    }

    if description:
        data["description"] = description
    if tag:
        data["tag"] = tag

    try:
        result = crud_graph.invoke(
            {
                "operation_type": "create",
                "object_type": "service_group",
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
def service_group_read(name: str) -> str:
    """Read an existing service group from PAN-OS firewall.

    Args:
        name: Name of the service group to retrieve

    Returns:
        Service group details or error message

    Example:
        service_group_read(name="web-services")
    """
    crud_graph = create_crud_subgraph()

    try:
        result = crud_graph.invoke(
            {
                "operation_type": "read",
                "object_type": "service_group",
                "object_name": name,
                "data": None,
            },
            config={"configurable": {"thread_id": str(uuid.uuid4())}},
        )
        return result["message"]
    except Exception as e:
        return f"❌ Error: {type(e).__name__}: {e}"


@tool
def service_group_update(
    name: str,
    members: Optional[list[str]] = None,
    description: Optional[str] = None,
    tag: Optional[list[str]] = None,
) -> str:
    """Update an existing service group on PAN-OS firewall.

    Args:
        name: Name of the service group to update
        members: New list of service object names (optional)
        description: New description (optional)
        tag: New list of tags (optional)

    Returns:
        Success/failure message

    Example:
        service_group_update(name="web-services", members=["web-http", "web-https", "web-alt"])
    """
    crud_graph = create_crud_subgraph()

    data = {}
    if members:
        data["value"] = members
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
                "object_type": "service_group",
                "object_name": name,
                "data": data,
            },
            config={"configurable": {"thread_id": str(uuid.uuid4())}},
        )
        return result["message"]
    except Exception as e:
        return f"❌ Error: {type(e).__name__}: {e}"


@tool
def service_group_delete(name: str) -> str:
    """Delete a service group from PAN-OS firewall.

    Args:
        name: Name of the service group to delete

    Returns:
        Success/failure message

    Example:
        service_group_delete(name="web-services")
    """
    crud_graph = create_crud_subgraph()

    try:
        result = crud_graph.invoke(
            {
                "operation_type": "delete",
                "object_type": "service_group",
                "object_name": name,
                "data": None,
            },
            config={"configurable": {"thread_id": str(uuid.uuid4())}},
        )
        return result["message"]
    except Exception as e:
        return f"❌ Error: {type(e).__name__}: {e}"


@tool
def service_group_list() -> str:
    """List all service groups on PAN-OS firewall.

    Returns:
        List of service groups or error message

    Example:
        service_group_list()
    """
    crud_graph = create_crud_subgraph()

    try:
        result = crud_graph.invoke(
            {
                "operation_type": "list",
                "object_type": "service_group",
                "object_name": None,
                "data": None,
            },
            config={"configurable": {"thread_id": str(uuid.uuid4())}},
        )
        return result["message"]
    except Exception as e:
        return f"❌ Error: {type(e).__name__}: {e}"


# Export all tools
SERVICE_GROUP_TOOLS = [
    service_group_create,
    service_group_read,
    service_group_update,
    service_group_delete,
    service_group_list,
]
