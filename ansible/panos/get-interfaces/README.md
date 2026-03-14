# Retrieve PAN-OS Firewall Interface Information

## Overview

This Ansible playbook runs the `show interface all` operational command on Palo Alto Networks firewalls and displays the results. It uses the `paloaltonetworks.panos` collection's `panos_op` module to send the command via the PAN-OS XML API. The `ansible.utils` collection's `from_xml` filter plugin then converts the XML response into a Python dictionary using `xmltodict`, and the parsed interface data is printed to the console using the `debug` module.

## Prerequisites

- Python 3.8 or later
- Ansible 2.12 or later
- The `paloaltonetworks.panos` Ansible collection
- The `ansible.utils` Ansible collection (provides the `from_xml` filter)
- The `pan-os-python` and `xmltodict` Python libraries
- Username/password access to one or more PAN-OS firewalls

## Quickstart

1. Clone the repository and navigate to this project:

   ```bash
   git clone https://github.com/cdot65/paloaltonetworks-automation-examples.git
   cd paloaltonetworks-automation-examples/ansible/panos/get-interfaces
   ```

2. Create and activate a Python virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install Ansible and required Python packages:

   ```bash
   pip install ansible pan-os-python xmltodict
   ```

4. Install the required Ansible collections:

   ```bash
   ansible-galaxy collection install paloaltonetworks.panos ansible.utils
   ```

5. Update the inventory and credentials (see Configuration below).

6. Run the playbook:

   ```bash
   ansible-playbook playbook.yaml
   ```

## Configuration

### Inventory

Edit `inventory.yaml` to list your PAN-OS firewalls. Each entry under `hosts` is the FQDN or hostname that Ansible uses to identify the device and to connect via the API.

```yaml
all:
  children:
    firewalls:
      hosts:
        fw01.example.com:
        fw02.example.com:
```

Replace the hostnames with the FQDNs or IP addresses of your firewalls. If the hostname does not resolve via DNS, add `ansible_host: 10.0.0.1` beneath it.

### Credentials

Credentials are stored in `group_vars/all/auth.yaml`. Never commit real passwords to version control.

```yaml
---
panos_username: "your-username-here"
panos_password: "your-password-here"
```

Encrypt sensitive files with Ansible Vault:

```bash
ansible-vault encrypt group_vars/all/auth.yaml
```

### Variables

| Variable           | Location                   | Required | Description                                       |
|--------------------|----------------------------|----------|---------------------------------------------------|
| `panos_username`   | `group_vars/all/auth.yaml` | Yes      | Username for PAN-OS API authentication            |
| `panos_password`   | `group_vars/all/auth.yaml` | Yes      | Password for PAN-OS API authentication            |
| `ansible_host`     | `inventory.yaml`           | Yes      | FQDN or IP address of each firewall               |

## Usage

**Basic run:**

```bash
ansible-playbook playbook.yaml
```

**Dry run (check mode):**

```bash
ansible-playbook playbook.yaml --check
```

Check mode simulates the playbook without making changes. Since this playbook only reads data (no configuration changes), check mode will skip the operational command tasks.

**Override variables at runtime:**

```bash
ansible-playbook playbook.yaml -e "panos_username=admin panos_password=secret123"
```

**Verbose debugging:**

```bash
ansible-playbook playbook.yaml -vvv
```

### Expected Output

```
PLAY [firewalls] ***************************************************************

TASK [Run commmand 'show interfaces' on firewalls running PAN-OS.] *************
ok: [fw01.example.com]
ok: [fw02.example.com]

TASK [Convert to Python dictionary with xmltodict] *****************************
ok: [fw01.example.com]
ok: [fw02.example.com]

TASK [Print interface output to the console] ***********************************
ok: [fw01.example.com] => {
    "msg": [
        {"name": "ethernet1/1", "status": "up", ...},
        {"name": "ethernet1/2", "status": "down", ...}
    ]
}
ok: [fw02.example.com] => {
    "msg": [
        {"name": "ethernet1/1", "status": "up", ...}
    ]
}

PLAY RECAP *********************************************************************
fw01.example.com           : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
fw02.example.com           : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

The `ok=3` indicates all three tasks completed successfully. `changed=0` is expected because this playbook only reads data and makes no configuration changes.

## Project Structure

```
get-interfaces/
├── ansible.cfg                    # Ansible configuration (inventory path, timeouts)
├── group_vars/
│   └── all/
│       └── auth.yaml              # Firewall credentials (username/password)
├── inventory.yaml                 # Target firewall host definitions
└── playbook.yaml                  # Main playbook that retrieves and displays interfaces
```

## Troubleshooting

| Problem                        | Possible Cause                                    | Solution                                                               |
|-------------------------------|---------------------------------------------------|------------------------------------------------------------------------|
| Connection refused             | Firewall is unreachable or wrong IP/FQDN          | Verify network connectivity and the host in `inventory.yaml`           |
| Invalid credentials            | Username or password is incorrect                  | Update `group_vars/all/auth.yaml` with correct credentials             |
| Module not found               | `paloaltonetworks.panos` collection not installed  | Run `ansible-galaxy collection install paloaltonetworks.panos`         |
| Timeout                        | Firewall is slow to respond                       | Increase `timeout` in `ansible.cfg`                                    |
| `xmltodict` not found          | Python library not installed                       | Run `pip install xmltodict` in your virtual environment                |
| `from_xml` filter not found    | `ansible.utils` collection not installed           | Run `ansible-galaxy collection install ansible.utils`                  |

## Ansible Concepts Used

- **Playbook**: A YAML file defining tasks to run on targeted hosts. `playbook.yaml` sends an operational command and formats the result.
- **Inventory**: Lists the firewalls to target. `inventory.yaml` groups them under the `firewalls` group.
- **Module**: Reusable units of work. `panos_op` sends operational commands to PAN-OS devices. `set_fact` stores intermediate data. `debug` prints output to the console.
- **Collection**: A packaged set of modules and plugins. `paloaltonetworks.panos` provides PAN-OS modules. `ansible.utils` provides the `from_xml` filter plugin.
- **Filter Plugin**: A plugin that transforms data within Jinja2 expressions. The `from_xml` filter (from `ansible.utils`) converts XML strings into Python dictionaries using the `xmltodict` library.
- **Group Vars**: Variables applied to all hosts in a group. `group_vars/all/auth.yaml` stores shared credentials used by every firewall.
- **Register**: Captures the output of a task into a variable (`result`) so subsequent tasks can access it.
- **Check Mode**: A dry-run mode activated with `--check` that shows what would change without executing tasks.
- **Vault**: An Ansible feature to encrypt sensitive files. Use `ansible-vault encrypt group_vars/all/auth.yaml` to protect credentials at rest.
