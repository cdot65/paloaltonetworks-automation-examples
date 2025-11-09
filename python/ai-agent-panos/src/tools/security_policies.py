"""Security policy tools for PAN-OS.

Full CRUD operations for security policy rule management.
"""

from typing import Optional

from langchain_core.tools import tool
from src.core.client import get_firewall_client
from src.core.retry_helper import with_retry


@tool
def security_policy_list() -> str:
    """List all security policy rules on PAN-OS firewall.

    Returns:
        List of security policy rules or error message

    Example:
        security_policy_list()
    """
    try:
        from panos.policies import SecurityRule

        fw = get_firewall_client()
        fw.refreshall(SecurityRule)
        rules = fw.findall(SecurityRule)

        if not rules:
            return "✅ No security policy rules found"

        rule_list = [{"name": rule.name, "action": rule.action} for rule in rules]

        return f"✅ Found {len(rule_list)} security policy rules:\n" + "\n".join(
            [f"- {r['name']} (action: {r['action']})" for r in rule_list]
        )

    except Exception as e:
        return f"❌ Error: {type(e).__name__}: {e}"


@tool
def security_policy_read(name: str) -> str:
    """Read an existing security policy rule from PAN-OS firewall.

    Args:
        name: Name of the security policy rule to retrieve

    Returns:
        Security policy rule details or error message

    Example:
        security_policy_read(name="allow-web-traffic")
    """
    try:
        from panos.policies import SecurityRule

        fw = get_firewall_client()
        fw.refreshall(SecurityRule)
        rule = fw.find(name, SecurityRule)

        if not rule:
            return f"❌ Error: Security policy rule '{name}' not found"

        return (
            f"✅ Retrieved security policy rule: {name}\n"
            f"Action: {rule.action}\n"
            f"From zone: {rule.fromzone}\n"
            f"To zone: {rule.tozone}"
        )

    except Exception as e:
        return f"❌ Error: {type(e).__name__}: {e}"


@tool
def security_policy_create(
    name: str,
    fromzone: list[str],
    tozone: list[str],
    source: list[str],
    destination: list[str],
    service: list[str],
    action: str = "allow",
    description: Optional[str] = None,
    tag: Optional[list[str]] = None,
    log_end: bool = True,
) -> str:
    """Create a new security policy rule on PAN-OS firewall.

    Args:
        name: Name of the security policy rule
        fromzone: List of source zones (e.g., ["trust"])
        tozone: List of destination zones (e.g., ["untrust"])
        source: List of source addresses (e.g., ["any", "10.1.1.0/24"])
        destination: List of destination addresses (e.g., ["any"])
        service: List of services (e.g., ["application-default", "service-http"])
        action: Action to take (allow, deny, drop) - default: allow
        description: Optional description
        tag: Optional list of tags
        log_end: Log at session end (default: True)

    Returns:
        Success/failure message

    Example:
        security_policy_create(
            name="allow-web-traffic",
            fromzone=["trust"],
            tozone=["untrust"],
            source=["10.1.1.0/24"],
            destination=["any"],
            service=["service-http", "service-https"],
            action="allow",
            description="Allow web traffic from internal network"
        )
    """
    try:
        from panos.policies import SecurityRule

        fw = get_firewall_client()

        # Check if rule already exists
        fw.refreshall(SecurityRule)
        existing = fw.find(name, SecurityRule)
        if existing:
            return f"❌ Error: Security policy rule '{name}' already exists"

        # Create rule object
        rule = SecurityRule(
            name=name,
            fromzone=fromzone,
            tozone=tozone,
            source=source,
            destination=destination,
            service=service,
            action=action,
            description=description,
            tag=tag,
            log_end=log_end,
        )

        # Add to firewall
        fw.add(rule)

        # Create on firewall
        def create_op():
            rule.create()

        with_retry(create_op, max_retries=3)

        return f"✅ Created security policy rule: {name}"

    except Exception as e:
        return f"❌ Error: {type(e).__name__}: {e}"


@tool
def security_policy_update(
    name: str,
    fromzone: Optional[list[str]] = None,
    tozone: Optional[list[str]] = None,
    source: Optional[list[str]] = None,
    destination: Optional[list[str]] = None,
    service: Optional[list[str]] = None,
    action: Optional[str] = None,
    description: Optional[str] = None,
    tag: Optional[list[str]] = None,
) -> str:
    """Update an existing security policy rule on PAN-OS firewall.

    Args:
        name: Name of the security policy rule to update
        fromzone: New source zones (optional)
        tozone: New destination zones (optional)
        source: New source addresses (optional)
        destination: New destination addresses (optional)
        service: New services (optional)
        action: New action (optional)
        description: New description (optional)
        tag: New tags (optional)

    Returns:
        Success/failure message

    Example:
        security_policy_update(
            name="allow-web-traffic",
            source=["10.1.1.0/24", "10.2.1.0/24"],
            description="Updated to include 10.2.1.0/24"
        )
    """
    try:
        from panos.policies import SecurityRule

        fw = get_firewall_client()

        # Find existing rule
        fw.refreshall(SecurityRule)
        rule = fw.find(name, SecurityRule)
        if not rule:
            return f"❌ Error: Security policy rule '{name}' not found"

        # Update fields
        updated_fields = []
        if fromzone is not None:
            rule.fromzone = fromzone
            updated_fields.append("fromzone")
        if tozone is not None:
            rule.tozone = tozone
            updated_fields.append("tozone")
        if source is not None:
            rule.source = source
            updated_fields.append("source")
        if destination is not None:
            rule.destination = destination
            updated_fields.append("destination")
        if service is not None:
            rule.service = service
            updated_fields.append("service")
        if action is not None:
            rule.action = action
            updated_fields.append("action")
        if description is not None:
            rule.description = description
            updated_fields.append("description")
        if tag is not None:
            rule.tag = tag
            updated_fields.append("tag")

        if not updated_fields:
            return "❌ Error: No fields provided for update"

        # Apply changes
        def update_op():
            rule.apply()

        with_retry(update_op, max_retries=3)

        return f"✅ Updated security policy rule: {name} (fields: {', '.join(updated_fields)})"

    except Exception as e:
        return f"❌ Error: {type(e).__name__}: {e}"


@tool
def security_policy_delete(name: str) -> str:
    """Delete a security policy rule from PAN-OS firewall.

    Args:
        name: Name of the security policy rule to delete

    Returns:
        Success/failure message

    Example:
        security_policy_delete(name="old-rule")
    """
    try:
        from panos.policies import SecurityRule

        fw = get_firewall_client()

        # Find existing rule
        fw.refreshall(SecurityRule)
        rule = fw.find(name, SecurityRule)
        if not rule:
            return f"❌ Error: Security policy rule '{name}' not found"

        # Delete rule
        def delete_op():
            rule.delete()

        with_retry(delete_op, max_retries=3)

        return f"✅ Deleted security policy rule: {name}"

    except Exception as e:
        return f"❌ Error: {type(e).__name__}: {e}"


# Export all tools
SECURITY_POLICY_TOOLS = [
    security_policy_list,
    security_policy_read,
    security_policy_create,
    security_policy_update,
    security_policy_delete,
]
