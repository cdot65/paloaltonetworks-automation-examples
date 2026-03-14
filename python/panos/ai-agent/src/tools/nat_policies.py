"""NAT policy tools for PAN-OS.

Basic CRUD operations for NAT policy rule management.
"""

from typing import Optional

from langchain_core.tools import tool
from src.core.client import get_firewall_client
from src.core.retry_helper import with_retry


@tool
def nat_policy_list() -> str:
    """List all NAT policy rules on PAN-OS firewall.

    Returns:
        List of NAT policy rules or error message

    Example:
        nat_policy_list()
    """
    try:
        from panos.policies import NatRule

        fw = get_firewall_client()
        fw.refreshall(NatRule)
        rules = fw.findall(NatRule)

        if not rules:
            return "✅ No NAT policy rules found"

        rule_list = [{"name": rule.name, "nat_type": rule.nat_type} for rule in rules]

        return f"✅ Found {len(rule_list)} NAT policy rules:\n" + "\n".join(
            [f"- {r['name']} (type: {r['nat_type']})" for r in rule_list]
        )

    except Exception as e:
        return f"❌ Error: {type(e).__name__}: {e}"


@tool
def nat_policy_read(name: str) -> str:
    """Read an existing NAT policy rule from PAN-OS firewall.

    Args:
        name: Name of the NAT policy rule to retrieve

    Returns:
        NAT policy rule details or error message

    Example:
        nat_policy_read(name="outbound-nat")
    """
    try:
        from panos.policies import NatRule

        fw = get_firewall_client()
        fw.refreshall(NatRule)
        rule = fw.find(name, NatRule)

        if not rule:
            return f"❌ Error: NAT policy rule '{name}' not found"

        return (
            f"✅ Retrieved NAT policy rule: {name}\n"
            f"NAT Type: {rule.nat_type}\n"
            f"From zone: {rule.fromzone}\n"
            f"To zone: {rule.tozone}"
        )

    except Exception as e:
        return f"❌ Error: {type(e).__name__}: {e}"


@tool
def nat_policy_create_source(
    name: str,
    fromzone: list[str],
    tozone: list[str],
    source: list[str],
    destination: list[str],
    service: str = "any",
    source_translation_type: str = "dynamic-ip-and-port",
    source_translation_address_type: str = "interface-address",
    source_translation_interface: Optional[str] = None,
    description: Optional[str] = None,
    tag: Optional[list[str]] = None,
) -> str:
    """Create a new source NAT policy rule on PAN-OS firewall.

    Args:
        name: Name of the NAT policy rule
        fromzone: List of source zones (e.g., ["trust"])
        tozone: List of destination zones (e.g., ["untrust"])
        source: List of source addresses (e.g., ["10.1.1.0/24"])
        destination: List of destination addresses (e.g., ["any"])
        service: Service (default: "any")
        source_translation_type: Type of source translation (default: "dynamic-ip-and-port")
        source_translation_address_type: Address type (default: "interface-address")
        source_translation_interface: Interface for NAT (e.g., "ethernet1/1")
        description: Optional description
        tag: Optional list of tags

    Returns:
        Success/failure message

    Example:
        nat_policy_create_source(
            name="outbound-nat",
            fromzone=["trust"],
            tozone=["untrust"],
            source=["10.1.1.0/24"],
            destination=["any"],
            source_translation_interface="ethernet1/1",
            description="Outbound NAT for internal network"
        )
    """
    try:
        from panos.policies import NatRule

        fw = get_firewall_client()

        # Check if rule already exists
        fw.refreshall(NatRule)
        existing = fw.find(name, NatRule)
        if existing:
            return f"❌ Error: NAT policy rule '{name}' already exists"

        # Create rule object
        rule = NatRule(
            name=name,
            fromzone=fromzone,
            tozone=tozone,
            source=source,
            destination=destination,
            service=service,
            nat_type="ipv4",
            source_translation_type=source_translation_type,
            source_translation_address_type=source_translation_address_type,
            source_translation_interface=source_translation_interface,
            description=description,
            tag=tag,
        )

        # Add to firewall
        fw.add(rule)

        # Create on firewall
        def create_op():
            rule.create()

        with_retry(create_op, max_retries=3)

        return f"✅ Created source NAT policy rule: {name}"

    except Exception as e:
        return f"❌ Error: {type(e).__name__}: {e}"


@tool
def nat_policy_delete(name: str) -> str:
    """Delete a NAT policy rule from PAN-OS firewall.

    Args:
        name: Name of the NAT policy rule to delete

    Returns:
        Success/failure message

    Example:
        nat_policy_delete(name="old-nat-rule")
    """
    try:
        from panos.policies import NatRule

        fw = get_firewall_client()

        # Find existing rule
        fw.refreshall(NatRule)
        rule = fw.find(name, NatRule)
        if not rule:
            return f"❌ Error: NAT policy rule '{name}' not found"

        # Delete rule
        def delete_op():
            rule.delete()

        with_retry(delete_op, max_retries=3)

        return f"✅ Deleted NAT policy rule: {name}"

    except Exception as e:
        return f"❌ Error: {type(e).__name__}: {e}"


# Export all tools
NAT_POLICY_TOOLS = [
    nat_policy_list,
    nat_policy_read,
    nat_policy_create_source,
    nat_policy_delete,
]
