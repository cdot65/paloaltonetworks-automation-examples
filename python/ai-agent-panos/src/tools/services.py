"""Service object tools for PAN-OS.

Tools for creating, reading, updating, deleting, and listing service objects.
"""

import uuid
from typing import Optional

from langchain_core.tools import tool
from src.core.subgraphs.crud import create_crud_subgraph


@tool
def service_create(
    name: str,
    protocol: str,
    port: str,
    description: Optional[str] = None,
    tag: Optional[list[str]] = None,
    mode: str = "strict",
) -> str:
    """Create a new service object on PAN-OS firewall.

    Args:
        name: Name of the service object
        protocol: Protocol (tcp or udp)
        port: Port number or range (e.g., "80", "8080-8090", "443")
        description: Optional description
        tag: Optional list of tags to apply
        mode: Error handling mode - "strict" (fail if exists) or "skip_if_exists" (skip if exists)

    Returns:
        Success/failure message

    Example:
        service_create(name="web-http", protocol="tcp", port="80", description="HTTP service")
        service_create(name="web-http", protocol="tcp", port="80", mode="skip_if_exists")
    """
    crud_graph = create_crud_subgraph()

    data = {
        "name": name,
        "protocol": protocol,
        "destination_port": port,
    }

    if description:
        data["description"] = description
    if tag:
        data["tag"] = tag

    try:
        result = crud_graph.invoke(
            {
                "operation_type": "create",
                "object_type": "service",
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
def service_read(name: str) -> str:
    """Read an existing service object from PAN-OS firewall.

    Args:
        name: Name of the service object to retrieve

    Returns:
        Service object details or error message

    Example:
        service_read(name="web-http")
    """
    crud_graph = create_crud_subgraph()

    try:
        result = crud_graph.invoke(
            {
                "operation_type": "read",
                "object_type": "service",
                "object_name": name,
                "data": None,
            },
            config={"configurable": {"thread_id": str(uuid.uuid4())}},
        )
        return result["message"]
    except Exception as e:
        return f"❌ Error: {type(e).__name__}: {e}"


@tool
def service_update(
    name: str,
    protocol: Optional[str] = None,
    port: Optional[str] = None,
    description: Optional[str] = None,
    tag: Optional[list[str]] = None,
) -> str:
    """Update an existing service object on PAN-OS firewall.

    Args:
        name: Name of the service object to update
        protocol: New protocol (tcp or udp) (optional)
        port: New port number or range (optional)
        description: New description (optional)
        tag: New list of tags (optional)

    Returns:
        Success/failure message

    Example:
        service_update(name="web-http", port="8080", description="Custom HTTP port")
    """
    crud_graph = create_crud_subgraph()

    data = {}
    if protocol:
        data["protocol"] = protocol
    if port:
        data["destination_port"] = port
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
                "object_type": "service",
                "object_name": name,
                "data": data,
            },
            config={"configurable": {"thread_id": str(uuid.uuid4())}},
        )
        return result["message"]
    except Exception as e:
        return f"❌ Error: {type(e).__name__}: {e}"


@tool
def service_delete(name: str, mode: str = "strict") -> str:
    """Delete a service object from PAN-OS firewall.

    Args:
        name: Name of the service object to delete
        mode: Error handling mode - "strict" (fail if missing) or "skip_if_missing" (skip if missing)

    Returns:
        Success/failure message

    Example:
        service_delete(name="web-http")
        service_delete(name="web-http", mode="skip_if_missing")
    """
    crud_graph = create_crud_subgraph()

    try:
        result = crud_graph.invoke(
            {
                "operation_type": "delete",
                "object_type": "service",
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
def service_list() -> str:
    """List all service objects on PAN-OS firewall.

    Returns:
        List of service objects or error message

    Example:
        service_list()
    """
    crud_graph = create_crud_subgraph()

    try:
        result = crud_graph.invoke(
            {
                "operation_type": "list",
                "object_type": "service",
                "object_name": None,
                "data": None,
            },
            config={"configurable": {"thread_id": str(uuid.uuid4())}},
        )
        return result["message"]
    except Exception as e:
        return f"❌ Error: {type(e).__name__}: {e}"


# Export all tools
SERVICE_TOOLS = [
    service_create,
    service_read,
    service_update,
    service_delete,
    service_list,
]
