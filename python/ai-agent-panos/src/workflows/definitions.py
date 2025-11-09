"""Predefined workflow definitions for deterministic mode.

Workflows are step-by-step automation sequences similar to Ansible playbooks.
Each step can be:
- tool_call: Execute a tool with parameters
- approval: Request human approval before continuing
- conditional: LLM-based routing decision
"""

# Workflow definition structure:
# {
#     "name": "Workflow name",
#     "description": "What this workflow does",
#     "steps": [
#         {
#             "name": "Step name",
#             "type": "tool_call" | "approval" | "conditional",
#             "tool": "tool_name",  # for tool_call
#             "params": {...},       # for tool_call
#             "message": "...",      # for approval
#         }
#     ]
# }

WORKFLOWS = {
    "simple_address": {
        "name": "Simple Address Creation",
        "description": "Create a single address object with validation",
        "steps": [
            {
                "name": "Create address object",
                "type": "tool_call",
                "tool": "address_create",
                "params": {
                    "name": "demo-server",
                    "value": "10.1.1.100",
                    "description": "Demo server created by workflow",
                },
            },
            {
                "name": "Verify address object",
                "type": "tool_call",
                "tool": "address_read",
                "params": {
                    "name": "demo-server",
                },
            },
        ],
    },
    "address_with_approval": {
        "name": "Address Creation with Approval",
        "description": "Create address object with human approval gate",
        "steps": [
            {
                "name": "Create address object",
                "type": "tool_call",
                "tool": "address_create",
                "params": {
                    "name": "approved-server",
                    "value": "10.2.1.100",
                    "description": "Server requiring approval",
                },
            },
            {
                "name": "Request approval for verification",
                "type": "approval",
                "message": "Address object created. Approve to verify?",
            },
            {
                "name": "Verify address object",
                "type": "tool_call",
                "tool": "address_read",
                "params": {
                    "name": "approved-server",
                },
            },
        ],
    },
    "web_server_setup": {
        "name": "Web Server Setup",
        "description": "Create address and service objects for a web server",
        "steps": [
            {
                "name": "Create web server address",
                "type": "tool_call",
                "tool": "address_create",
                "params": {
                    "name": "web-server-1",
                    "value": "10.10.1.100",
                    "description": "Web server primary",
                    "mode": "skip_if_exists",
                },
            },
            {
                "name": "Create HTTP service",
                "type": "tool_call",
                "tool": "service_create",
                "params": {
                    "name": "custom-http",
                    "protocol": "tcp",
                    "port": "8080",
                    "description": "Custom HTTP port",
                    "mode": "skip_if_exists",
                },
            },
            {
                "name": "Create HTTPS service",
                "type": "tool_call",
                "tool": "service_create",
                "params": {
                    "name": "custom-https",
                    "protocol": "tcp",
                    "port": "8443",
                    "description": "Custom HTTPS port",
                    "mode": "skip_if_exists",
                },
            },
            {
                "name": "Create service group",
                "type": "tool_call",
                "tool": "service_group_create",
                "params": {
                    "name": "web-services",
                    "members": ["custom-http", "custom-https"],
                    "mode": "skip_if_exists",
                },
            },
            {
                "name": "List all services",
                "type": "tool_call",
                "tool": "service_list",
                "params": {},
            },
        ],
    },
    "multi_address_creation": {
        "name": "Multiple Address Creation",
        "description": "Create multiple address objects in sequence",
        "steps": [
            {
                "name": "Create DB server address",
                "type": "tool_call",
                "tool": "address_create",
                "params": {
                    "name": "db-server-1",
                    "value": "10.20.1.10",
                    "description": "Database server 1",
                    "tag": ["Database"],
                },
            },
            {
                "name": "Create DB server 2 address",
                "type": "tool_call",
                "tool": "address_create",
                "params": {
                    "name": "db-server-2",
                    "value": "10.20.1.11",
                    "description": "Database server 2",
                    "tag": ["Database"],
                },
            },
            {
                "name": "Create DB server group",
                "type": "tool_call",
                "tool": "address_group_create",
                "params": {
                    "name": "db-servers",
                    "static_members": ["db-server-1", "db-server-2"],
                    "description": "Database server group",
                },
            },
            {
                "name": "Approval before verification",
                "type": "approval",
                "message": "All objects created. Approve to verify?",
            },
            {
                "name": "Verify address group",
                "type": "tool_call",
                "tool": "address_group_read",
                "params": {
                    "name": "db-servers",
                },
            },
        ],
    },
    "network_segmentation": {
        "name": "Network Segmentation Setup",
        "description": "Create addresses and groups for network segmentation",
        "steps": [
            {
                "name": "Create DMZ subnet address",
                "type": "tool_call",
                "tool": "address_create",
                "params": {
                    "name": "dmz-subnet",
                    "value": "10.100.0.0/24",
                    "description": "DMZ network segment",
                    "tag": ["DMZ"],
                },
            },
            {
                "name": "Create internal subnet address",
                "type": "tool_call",
                "tool": "address_create",
                "params": {
                    "name": "internal-subnet",
                    "value": "10.200.0.0/24",
                    "description": "Internal network segment",
                    "tag": ["Internal"],
                },
            },
            {
                "name": "Create VPN subnet address",
                "type": "tool_call",
                "tool": "address_create",
                "params": {
                    "name": "vpn-subnet",
                    "value": "10.50.0.0/24",
                    "description": "VPN network segment",
                    "tag": ["VPN"],
                },
            },
            {
                "name": "Create trusted networks group",
                "type": "tool_call",
                "tool": "address_group_create",
                "params": {
                    "name": "trusted-networks",
                    "static_members": ["internal-subnet", "vpn-subnet"],
                    "description": "Trusted network segments",
                },
            },
            {
                "name": "Request approval for review",
                "type": "approval",
                "message": "Network segmentation complete. Review configuration?",
            },
            {
                "name": "List all address objects",
                "type": "tool_call",
                "tool": "address_list",
                "params": {},
            },
            {
                "name": "List all address groups",
                "type": "tool_call",
                "tool": "address_group_list",
                "params": {},
            },
        ],
    },
    "security_rule_complete": {
        "name": "Complete Security Rule Setup",
        "description": "End-to-end security rule creation with all dependencies and approval gates",
        "steps": [
            {
                "name": "Create source address object",
                "type": "tool_call",
                "tool": "address_create",
                "params": {
                    "name": "app-server-subnet",
                    "value": "10.10.10.0/24",
                    "description": "Application server subnet",
                    "tag": ["AppTier"],
                },
            },
            {
                "name": "Create destination address object",
                "type": "tool_call",
                "tool": "address_create",
                "params": {
                    "name": "db-server-subnet",
                    "value": "10.20.20.0/24",
                    "description": "Database server subnet",
                    "tag": ["DBTier"],
                },
            },
            {
                "name": "Create MySQL service",
                "type": "tool_call",
                "tool": "service_create",
                "params": {
                    "name": "mysql-custom",
                    "protocol": "tcp",
                    "port": "3306",
                    "description": "MySQL database service",
                },
            },
            {
                "name": "Create PostgreSQL service",
                "type": "tool_call",
                "tool": "service_create",
                "params": {
                    "name": "postgresql-custom",
                    "protocol": "tcp",
                    "port": "5432",
                    "description": "PostgreSQL database service",
                },
            },
            {
                "name": "Create database services group",
                "type": "tool_call",
                "tool": "service_group_create",
                "params": {
                    "name": "database-services",
                    "members": ["mysql-custom", "postgresql-custom"],
                    "description": "All database services",
                },
            },
            {
                "name": "Approval before policy creation",
                "type": "approval",
                "message": "All objects created. Approve to create security policy rule?",
            },
            {
                "name": "Verify all objects created",
                "type": "tool_call",
                "tool": "address_list",
                "params": {},
            },
            {
                "name": "Review service group",
                "type": "tool_call",
                "tool": "service_group_read",
                "params": {
                    "name": "database-services",
                },
            },
        ],
    },
    "complete_security_workflow": {
        "name": "Complete Security Policy Workflow with Commit",
        "description": "End-to-end: create objects, create policy, commit changes",
        "steps": [
            {
                "name": "Create first source address",
                "type": "tool_call",
                "tool": "address_create",
                "params": {
                    "name": "internal-net-1",
                    "value": "192.168.1.0/24",
                    "description": "Internal network 1",
                },
            },
            {
                "name": "Create second source address",
                "type": "tool_call",
                "tool": "address_create",
                "params": {
                    "name": "internal-net-2",
                    "value": "192.168.2.0/24",
                    "description": "Internal network 2",
                },
            },
            {
                "name": "Create destination address",
                "type": "tool_call",
                "tool": "address_create",
                "params": {
                    "name": "internet-any",
                    "value": "0.0.0.0/0",
                    "description": "Internet (any)",
                },
            },
            {
                "name": "Create security policy",
                "type": "tool_call",
                "tool": "security_policy_create",
                "params": {
                    "name": "allow-internet-access",
                    "fromzone": ["trust"],
                    "tozone": ["untrust"],
                    "source": ["internal-net-1", "internal-net-2"],
                    "destination": ["any"],
                    "service": ["application-default"],
                    "action": "allow",
                    "description": "Allow internal networks to access internet",
                },
            },
            {
                "name": "Request approval for commit",
                "type": "approval",
                "message": "All objects and policies created. Approve commit to firewall?",
            },
            {
                "name": "Commit changes",
                "type": "tool_call",
                "tool": "commit_changes",
                "params": {
                    "description": "Security policy workflow - allow internet access",
                    "sync": True,
                },
            },
        ],
    },
}


def get_workflow(name: str) -> dict | None:
    """Get workflow definition by name.

    Args:
        name: Workflow name

    Returns:
        Workflow definition dict or None if not found
    """
    return WORKFLOWS.get(name)


def list_workflows() -> list[str]:
    """List all available workflow names.

    Returns:
        List of workflow names
    """
    return list(WORKFLOWS.keys())


def get_workflow_description(name: str) -> str | None:
    """Get workflow description.

    Args:
        name: Workflow name

    Returns:
        Workflow description or None if not found
    """
    workflow = WORKFLOWS.get(name)
    return workflow.get("description") if workflow else None
