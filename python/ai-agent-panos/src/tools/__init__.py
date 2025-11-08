"""PAN-OS agent tools.

Exports all tools for use in autonomous and deterministic graphs.
"""

from src.tools.address_groups import ADDRESS_GROUP_TOOLS
from src.tools.address_objects import ADDRESS_TOOLS
from src.tools.nat_policies import NAT_POLICY_TOOLS
from src.tools.orchestration.commit_operations import commit_changes
from src.tools.orchestration.crud_operations import crud_operation
from src.tools.security_policies import SECURITY_POLICY_TOOLS
from src.tools.service_groups import SERVICE_GROUP_TOOLS
from src.tools.services import SERVICE_TOOLS

# All tools combined for autonomous agent
ALL_TOOLS = [
    # Object CRUD tools (22 tools)
    *ADDRESS_TOOLS,  # 5 tools
    *ADDRESS_GROUP_TOOLS,  # 5 tools
    *SERVICE_TOOLS,  # 5 tools
    *SERVICE_GROUP_TOOLS,  # 5 tools
    # Policy tools (9 tools)
    *SECURITY_POLICY_TOOLS,  # 5 tools
    *NAT_POLICY_TOOLS,  # 4 tools
    # Orchestration tools (2 tools)
    crud_operation,  # Unified CRUD
    commit_changes,  # Commit workflow
]

__all__ = [
    "ALL_TOOLS",
    "ADDRESS_TOOLS",
    "ADDRESS_GROUP_TOOLS",
    "SERVICE_TOOLS",
    "SERVICE_GROUP_TOOLS",
    "SECURITY_POLICY_TOOLS",
    "NAT_POLICY_TOOLS",
    "crud_operation",
    "commit_changes",
]
