# Finding Firewall Device Group Membership on Panorama with Ansible

## Overview

This project queries a Palo Alto Networks Panorama management server to determine which device group a firewall belongs to, based on its serial number. It uses the `paloaltonetworks.panos` collection to run a `show devicegroups` operational command that retrieves the full device group hierarchy with all connected firewalls. A custom Ansible filter plugin written in Python then searches through the JSON response and returns the matching device group name. This is useful for dynamically resolving device group membership in larger automation workflows.

## Prerequisites

- Python 3.6 or later
- Ansible 2.10 or later
- The `paloaltonetworks.panos` collection installed
- The `pan-os-python` Python library installed
- Network access to your Panorama appliance on HTTPS (TCP/443)
- Valid Panorama credentials (username and password) with read access to device groups

## Quickstart

1. Clone the repository and navigate to this project:

   ```bash
   git clone https://github.com/cdot65/paloaltonetworks-automation-examples.git
   cd paloaltonetworks-automation-examples/ansible/panorama/firewalls-to-device-groups
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
        panorama:
          ansible_host: 192.168.1.1
```

Replace `192.168.1.1` with the IP address or FQDN of your Panorama appliance. The `ansible_host` variable tells Ansible the actual network address to connect to, while the host entry name (`panorama`) is a label used within plays.

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
| `serial_number` | `playbook.yaml` (vars section) | Yes | Serial number of the firewall to look up |
| `ansible_host` | `inventory.yaml` | Yes | IP address or FQDN of the Panorama appliance |

## Usage

**Basic run:**

```bash
ansible-playbook playbook.yaml
```

**Look up a different firewall serial number:**

```bash
ansible-playbook playbook.yaml -e "serial_number=09876543210"
```

**Dry run (check mode):**

```bash
ansible-playbook playbook.yaml --check
```

Check mode simulates the playbook run without making any changes. Since this playbook only reads data (no configuration changes are made), check mode behaves similarly to a normal run, but some tasks may be skipped.

**Verbose debugging output:**

```bash
ansible-playbook playbook.yaml -vvv
```

### Expected Output

A successful run will produce output similar to:

```
PLAY [Pull in Device Groups and Firewall relationships] ************************

TASK [Pull in device group data from Panorama] *********************************
ok: [panorama]

TASK [Use Custom Filter to Find Device Group] **********************************
ok: [panorama]

TASK [Print device group to console] *******************************************
ok: [panorama] => {
    "device_group": "Branch-Office-DG"
}

PLAY RECAP *********************************************************************
panorama                   : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

If the serial number is not found in any device group, the output will show `"Device group not found"`.

## Project Structure

```
firewalls-to-device-groups/
├── ansible.cfg                        # Ansible configuration (inventory path, timeouts, logging)
├── filter_plugins/
│   └── serial_to_devicegroup.py       # Custom filter plugin that maps serial numbers to device groups
├── group_vars/
│   └── panorama.yaml                  # Panorama credentials (move to group_vars/all/credentials.yaml recommended)
├── inventory.yaml                     # Target Panorama host definition
├── playbook.yaml                      # Main playbook that queries device groups
└── README.md                          # This file
```

## Troubleshooting

| Problem | Possible Cause | Solution |
|---|---|---|
| Connection refused | Panorama is unreachable or HTTPS is not enabled | Verify network connectivity and that the management interface is listening on port 443 |
| Invalid credentials / 403 error | Username or password is incorrect | Verify credentials in `group_vars/all/credentials.yaml` |
| Module not found: `paloaltonetworks.panos.panos_op` | The `paloaltonetworks.panos` collection is not installed | Run `ansible-galaxy collection install paloaltonetworks.panos` |
| Timeout error | Panorama is slow to respond or has many device groups | Increase the `timeout` value in `ansible.cfg` |
| "Device group not found" | The serial number does not match any firewall in Panorama | Verify the serial number is correct and the firewall is connected to Panorama |
| Filter plugin not found | Ansible cannot locate the `filter_plugins/` directory | Ensure you run the playbook from within the project directory so the relative path resolves correctly |

## Ansible Concepts Used

- **Playbook**: A YAML file that defines a set of tasks to be executed on target hosts. `playbook.yaml` is the main entry point for this project.
- **Inventory**: A file (`inventory.yaml`) that lists the hosts Ansible will manage. Hosts are organized into groups such as `panorama`.
- **Module**: A unit of work in Ansible. This project uses `paloaltonetworks.panos.panos_op` to run an operational command and `debug` to print output.
- **Collection**: A packaged set of modules, roles, and plugins. The `paloaltonetworks.panos` collection provides all PAN-OS modules used here.
- **Filter Plugin**: A custom Python function that transforms data within Jinja2 expressions. The `find_device_group` filter in `filter_plugins/serial_to_devicegroup.py` parses the device group API response and returns the group name matching a given serial number. Ansible automatically discovers filter plugins placed in a `filter_plugins/` directory alongside the playbook.
- **Jinja2**: A templating language used by Ansible for variable substitution and data manipulation. The expression `results.stdout | from_json | find_device_group(serial_number)` chains Jinja2 filters to parse JSON output and apply the custom filter.
- **Group Variables (group_vars)**: Variables stored in the `group_vars/` directory that apply to all hosts in a group. Credentials are stored here to keep them out of the playbook.
- **Register**: The `register` keyword captures the output of a task into a variable for use in later tasks.
- **set_fact**: A module that creates or updates host-level variables during playbook execution. Used here to store the device group result for later reference.
- **Vault**: Ansible Vault lets you encrypt sensitive files like credential files so secrets are not stored in plain text.
- **Check Mode**: Running a playbook with `--check` simulates execution without making changes, useful for validating logic before applying.
