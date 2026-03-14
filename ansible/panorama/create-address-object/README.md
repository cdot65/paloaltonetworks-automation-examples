# Creating Address Objects on Panorama with Ansible

## Overview

This project demonstrates how to create an address object on a Palo Alto Networks Panorama management server using Ansible. It uses the `paloaltonetworks.panos` collection's `panos_address_object` module to define an FQDN-based address object. The playbook runs in check mode by default, validating that Panorama would accept the object without actually creating it, and then prints the result to the console. This pattern is useful for testing API connectivity and validating object definitions before applying them.

## Prerequisites

- Python 3.6 or later
- Ansible 2.10 or later
- The `paloaltonetworks.panos` collection installed
- The `ansible.utils` collection installed
- The `pan-os-python` Python library installed
- Network access to your Panorama appliance on HTTPS (TCP/443)
- A valid PAN-OS API key and username with permissions to manage address objects

## Quickstart

1. Clone the repository and navigate to this project:

   ```bash
   git clone https://github.com/cdot65/paloaltonetworks-automation-examples.git
   cd paloaltonetworks-automation-examples/ansible/panorama/create-address-object
   ```

2. Create and activate a Python virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install Ansible and the required collections:

   ```bash
   pip install ansible pan-os-python
   ansible-galaxy collection install paloaltonetworks.panos ansible.utils
   ```

4. Edit `inventory.yaml` to set your Panorama hostname and update `group_vars/all/credentials.yaml` with your API key (see Configuration below).

5. Run the playbook:

   ```bash
   ansible-playbook playbook.yaml
   ```

## Configuration

### Inventory

The inventory file `inventory.yaml` defines the Panorama host to target:

```yaml
all:
  children:
    panorama:
      hosts:
        panorama.example.com:
```

Replace `panorama.example.com` with the FQDN or IP address of your Panorama appliance. Ansible will use this hostname to connect to the device. Since `ansible_host` is not explicitly set, the hostname entry itself is used for resolution.

### Credentials

Store your credentials in `group_vars/all/credentials.yaml`:

```yaml
---
panorama_api_key: "your-api-key-here"
panorama_username: "admin"
```

To encrypt this file with Ansible Vault:

```bash
ansible-vault encrypt group_vars/all/credentials.yaml
```

You will then need to pass `--ask-vault-pass` when running the playbook.

### Variables

| Variable | Location | Required | Description |
|---|---|---|---|
| `panorama_api_key` | `group_vars/all/credentials.yaml` | Yes | API key for authenticating to the PAN-OS XML API |
| `panorama_username` | `group_vars/all/credentials.yaml` | Yes | Username for Panorama login |
| `ansible_host` | `inventory.yaml` | Yes | FQDN or IP of the Panorama appliance (derived from the host entry name) |

## Usage

**Basic run:**

```bash
ansible-playbook playbook.yaml
```

Note: The playbook has `check_mode: yes` hardcoded on the address object creation task, so it validates without creating the object by default. To actually create the object, edit `playbook.yaml` and remove the `check_mode: yes` line.

**Dry run (check mode):**

```bash
ansible-playbook playbook.yaml --check
```

Check mode simulates the playbook run without making any changes on Panorama. This is in addition to the task-level check mode already set in the playbook.

**Override credentials at runtime:**

```bash
ansible-playbook playbook.yaml -e "panorama_username=admin panorama_api_key=your-key"
```

**Verbose debugging output:**

```bash
ansible-playbook playbook.yaml -vvv
```

### Expected Output

A successful run will produce output similar to:

```
PLAY [panorama] ****************************************************************

TASK [Validate that Panorama would allow us to create an object, check mode] ***
ok: [panorama.example.com]

TASK [Print result to the console] *********************************************
ok: [panorama.example.com] => {
    "msg": {
        "changed": false,
        "msg": "done"
    }
}

PLAY RECAP *********************************************************************
panorama.example.com       : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

Because the task uses check mode, `changed` shows `0` -- the object was validated but not created.

## Project Structure

```
create-address-object/
├── ansible.cfg                  # Ansible configuration (inventory path, timeouts, logging)
├── group_vars/
│   └── all/
│       └── auth.yaml            # Panorama API key (rename to credentials.yaml recommended)
├── inventory.yaml               # Target Panorama host definition
├── playbook.yaml                # Main playbook that creates an FQDN address object in check mode
└── README.md                    # This file
```

## Troubleshooting

| Problem | Possible Cause | Solution |
|---|---|---|
| Connection refused | Panorama is unreachable or HTTPS is not enabled | Verify network connectivity and that the management interface is listening on port 443 |
| Invalid credentials / 403 error | API key is incorrect or expired | Generate a new API key and update `group_vars/all/credentials.yaml` |
| Module not found: `panos_address_object` | The `paloaltonetworks.panos` collection is not installed | Run `ansible-galaxy collection install paloaltonetworks.panos` |
| Timeout error | Panorama is slow to respond | Increase the `timeout` value in `ansible.cfg` |
| Object already exists error | An address object with the same name already exists | Change the `name` field in the playbook or use `state: replaced` |

## Ansible Concepts Used

- **Playbook**: A YAML file that defines a set of tasks to be executed on target hosts. `playbook.yaml` is the main entry point for this project.
- **Inventory**: A file (`inventory.yaml`) that lists the hosts Ansible will manage. Hosts are organized into groups such as `panorama`.
- **Module**: A unit of work in Ansible. This project uses `panos_address_object` to create address objects and `debug` to print output.
- **Collection**: A packaged set of modules, roles, and plugins. The `paloaltonetworks.panos` collection provides all PAN-OS modules used here.
- **Group Variables (group_vars)**: Variables stored in the `group_vars/` directory that apply to all hosts in a group. Credentials are stored here to keep them out of the playbook.
- **Check Mode**: Running a task with `check_mode: yes` (or a playbook with `--check`) simulates execution without making changes. This playbook uses task-level check mode to validate the address object creation without committing it.
- **Register**: The `register` keyword captures the output of a task into a variable for use in later tasks. Here it captures the result of the address object validation.
- **Vault**: Ansible Vault lets you encrypt sensitive files like credential files so secrets are not stored in plain text.
