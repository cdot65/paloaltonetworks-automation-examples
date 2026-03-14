# Ansible Examples

27 Ansible playbooks and supporting projects for automating Palo Alto Networks firewalls, Panorama, vCenter deployments, event-driven automation, and custom execution environments.

## Project Categories

| Category | Count | Description |
|----------|-------|-------------|
| [PAN-OS Playbooks](panos.md) | 11 | Firewall configuration, VPN, security policies, log retrieval |
| [Panorama Playbooks](panorama.md) | 6 | Centralized management, upgrades, dynamic inventory |
| [vCenter Deployment](vcenter.md) | 1 | VM-Series firewall cloning on vSphere |
| [Event-Driven Ansible](event-driven.md) | 1 | Log-triggered remediation with EDA |
| [Execution Environments](execution-environments.md) | 3 | Container images for consistent automation |

## Common Prerequisites

- Python 3.11+ with Ansible installed
- `paloaltonetworks.panos` collection (`ansible-galaxy collection install paloaltonetworks.panos`)
- PAN-OS firewall or Panorama with API/admin access

## Key Patterns

All Ansible projects in this repository follow these conventions:

- **Credentials** are externalized in `group_vars/` or `host_vars/` -- never inline in playbooks
- **Ansible Vault** is recommended for encrypting sensitive variable files
- **Check mode** (`--check`) is documented for dry-run validation before real execution
- **Expected output** includes `PLAY RECAP` blocks showing success/failure status
