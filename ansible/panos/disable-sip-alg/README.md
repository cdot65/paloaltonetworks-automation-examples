# Disable SIP ALG on PAN-OS Firewalls

## Overview

This project disables the SIP Application Layer Gateway (ALG) on Palo Alto Networks firewalls using the `paloaltonetworks.panos` Ansible collection. SIP ALG can interfere with VoIP traffic by modifying SIP headers in transit, causing call setup failures and one-way audio. The playbook uses the `panos_config_element` module to push an XPath-based configuration change that sets `alg-disabled` to `yes` for the SIP application under the shared ALG override path. The change applies to all firewalls in the inventory simultaneously. A manual commit on each firewall is still required after running the playbook.

## Prerequisites

- Python 3.8+
- Ansible Core 2.10+
- `paloaltonetworks.panos` Ansible collection
- `pan-os-python` Python library
- Network access to PAN-OS firewall management interfaces
- Firewall admin credentials with configuration privileges

## Quickstart

1. Clone the repository and navigate to the project directory:

   ```bash
   git clone https://github.com/cdot65/paloaltonetworks-automation-examples.git
   cd paloaltonetworks-automation-examples/ansible/panos/disable-sip-alg
   ```

2. Create and activate a Python virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install Ansible and the PAN-OS Python library:

   ```bash
   pip install ansible pan-os-python
   ```

4. Install the PAN-OS Ansible collection:

   ```bash
   ansible-galaxy collection install paloaltonetworks.panos
   ```

5. Update inventory and credentials (see Configuration below).

6. Run the playbook:

   ```bash
   ansible-playbook playbook.yml --ask-vault-pass
   ```

## Configuration

### Inventory

Edit `inventory.yaml` with your firewall hostnames or IP addresses:

```yaml
all:
  children:
    firewalls:
      hosts:
        firewall-01.example.com:
        firewall-02.example.com:
```

Each hostname becomes the `ansible_host` value used by the `panos_config_element` module for API connections. If DNS does not resolve the hostname, add `ansible_host` explicitly:

```yaml
        firewall-01.example.com:
          ansible_host: 10.0.0.1
```

### Credentials

Create `group_vars/all/credentials.yaml` with your firewall admin credentials:

```yaml
panos_username: "your-firewall-admin-username"
panos_password: "your-firewall-admin-password"
```

Encrypt with Ansible Vault to keep secrets out of version control:

```bash
ansible-vault encrypt group_vars/all/credentials.yaml
```

The playbook's provider block should reference these variables instead of inline values:

```yaml
provider:
  ip_address: "{{ ansible_host }}"
  username: "{{ panos_username }}"
  password: "{{ panos_password }}"
```

### Variables

| Variable | Location | Required | Description |
|----------|----------|----------|-------------|
| `panos_username` | `group_vars/all/credentials.yaml` | Yes | Firewall admin username |
| `panos_password` | `group_vars/all/credentials.yaml` | Yes | Firewall admin password |
| `ansible_python_interpreter` | `group_vars/all/python.yaml` | No | Python interpreter override to prevent path issues |

## Usage

### Basic Run

Disable SIP ALG on all firewalls in the inventory:

```bash
ansible-playbook playbook.yml --ask-vault-pass
```

### Dry Run

```bash
ansible-playbook playbook.yml --check --ask-vault-pass
```

Check mode simulates the playbook run without pushing configuration changes to the firewalls. The `panos_config_element` module reports what it would change without making API calls.

### Variable Override

Target a specific firewall:

```bash
ansible-playbook playbook.yml --limit firewall-01.example.com --ask-vault-pass
```

### Verbose Debugging

```bash
ansible-playbook playbook.yml -vvv --ask-vault-pass
```

### Expected Output

```
PLAY [all] *********************************************************************

TASK [SIP ALG Disable] *********************************************************
changed: [firewall-01.example.com]
changed: [firewall-02.example.com]

PLAY RECAP *********************************************************************
firewall-01.example.com    : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
firewall-02.example.com    : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

- `ok=1` -- the SIP ALG disable task completed on each firewall.
- `changed=1` -- the ALG override configuration was applied. On subsequent runs with the same setting, this becomes `changed=0`.
- `failed=0` -- no errors. If a firewall rejects the API call, this counter increments.

After running, log into each firewall and commit the candidate configuration to activate the change.

## Project Structure

```
disable-sip-alg/
├── ansible.cfg                              # Ansible settings (inventory path, timeouts)
├── inventory.yaml                           # Firewall hosts
├── playbook.yml                             # Single-task playbook to disable SIP ALG
└── group_vars/
    └── all/
        └── python.yaml                      # Python interpreter override
```

## Troubleshooting

| Problem | Possible Cause | Solution |
|---------|---------------|----------|
| Connection refused to firewall | Firewall management interface unreachable | Verify network connectivity and that HTTPS API is enabled |
| Invalid credentials / authentication failure | Wrong username or password | Update `group_vars/all/credentials.yaml` and re-encrypt with Vault |
| Module not found: `paloaltonetworks.panos.panos_config_element` | Collection not installed | Run `ansible-galaxy collection install paloaltonetworks.panos` |
| Timeout during API call | Firewall under heavy load or slow network | Increase `timeout` in `ansible.cfg` (currently 240 seconds) |
| Change not taking effect | Candidate configuration not committed | Log into the firewall and run `commit` after the playbook completes |
| XPath error from firewall | PAN-OS version does not support the ALG override path | Verify your PAN-OS version supports `/config/shared/alg-override/application` |

## Ansible Concepts Used

- **Playbook**: A YAML file defining tasks to run against hosts. `playbook.yml` contains a single task that disables SIP ALG on all inventory hosts.

- **Inventory**: A file listing hosts and groups. The `firewalls` group contains the target PAN-OS firewalls.

- **Module**: A unit of code Ansible executes. `paloaltonetworks.panos.panos_config_element` pushes an XML element to a specific XPath location in the PAN-OS configuration.

- **Collection**: A distribution format for Ansible content. `paloaltonetworks.panos` provides PAN-OS modules including `panos_config_element`.

- **Group Vars**: Variable files in `group_vars/all/` that apply to every host. Used here for Python interpreter settings and (recommended) credentials.

- **Vault**: Ansible Vault encrypts sensitive files (usernames, passwords) at rest. Use `ansible-vault encrypt` and `--ask-vault-pass` at runtime.

- **Check Mode**: A dry-run mode (`--check`) that previews changes without applying them to the firewalls.
