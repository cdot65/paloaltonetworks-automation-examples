# Updating Content on Panorama with Ansible

## Overview

This project automates the process of downloading the latest Application and Threats content updates and Antivirus updates on a Palo Alto Networks Panorama management server. It uses the `paloaltonetworks.panos` Ansible collection to issue operational commands via the PAN-OS XML API. The playbook checks for available updates, downloads the latest content packages, and polls each download job until completion before proceeding. Job completion is monitored with up to 20 retries at 30-second intervals to accommodate large downloads.

## Prerequisites

- Python 3.6 or later
- Ansible 2.10 or later
- The `paloaltonetworks.panos` collection installed
- The `ansible.utils` collection installed
- The `pan-os-python` Python library installed
- Network access to your Panorama appliance on HTTPS (TCP/443)
- A valid PAN-OS API key with permissions to manage content updates

## Quickstart

1. Clone the repository and navigate to this project:

   ```bash
   git clone https://github.com/cdot65/paloaltonetworks-automation-examples.git
   cd paloaltonetworks-automation-examples/ansible/panorama/content-update
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

Replace `panorama.example.com` with the FQDN or IP address of your Panorama appliance. Because `ansible_host` is not explicitly set, Ansible will resolve the hostname you provide here directly.

### Credentials

Store your credentials in `group_vars/all/credentials.yaml`:

```yaml
---
panorama_hostname: "panorama.example.com"
panorama_api_key: "your-api-key-here"
```

To encrypt this file with Ansible Vault:

```bash
ansible-vault encrypt group_vars/all/credentials.yaml
```

You will then need to pass `--ask-vault-pass` when running the playbook.

### Variables

| Variable | Location | Required | Description |
|---|---|---|---|
| `panorama_hostname` | `group_vars/all/credentials.yaml` | Yes | FQDN or IP of the Panorama appliance used in the provider block |
| `panorama_api_key` | `group_vars/all/credentials.yaml` | Yes | API key for authenticating to the PAN-OS XML API |

## Usage

**Basic run:**

```bash
ansible-playbook playbook.yaml
```

**Dry run (check mode):**

```bash
ansible-playbook playbook.yaml --check
```

Check mode simulates the playbook run without making any changes on Panorama. Note that operational commands issued via `panos_op` may not fully support check mode, so some tasks may be skipped or behave differently.

**Override a variable at runtime:**

```bash
ansible-playbook playbook.yaml -e "panorama_hostname=panorama.corp.example.com"
```

**Verbose debugging output:**

```bash
ansible-playbook playbook.yaml -vvv
```

### Expected Output

A successful run will produce output similar to:

```
PLAY [panorama] ****************************************************************

TASK [Check latest content] ****************************************************
ok: [panorama.example.com]

TASK [Download latest Application and Threats content] *************************
changed: [panorama.example.com]

TASK [Check content download result] *******************************************
FAILED - RETRYING: Check content download result (20 retries left).
ok: [panorama.example.com]

TASK [Download latest Antivirus updates] ***************************************
changed: [panorama.example.com]

TASK [Check content download_av result] ****************************************
FAILED - RETRYING: Check content download_av result (20 retries left).
ok: [panorama.example.com]

PLAY RECAP *********************************************************************
panorama.example.com       : ok=5    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

The "RETRYING" messages are expected -- the playbook polls the download job status every 30 seconds until the job finishes.

## Project Structure

```
content-update/
├── ansible.cfg                  # Ansible configuration (inventory path, timeouts, logging)
├── group_vars/
│   └── all/
│       └── auth.yaml            # Panorama API key (rename to credentials.yaml recommended)
├── inventory.yaml               # Target Panorama host definition
├── playbook.yaml                # Main playbook that downloads content and AV updates
└── README.md                    # This file
```

## Troubleshooting

| Problem | Possible Cause | Solution |
|---|---|---|
| Connection refused | Panorama is unreachable or HTTPS is not enabled | Verify network connectivity and that the management interface is listening on port 443 |
| Invalid credentials / 403 error | API key is incorrect or expired | Generate a new API key and update `group_vars/all/credentials.yaml` |
| Module not found: `paloaltonetworks.panos.panos_op` | The `paloaltonetworks.panos` collection is not installed | Run `ansible-galaxy collection install paloaltonetworks.panos` |
| Timeout waiting for download job | Content download is taking longer than expected | Increase the `retries` or `delay` values in `playbook.yaml` |
| Download job status shows `FAIL` | Panorama cannot reach the Palo Alto Networks update server | Check DNS resolution and internet access from Panorama |

## Ansible Concepts Used

- **Playbook**: A YAML file that defines a set of tasks to be executed on target hosts. `playbook.yaml` is the main entry point for this project.
- **Inventory**: A file (`inventory.yaml`) that lists the hosts Ansible will manage. Hosts are organized into groups such as `panorama`.
- **Module**: A unit of work in Ansible. This project uses `paloaltonetworks.panos.panos_op` to run operational commands on Panorama.
- **Collection**: A packaged set of modules, roles, and plugins. The `paloaltonetworks.panos` collection provides all PAN-OS modules used here.
- **Group Variables (group_vars)**: Variables stored in the `group_vars/` directory that apply to all hosts in a group. Credentials are stored here to keep them out of the playbook.
- **Register**: The `register` keyword captures the output of a task into a variable for use in later tasks.
- **Retries and Delay**: The `until`, `retries`, and `delay` keywords allow a task to be repeated until a condition is met, used here to poll job completion status.
- **Vault**: Ansible Vault lets you encrypt sensitive files like credential files so secrets are not stored in plain text.
- **Check Mode**: Running a playbook with `--check` simulates execution without making changes, useful for validating logic before applying.
