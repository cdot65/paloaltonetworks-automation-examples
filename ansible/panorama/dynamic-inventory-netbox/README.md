# Dynamic Inventory from NetBox for Palo Alto Networks Devices

## Overview

This project provides a dynamic inventory configuration that pulls device information from a NetBox instance for use with Ansible. Instead of manually maintaining a static inventory file, the `netbox.netbox.nb_inventory` plugin queries the NetBox API to automatically discover hosts and organize them into groups based on device roles, platforms, device types, tenants, sites, racks, and tags. Custom fields are flattened into host variables, and config context and interface data are included per device, making the inventory immediately usable with PAN-OS automation playbooks.

## Prerequisites

- Python 3.6 or later
- Ansible 2.10 or later
- The `netbox.netbox` collection installed
- The `pynetbox` Python library installed
- A running NetBox instance with devices configured
- A NetBox API token with read access to devices and interfaces

## Quickstart

1. Clone the repository and navigate to this project:

   ```bash
   git clone https://github.com/cdot65/paloaltonetworks-automation-examples.git
   cd paloaltonetworks-automation-examples/ansible/panorama/dynamic-inventory-netbox
   ```

2. Create and activate a Python virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install Ansible, the required collection, and Python dependency:

   ```bash
   pip install ansible pynetbox
   ansible-galaxy collection install netbox.netbox
   ```

4. Edit `inventory.yaml` to set your NetBox API endpoint and token (see Configuration below).

5. Test the dynamic inventory:

   ```bash
   ansible-inventory -i inventory.yaml --list
   ```

## Configuration

### Inventory

The inventory file `inventory.yaml` configures the NetBox dynamic inventory plugin:

```yaml
plugin: "netbox.netbox.nb_inventory"
api_endpoint: "https://netbox.example.com"
token: "your-netbox-api-token-here"
validate_certs: false
config_context: true
interfaces: true
group_names_raw: true
group_by:
  - device_roles
  - platforms
  - device_types
  - tenants
  - sites
  - racks
  - tags
query_filters: []
device_query_filters:
  - has_primary_ip: "true"
flatten_custom_fields: true
```

- `api_endpoint`: The URL of your NetBox instance.
- `token`: Your NetBox API token for authentication.
- `group_by`: Controls how devices are grouped in the inventory. Each entry creates host groups based on that NetBox attribute.
- `device_query_filters`: Only devices with a primary IP assigned are included in the inventory.
- `config_context`: When `true`, NetBox config context data is included as host variables.
- `interfaces`: When `true`, interface data is included for each device.
- `flatten_custom_fields`: When `true`, custom fields are merged directly into host vars rather than nested under a key.

### Credentials

Store your NetBox API token in `group_vars/all/credentials.yaml` to avoid embedding it in the inventory file:

```yaml
---
netbox_api_token: "your-netbox-api-token-here"
```

Then reference it in the inventory file or pass it as an environment variable (`NETBOX_TOKEN`).

To encrypt this file with Ansible Vault:

```bash
ansible-vault encrypt group_vars/all/credentials.yaml
```

### Variables

| Variable | Location | Required | Description |
|---|---|---|---|
| `plugin` | `inventory.yaml` | Yes | Must be `netbox.netbox.nb_inventory` to use the NetBox inventory plugin |
| `api_endpoint` | `inventory.yaml` | Yes | URL of the NetBox instance |
| `token` | `inventory.yaml` | Yes | NetBox API token for authentication |
| `validate_certs` | `inventory.yaml` | No | Whether to validate SSL certificates (default: `true`) |
| `group_by` | `inventory.yaml` | No | List of NetBox attributes to group hosts by |
| `device_query_filters` | `inventory.yaml` | No | Filters to limit which devices are included |
| `config_context` | `inventory.yaml` | No | Include NetBox config context data as host vars |
| `interfaces` | `inventory.yaml` | No | Include interface data for each device |
| `flatten_custom_fields` | `inventory.yaml` | No | Merge custom fields directly into host vars |

## Usage

**List all discovered hosts and groups:**

```bash
ansible-inventory -i inventory.yaml --list
```

**View the inventory as a graph:**

```bash
ansible-inventory -i inventory.yaml --graph
```

**Use this inventory with a playbook:**

```bash
ansible-playbook -i inventory.yaml playbook.yaml
```

**Limit to a specific group (e.g., firewalls by device role):**

```bash
ansible-playbook -i inventory.yaml playbook.yaml --limit device_roles_firewall
```

**Dry run (check mode):**

```bash
ansible-playbook -i inventory.yaml playbook.yaml --check
```

Check mode simulates a playbook run without making changes. This is useful for validating that the dynamic inventory is returning the expected hosts before executing tasks against them.

**Override a variable at runtime:**

```bash
ansible-playbook -i inventory.yaml playbook.yaml -e "target_group=firewalls"
```

**Verbose debugging output:**

```bash
ansible-inventory -i inventory.yaml --list -vvv
```

### Expected Output

Running `ansible-inventory -i inventory.yaml --list` will produce JSON output. When used with a playbook targeting the discovered hosts, the PLAY RECAP will look similar to:

```
PLAY [all] *********************************************************************

TASK [Gathering Facts] *********************************************************
ok: [firewall-01.example.com]
ok: [firewall-02.example.com]

TASK [Show hostname] ***********************************************************
ok: [firewall-01.example.com]
ok: [firewall-02.example.com]

PLAY RECAP *********************************************************************
firewall-01.example.com    : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
firewall-02.example.com    : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

The actual hostnames will depend on the devices registered in your NetBox instance.

## Project Structure

```
dynamic-inventory-netbox/
├── inventory.yaml               # NetBox dynamic inventory plugin configuration
└── README.md                    # This file
```

## Troubleshooting

| Problem | Possible Cause | Solution |
|---|---|---|
| Connection refused | NetBox instance is unreachable | Verify network connectivity and that the `api_endpoint` URL is correct |
| Invalid credentials / 403 error | NetBox API token is incorrect or lacks permissions | Generate a new API token in NetBox with device read permissions |
| Module not found: `netbox.netbox.nb_inventory` | The `netbox.netbox` collection is not installed | Run `ansible-galaxy collection install netbox.netbox` |
| Timeout when fetching inventory | NetBox has many devices or slow network | Add more specific `device_query_filters` to limit results |
| No hosts returned | Devices in NetBox do not have a primary IP assigned | Ensure devices have a primary IP set, or remove the `has_primary_ip` filter |
| `pynetbox` import error | The `pynetbox` Python library is not installed | Run `pip install pynetbox` |

## Ansible Concepts Used

- **Inventory**: A file that tells Ansible which hosts to manage. This project uses a dynamic inventory plugin instead of a static list of hosts.
- **Dynamic Inventory Plugin**: A plugin that generates inventory at runtime by querying an external source. The `netbox.netbox.nb_inventory` plugin queries NetBox for device data and automatically creates host groups.
- **Collection**: A packaged set of modules, roles, and plugins. The `netbox.netbox` collection provides the inventory plugin used here.
- **Group Variables (group_vars)**: Variables stored in the `group_vars/` directory that apply to all hosts in a group. Can be used to store the NetBox API token separately from the inventory file.
- **Vault**: Ansible Vault lets you encrypt sensitive files like credential files so secrets are not stored in plain text.
- **Check Mode**: Running a playbook with `--check` simulates execution without making changes, useful for validating that the dynamic inventory returns expected hosts before running tasks.
