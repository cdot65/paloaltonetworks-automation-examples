"""CRUD subgraph for single PAN-OS object operations.

Workflow: validate → check_existence → create/update/delete → verify → format

Adapted from SCM agent patterns for PAN-OS XML API.
"""

import logging
from typing import Literal

from langgraph.graph import StateGraph, END

from panos.objects import AddressObject, AddressGroup, ServiceObject, ServiceGroup
from panos.policies import SecurityRule, NatRule
from panos.errors import PanDeviceError

from src.core.state_schemas import CRUDState
from src.core.client import get_firewall_client
from src.core.retry_helper import with_retry

logger = logging.getLogger(__name__)

# Mapping of object types to pan-os-python classes
OBJECT_CLASS_MAP = {
    "address": AddressObject,
    "address_group": AddressGroup,
    "service": ServiceObject,
    "service_group": ServiceGroup,
    "security_policy": SecurityRule,
    "nat_policy": NatRule,
}


def validate_input(state: CRUDState) -> CRUDState:
    """Validate CRUD operation inputs.

    Args:
        state: Current CRUD state

    Returns:
        Updated state with validation_result
    """
    logger.info(f"Validating {state['operation_type']} for {state['object_type']}")

    # Check required fields
    if state["operation_type"] in ["create", "update"] and not state.get("data"):
        return {
            **state,
            "validation_result": "❌ Missing required 'data' field",
            "error": "Missing data for create/update operation",
        }

    if state["operation_type"] in ["read", "update", "delete"] and not state.get("object_name"):
        return {
            **state,
            "validation_result": "❌ Missing required 'object_name' field",
            "error": "Missing object_name for operation",
        }

    # Validate object type
    if state["object_type"] not in OBJECT_CLASS_MAP:
        return {
            **state,
            "validation_result": f"❌ Unsupported object_type: {state['object_type']}",
            "error": f"Object type {state['object_type']} not supported",
        }

    return {
        **state,
        "validation_result": "✅ Validation passed",
    }


def check_existence(state: CRUDState) -> CRUDState:
    """Check if object exists on firewall.

    Args:
        state: Current CRUD state

    Returns:
        Updated state with exists flag
    """
    if state.get("error"):
        return state  # Skip if validation failed

    if state["operation_type"] == "list":
        return state  # Skip for list operations

    logger.info(f"Checking existence of {state['object_type']}: {state['object_name']}")

    try:
        fw = get_firewall_client()
        object_class = OBJECT_CLASS_MAP[state["object_type"]]

        # Refresh objects from firewall
        if state["object_type"] in ["address", "address_group", "service", "service_group"]:
            # Objects live under firewall
            fw.refreshall(object_class)
            existing = fw.find(state["object_name"], object_class)
        else:
            # Policies (security/NAT) need different handling
            # For now, simplified - will expand in policy-specific implementation
            existing = None

        exists = existing is not None
        logger.info(f"Object exists: {exists}")

        return {**state, "exists": exists}

    except Exception as e:
        logger.error(f"Error checking existence: {e}")
        return {
            **state,
            "exists": False,
            "error": f"Failed to check existence: {e}",
        }


def route_operation(state: CRUDState) -> Literal["create_object", "read_object", "update_object", "delete_object", "list_objects", "format_response"]:
    """Route to appropriate operation based on operation_type.

    Args:
        state: Current CRUD state

    Returns:
        Next node name
    """
    if state.get("error"):
        return "format_response"

    operation_map = {
        "create": "create_object",
        "read": "read_object",
        "update": "update_object",
        "delete": "delete_object",
        "list": "list_objects",
    }

    return operation_map[state["operation_type"]]


def create_object(state: CRUDState) -> CRUDState:
    """Create new PAN-OS object.

    Args:
        state: Current CRUD state

    Returns:
        Updated state with operation_result
    """
    logger.info(f"Creating {state['object_type']}: {state['data'].get('name')}")

    # Check if already exists
    if state.get("exists"):
        return {
            **state,
            "error": f"Object {state['data'].get('name')} already exists",
            "operation_result": {"status": "error", "message": "Object already exists"},
        }

    try:
        fw = get_firewall_client()
        object_class = OBJECT_CLASS_MAP[state["object_type"]]

        # Create object instance
        obj = object_class(**state["data"])

        # Add to firewall and create
        fw.add(obj)

        def create_op():
            obj.create()

        with_retry(create_op, max_retries=3)

        logger.info(f"Successfully created {state['object_type']}: {state['data'].get('name')}")

        return {
            **state,
            "operation_result": {
                "status": "success",
                "name": state["data"].get("name"),
                "object_type": state["object_type"],
            },
        }

    except Exception as e:
        logger.error(f"Failed to create object: {e}")
        return {
            **state,
            "error": str(e),
            "operation_result": {"status": "error", "message": str(e)},
        }


def read_object(state: CRUDState) -> CRUDState:
    """Read existing PAN-OS object.

    Args:
        state: Current CRUD state

    Returns:
        Updated state with operation_result
    """
    logger.info(f"Reading {state['object_type']}: {state['object_name']}")

    if not state.get("exists"):
        return {
            **state,
            "error": f"Object {state['object_name']} does not exist",
            "operation_result": {"status": "error", "message": "Object not found"},
        }

    try:
        fw = get_firewall_client()
        object_class = OBJECT_CLASS_MAP[state["object_type"]]

        fw.refreshall(object_class)
        obj = fw.find(state["object_name"], object_class)

        # Extract object data
        obj_dict = vars(obj)

        return {
            **state,
            "operation_result": {
                "status": "success",
                "name": state["object_name"],
                "data": obj_dict,
            },
        }

    except Exception as e:
        logger.error(f"Failed to read object: {e}")
        return {
            **state,
            "error": str(e),
            "operation_result": {"status": "error", "message": str(e)},
        }


def update_object(state: CRUDState) -> CRUDState:
    """Update existing PAN-OS object.

    Args:
        state: Current CRUD state

    Returns:
        Updated state with operation_result
    """
    logger.info(f"Updating {state['object_type']}: {state['object_name']}")

    if not state.get("exists"):
        return {
            **state,
            "error": f"Object {state['object_name']} does not exist",
            "operation_result": {"status": "error", "message": "Object not found"},
        }

    try:
        fw = get_firewall_client()
        object_class = OBJECT_CLASS_MAP[state["object_type"]]

        fw.refreshall(object_class)
        obj = fw.find(state["object_name"], object_class)

        # Update attributes from data
        for key, value in state["data"].items():
            if hasattr(obj, key):
                setattr(obj, key, value)

        def update_op():
            obj.apply()

        with_retry(update_op, max_retries=3)

        logger.info(f"Successfully updated {state['object_type']}: {state['object_name']}")

        return {
            **state,
            "operation_result": {
                "status": "success",
                "name": state["object_name"],
                "updated_fields": list(state["data"].keys()),
            },
        }

    except Exception as e:
        logger.error(f"Failed to update object: {e}")
        return {
            **state,
            "error": str(e),
            "operation_result": {"status": "error", "message": str(e)},
        }


def delete_object(state: CRUDState) -> CRUDState:
    """Delete existing PAN-OS object.

    Args:
        state: Current CRUD state

    Returns:
        Updated state with operation_result
    """
    logger.info(f"Deleting {state['object_type']}: {state['object_name']}")

    if not state.get("exists"):
        return {
            **state,
            "error": f"Object {state['object_name']} does not exist",
            "operation_result": {"status": "error", "message": "Object not found"},
        }

    try:
        fw = get_firewall_client()
        object_class = OBJECT_CLASS_MAP[state["object_type"]]

        fw.refreshall(object_class)
        obj = fw.find(state["object_name"], object_class)

        def delete_op():
            obj.delete()

        with_retry(delete_op, max_retries=3)

        logger.info(f"Successfully deleted {state['object_type']}: {state['object_name']}")

        return {
            **state,
            "operation_result": {
                "status": "success",
                "name": state["object_name"],
                "deleted": True,
            },
        }

    except Exception as e:
        logger.error(f"Failed to delete object: {e}")
        return {
            **state,
            "error": str(e),
            "operation_result": {"status": "error", "message": str(e)},
        }


def list_objects(state: CRUDState) -> CRUDState:
    """List all objects of specified type.

    Args:
        state: Current CRUD state

    Returns:
        Updated state with operation_result
    """
    logger.info(f"Listing all {state['object_type']} objects")

    try:
        fw = get_firewall_client()
        object_class = OBJECT_CLASS_MAP[state["object_type"]]

        fw.refreshall(object_class)
        objects = fw.findall(object_class)

        object_list = [{"name": obj.name} for obj in objects]

        return {
            **state,
            "operation_result": {
                "status": "success",
                "count": len(object_list),
                "objects": object_list,
            },
        }

    except Exception as e:
        logger.error(f"Failed to list objects: {e}")
        return {
            **state,
            "error": str(e),
            "operation_result": {"status": "error", "message": str(e)},
        }


def format_response(state: CRUDState) -> CRUDState:
    """Format final response message.

    Args:
        state: Current CRUD state

    Returns:
        Updated state with message field
    """
    if state.get("error"):
        message = f"❌ Error: {state['error']}"
    elif state.get("operation_result"):
        result = state["operation_result"]
        if result.get("status") == "success":
            if state["operation_type"] == "create":
                message = f"✅ Created {state['object_type']}: {result.get('name')}"
            elif state["operation_type"] == "read":
                message = f"✅ Retrieved {state['object_type']}: {result.get('name')}"
            elif state["operation_type"] == "update":
                message = f"✅ Updated {state['object_type']}: {result.get('name')}"
            elif state["operation_type"] == "delete":
                message = f"✅ Deleted {state['object_type']}: {result.get('name')}"
            elif state["operation_type"] == "list":
                message = f"✅ Found {result.get('count')} {state['object_type']} objects"
        else:
            message = f"❌ Operation failed: {result.get('message')}"
    else:
        message = "❌ Unknown error occurred"

    return {**state, "message": message}


def create_crud_subgraph() -> StateGraph:
    """Create CRUD subgraph for single object operations.

    Returns:
        Compiled StateGraph for CRUD operations
    """
    workflow = StateGraph(CRUDState)

    # Add nodes
    workflow.add_node("validate_input", validate_input)
    workflow.add_node("check_existence", check_existence)
    workflow.add_node("create_object", create_object)
    workflow.add_node("read_object", read_object)
    workflow.add_node("update_object", update_object)
    workflow.add_node("delete_object", delete_object)
    workflow.add_node("list_objects", list_objects)
    workflow.add_node("format_response", format_response)

    # Add edges
    workflow.set_entry_point("validate_input")
    workflow.add_edge("validate_input", "check_existence")
    workflow.add_conditional_edges(
        "check_existence",
        route_operation,
        {
            "create_object": "create_object",
            "read_object": "read_object",
            "update_object": "update_object",
            "delete_object": "delete_object",
            "list_objects": "list_objects",
            "format_response": "format_response",
        },
    )
    workflow.add_edge("create_object", "format_response")
    workflow.add_edge("read_object", "format_response")
    workflow.add_edge("update_object", "format_response")
    workflow.add_edge("delete_object", "format_response")
    workflow.add_edge("list_objects", "format_response")
    workflow.add_edge("format_response", END)

    return workflow.compile()
