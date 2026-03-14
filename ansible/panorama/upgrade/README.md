# Upgrading PAN-OS Firewall Software via Panorama with Ansible

## Overview

This project automates the process of upgrading PAN-OS software on a firewall managed by Panorama. It uses the `paloaltonetworks.panos` collection's `panos_software` module to download, install, and restart a firewall through Panorama by specifying the firewall's serial number. The playbook handles the entire upgrade lifecycle in a single task -- downloading the target software version, installing it, and triggering a restart. The serial number and target version are defined as playbook variables and can be overridden at the command line.

## Prerequisites

- Python 3.6 or later
- Ansible 2.10 or later
- The `paloaltonetworks.panos` collection installed
- The `pan-os-python` Python library installed
- Network access to your Panorama appliance on HTTPS (TCP/443)
- Valid Panorama credentials (username and password) with permissions to manage firewall software
- The target firewall must be connected to and managed by the Panorama instance
- The target PAN-OS version must be available for download

## Quickstart

1. Clone the repository and navigate to this project:

   ```bash
   git clone https://github.com/cdot65/paloaltonetworks-automation-examples.git
   cd paloaltonetworks-automation-examples/ansible/panorama/upgrade
   ```

2. Create and activate a Python virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install Ansible and the required collection:

   ```bash
   pip install ansible pan-os-python
   ansible-galaxy collection install paloaltonetworks.panos
   ```

4. Edit `inventory.yaml` with your Panorama host and update `group_vars/all/credentials.yaml` with your credentials (see Configuration below).

5. Run the playbook:

   ```bash
   ansible-playbook playbook.yaml
   ```

## Configuration

### Inventory

The inventory file `inventory.yaml` defines the Panorama host:

```yaml
all:
  children:
    panorama:
      hosts:
        panorama.example.com:
          ansible_host: 192.168.1.1
```

Replace `192.168.1.1` with the IP address or FQDN of your Panorama appliance. The `ansible_host` variable tells Ansible the actual network address to connect to.

### Credentials

Store your credentials in `group_vars/all/credentials.yaml`:

```yaml
---
panorama_credentials:
  username: "your-username-here"
  password: "your-password-here"
```

To encrypt this file with Ansible Vault:

```bash
ansible-vault encrypt group_vars/all/credentials.yaml
```

You will then need to pass `--ask-vault-pass` when running the playbook.

### Variables

| Variable | Location | Required | Description |
|---|---|---|---|
| `panorama_credentials.username` | `group_vars/all/credentials.yaml` | Yes | Username for Panorama API authentication |
| `panorama_credentials.password` | `group_vars/all/credentials.yaml` | Yes | Password for Panorama API authentication |
| `serial_number` | `playbook.yaml` (vars section) | Yes | Serial number of the firewall to upgrade |
| `software_version` | `playbook.yaml` (vars section) | Yes | Target PAN-OS version (e.g., `11.0.2-h1`) |
| `ansible_host` | `inventory.yaml` | Yes | IP address or FQDN of the Panorama appliance |

## Usage

**Basic run:**

```bash
ansible-playbook playbook.yaml
```

**Upgrade a specific firewall to a specific version:**

```bash
ansible-playbook playbook.yaml -e "serial_number=012345678901234 software_version=11.1.0"
```

**Dry run (check mode):**

```bash
ansible-playbook playbook.yaml --check
```

Check mode simulates the playbook run without making any changes. The `panos_software` module will report what it would do without actually downloading, installing, or restarting the firewall. This is strongly recommended before running an actual upgrade.

**Verbose debugging output:**

```bash
ansible-playbook playbook.yaml -vvv
```

### Expected Output

A successful run will produce output similar to:

```
PLAY [Upgrade a firewall] ******************************************************

TASK [Install Software] ********************************************************
changed: [panorama.example.com]

PLAY RECAP *********************************************************************
panorama.example.com       : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

The `changed=1` indicates the software was downloaded, installed, and a restart was triggered. The firewall will reboot after the upgrade is installed. Allow several minutes for the device to come back online.

## Project Structure

```
upgrade/
├── ansible.cfg                  # Ansible configuration (inventory path, timeouts, logging)
├── group_vars/
│   └── all/
│       └── panorama.yaml        # Panorama credentials (rename to credentials.yaml recommended)
├── inventory.yaml               # Target Panorama host definition
├── playbook.yaml                # Main playbook that upgrades a firewall via Panorama
└── README.md                    # This file
```

## Troubleshooting

| Problem | Possible Cause | Solution |
|---|---|---|
| Connection refused | Panorama is unreachable or HTTPS is not enabled | Verify network connectivity and that the management interface is listening on port 443 |
| Invalid credentials / 403 error | Username or password is incorrect | Verify credentials in `group_vars/all/credentials.yaml` |
| Module not found: `paloaltonetworks.panos.panos_software` | The `paloaltonetworks.panos` collection is not installed | Run `ansible-galaxy collection install paloaltonetworks.panos` |
| Timeout during upgrade | Software download or install is taking longer than expected | Increase the `timeout` value in `ansible.cfg` (currently set to 240 seconds) |
| "Software version not found" | The specified PAN-OS version is not available | Verify the version string is correct and the image is available on the Palo Alto Networks update server |
| Firewall not found by serial number | Serial number does not match any firewall managed by Panorama | Verify the serial number and confirm the firewall is connected to Panorama |

## Ansible Concepts Used

- **Playbook**: A YAML file that defines a set of tasks to be executed on target hosts. `playbook.yaml` is the main entry point for this project.
- **Inventory**: A file (`inventory.yaml`) that lists the hosts Ansible will manage. Hosts are organized into groups such as `panorama`.
- **Module**: A unit of work in Ansible. This project uses `paloaltonetworks.panos.panos_software` to manage PAN-OS software upgrades including download, install, and restart.
- **Collection**: A packaged set of modules, roles, and plugins. The `paloaltonetworks.panos` collection provides all PAN-OS modules used here.
- **Group Variables (group_vars)**: Variables stored in the `group_vars/` directory that apply to all hosts in a group. Credentials are stored here to keep them out of the playbook.
- **Vault**: Ansible Vault lets you encrypt sensitive files like credential files so secrets are not stored in plain text.
- **Check Mode**: Running a playbook with `--check` simulates execution without making changes. Especially important for upgrade operations to verify what would happen before committing to a software upgrade and device restart.
