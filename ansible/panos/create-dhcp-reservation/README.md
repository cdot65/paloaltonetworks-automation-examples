# Create DHCP Reservations on Panorama-Managed Firewalls

## Overview

This project demonstrates two approaches to creating DHCP server reservations on Palo Alto Networks firewalls managed through Panorama. Both approaches push reserved address entries into a Panorama template's DHCP server configuration via the XML API. Approach 1 uses the `paloaltonetworks.panos` collection's `panos_config_element` module with XPath-based configuration. Approach 2 achieves the same result using only Ansible's built-in `uri` module to make direct REST API calls. Each approach loops over a list of reservations containing IP addresses, MAC addresses, descriptions, and interface assignments.

## Prerequisites

- Python 3.8+
- Ansible Core 2.10+
- Panorama with API access enabled
- A valid Panorama API key
- For Approach 1: `paloaltonetworks.panos` Ansible collection and `pan-os-python` Python library

## Quickstart

1. Clone the repository and navigate to the project directory:

   ```bash
   git clone https://github.com/cdot65/paloaltonetworks-automation-examples.git
   cd paloaltonetworks-automation-examples/ansible/panos/create-dhcp-reservation
   ```

2. Create and activate a Python virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install Ansible and dependencies:

   ```bash
   pip install ansible pan-os-python
   ```

4. Install the PAN-OS collection (needed for Approach 1):

   ```bash
   ansible-galaxy collection install paloaltonetworks.panos
   ```

5. Update credentials and inventory in your chosen approach directory (see Configuration below).

6. Run the playbook:

   ```bash
   cd 1-panos-ansible-collection
   ansible-playbook playbook.yaml
   ```

## Configuration

### Inventory

Both approaches use the same inventory format. Edit `inventory.yaml` in the chosen approach directory:

```yaml
all:
  children:
    panorama:
      hosts:
        panorama.example.com:
```

Replace `panorama.example.com` with your Panorama's FQDN or IP address. The hostname becomes the `ansible_host` value used for API connections.

### Credentials

**Approach 1** -- edit `1-panos-ansible-collection/group_vars/all/credentials.yaml`:

```yaml
panorama_api_key: "your-panorama-api-key-here"
```

**Approach 2** -- edit `2-ansible-builtin-modules/group_vars/all/credentials.yaml`:

```yaml
panorama_api_key: "your-panorama-api-key-here"
```

Encrypt either file with Ansible Vault:

```bash
ansible-vault encrypt group_vars/all/credentials.yaml
```

### Variables

| Variable | Location | Required | Description |
|----------|----------|----------|-------------|
| `panorama_api_key` / `firewall_api_key` | `group_vars/all/credentials.yaml` | Yes | Panorama API key for authentication |
| `dhcp_reservations` | `group_vars/all/dhcp.yaml` (Approach 1) | Yes | List of DHCP reservations with `ip_address`, `mac`, `description`, `interface`, `template` |
| `interface` | `playbook.yaml` vars (Approach 2) | Yes | Target DHCP interface (e.g., `ethernet1/2`) |
| `template` | `playbook.yaml` vars (Approach 2) | Yes | Panorama template name (e.g., `BaseTemplate`) |
| `ansible_python_interpreter` | `group_vars/all/python.yaml` | No | Python interpreter override to prevent path issues |

## Usage

### Basic Run (Approach 1 -- PAN-OS Collection)

```bash
cd 1-panos-ansible-collection
ansible-playbook playbook.yaml
```

### Basic Run (Approach 2 -- Built-in URI Module)

```bash
cd 2-ansible-builtin-modules
ansible-playbook playbook.yaml
```

### Dry Run

```bash
ansible-playbook playbook.yaml --check
```

Check mode simulates the playbook run without pushing any configuration to Panorama. The `panos_config_element` and `uri` module tasks will report what they would do without making actual API calls.

### Variable Override

Override the Panorama template name at runtime:

```bash
ansible-playbook playbook.yaml -e "template=NewTemplateName"
```

### Verbose Debugging

```bash
ansible-playbook playbook.yaml -vvv
```

### Expected Output

```
PLAY [panorama] ****************************************************************

TASK [DHCP reservations] *******************************************************
changed: [panorama.example.com] => (item={'ip_address': '192.168.101.20', 'mac': '00:50:56:11:20:44', 'description': 'server20', 'interface': 'ethernet1/2', 'template': 'BranchFirewalls'})
changed: [panorama.example.com] => (item={'ip_address': '192.168.101.21', 'mac': '00:50:56:11:21:44', 'description': 'server21', 'interface': 'ethernet1/2', 'template': 'BranchFirewalls'})
changed: [panorama.example.com] => (item={'ip_address': '192.168.101.22', 'mac': '00:50:56:11:22:44', 'description': 'server22', 'interface': 'ethernet1/3', 'template': 'BranchFirewalls'})
changed: [panorama.example.com] => (item={'ip_address': '192.168.101.22', 'mac': '00:50:56:11:23:44', 'description': 'server23', 'interface': 'ethernet1/4', 'template': 'BranchFirewalls'})

PLAY RECAP *********************************************************************
panorama.example.com       : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

- `ok=1` -- the looped task completed for all items.
- `changed=1` -- DHCP reservations were created or updated on Panorama.
- `failed=0` -- no errors. If Panorama rejects the API call, this counter increments.

## Project Structure

```
create-dhcp-reservation/
├── 1-panos-ansible-collection/
│   ├── ansible.cfg                          # Ansible settings
│   ├── inventory.yaml                       # Panorama host
│   ├── playbook.yaml                        # Uses panos_config_element module with loop
│   └── group_vars/
│       └── all/
│           ├── auth.yaml                    # API key (rename to credentials.yaml)
│           ├── dhcp.yaml                    # DHCP reservation list
│           └── python.yaml                  # Python interpreter override
├── 2-ansible-builtin-modules/
│   ├── ansible.cfg                          # Ansible settings
│   ├── inventory.yaml                       # Panorama host
│   ├── playbook.yaml                        # Uses ansible.builtin.uri with direct API calls
│   └── group_vars/
│       └── all/
│           └── auth.yaml                    # API key (rename to credentials.yaml)
└── README.md
```

## Troubleshooting

| Problem | Possible Cause | Solution |
|---------|---------------|----------|
| Connection refused to Panorama | Panorama management interface unreachable | Verify network connectivity and that HTTPS API access is enabled |
| Invalid credentials / HTTP 403 | Wrong or expired API key | Generate a new API key: `curl -k 'https://PANORAMA/api/?type=keygen&user=admin&password=PASSWORD'` |
| Module not found: `paloaltonetworks.panos.panos_config_element` | PAN-OS collection not installed | Run `ansible-galaxy collection install paloaltonetworks.panos` |
| Timeout during API call | Panorama under heavy load or network latency | Increase `timeout` in `ansible.cfg` (default: 240 seconds) |
| Template not found error from Panorama | Incorrect `template` variable value | Verify the template name in Panorama matches the value in `dhcp.yaml` or playbook vars exactly |
| SSL certificate verification error | Self-signed certificate on Panorama | Add `validate_certs: no` to the module or set up proper CA trust |

## Ansible Concepts Used

- **Playbook**: A YAML file that defines tasks to run against hosts. Each approach has its own `playbook.yaml` targeting the `panorama` host group.

- **Inventory**: A file listing hosts and groups. The `panorama` group contains the Panorama management appliance hostname.

- **Module**: A unit of code Ansible executes. Approach 1 uses `paloaltonetworks.panos.panos_config_element` (XPath-based config push). Approach 2 uses `ansible.builtin.uri` (direct HTTP API calls).

- **Collection**: A distribution format for Ansible content. `paloaltonetworks.panos` provides PAN-OS-specific modules like `panos_config_element`.

- **Group Vars**: Variable files in `group_vars/all/` that apply to every host. Used here for API keys, DHCP reservation data, and Python interpreter settings.

- **Vault**: Ansible Vault encrypts sensitive files (API keys). Run `ansible-vault encrypt group_vars/all/auth.yaml` to protect credentials.

- **Check Mode**: A dry-run mode (`--check`) that previews changes without applying them to Panorama.

- **Loop**: Ansible's `loop` keyword iterates over a list, executing the same task for each item. Both approaches loop over DHCP reservation entries.
