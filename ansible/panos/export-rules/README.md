# Export PAN-OS Security Rules to CSV

## Overview

This Ansible playbook retrieves security rules from a Palo Alto Networks Panorama appliance and exports them to a CSV file. It uses the `paloaltonetworks.panos` collection to pull both pre-rulebase and post-rulebase security rules via the PAN-OS API. A Jinja2 template then formats the rule data (name, description, and security profile group) into a CSV file for reporting or auditing purposes. The `community.general` collection is also included for additional utility support.

## Prerequisites

- Python 3.8 or later
- Ansible 2.12 or later
- The `paloaltonetworks.panos` Ansible collection
- The `community.general` Ansible collection
- The `pan-os-python` Python library
- API key access to a Panorama appliance

## Quickstart

1. Clone the repository and navigate to this project:

   ```bash
   git clone https://github.com/cdot65/paloaltonetworks-automation-examples.git
   cd paloaltonetworks-automation-examples/ansible/panos/export-rules
   ```

2. Create and activate a Python virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install Ansible and the required Python library:

   ```bash
   pip install ansible pan-os-python
   ```

4. Install the required Ansible collections:

   ```bash
   ansible-galaxy collection install paloaltonetworks.panos community.general
   ```

5. Update the inventory and credentials (see Configuration below).

6. Run the playbook:

   ```bash
   ansible-playbook playbook.yaml
   ```

## Configuration

### Inventory

Edit `inventory.yaml` to point to your Panorama appliance. The hostname listed under `hosts` is used as the `ansible_host` value for API connections.

```yaml
all:
  children:
    panorama:
      hosts:
        panorama.example.com:
      vars:
        ansible_python_interpreter: "{{ ansible_playbook_python }}"
```

Replace `panorama.example.com` with the FQDN or IP address of your Panorama appliance.

### Credentials

Credentials are stored in `group_vars/all/auth.yaml`. Never commit real API keys to version control.

```yaml
---
panorama_api_key: "your-panorama-api-key-here"
```

Encrypt sensitive files with Ansible Vault:

```bash
ansible-vault encrypt group_vars/all/auth.yaml
```

### Variables

| Variable            | Location                   | Required | Description                                           |
|---------------------|----------------------------|----------|-------------------------------------------------------|
| `panorama_api_key`  | `group_vars/all/auth.yaml` | Yes      | API key used to authenticate with Panorama            |
| `ansible_host`      | `inventory.yaml`           | Yes      | FQDN or IP of the Panorama appliance                  |

## Usage

**Basic run:**

```bash
ansible-playbook playbook.yaml
```

**Dry run (check mode):**

```bash
ansible-playbook playbook.yaml --check
```

Check mode simulates the playbook run without making changes. Note that API calls to retrieve rules will still be attempted, but the CSV file will not be written.

**Override variables at runtime:**

```bash
ansible-playbook playbook.yaml -e "panorama_api_key=your-new-key"
```

**Verbose debugging:**

```bash
ansible-playbook playbook.yaml -vvv
```

### Expected Output

```
PLAY [Retrieve Panorama configuration] ****************************************

TASK [Retrieve security pre-rule base] *****************************************
ok: [panorama.example.com]

TASK [Retrieve security post-rule base] ****************************************
ok: [panorama.example.com]

TASK [Parse data and write to CSV file with Jinja2] ****************************
changed: [panorama.example.com]

PLAY RECAP *********************************************************************
panorama.example.com       : ok=3    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

The `ok=3` indicates all three tasks completed. The `changed=1` reflects the CSV file being written to disk. The output file `test.csv` will contain the exported rule names, descriptions, and security profile groups.

## Project Structure

```
export-rules/
├── ansible.cfg                          # Ansible configuration (inventory path, timeouts)
├── group_vars/
│   └── all/
│       └── auth.yaml                    # Panorama API key credential
├── inventory.yaml                       # Target Panorama host definition
├── playbook.yaml                        # Main playbook that retrieves rules and writes CSV
├── templates/
│   └── security_profile_group.j2        # Jinja2 template for CSV formatting
└── test.csv                             # Example CSV output
```

## Troubleshooting

| Problem                        | Possible Cause                                     | Solution                                                                 |
|-------------------------------|----------------------------------------------------|--------------------------------------------------------------------------|
| Connection refused             | Panorama is unreachable or wrong IP/FQDN           | Verify network connectivity and the host in `inventory.yaml`             |
| Invalid credentials            | API key is incorrect or expired                     | Generate a new API key and update `group_vars/all/auth.yaml`             |
| Module not found               | `paloaltonetworks.panos` collection not installed   | Run `ansible-galaxy collection install paloaltonetworks.panos`           |
| Timeout                        | Panorama is slow to respond                        | Increase `timeout` in `ansible.cfg` or set `command_timeout` higher      |
| Empty CSV output               | No rules in the specified rulebase                  | Verify that pre-rulebase and post-rulebase contain rules in Panorama     |
| Template rendering error       | Rule data structure has changed                    | Run with `-vvv` to inspect the `pre_rule_base` and `post_rule_base` data |

## Ansible Concepts Used

- **Playbook**: A YAML file that defines the sequence of tasks to execute on targeted hosts. `playbook.yaml` is the entry point for this project.
- **Inventory**: Defines which hosts Ansible manages. Here, `inventory.yaml` lists the Panorama appliance under the `panorama` group.
- **Module**: Reusable units of work. This project uses `panos_security_rule_facts` to retrieve rules and `template` to render the CSV.
- **Collection**: A packaged set of modules, roles, and plugins. `paloaltonetworks.panos` provides PAN-OS modules and `community.general` provides utility modules.
- **Group Vars**: Variables applied to all hosts in a group. The `group_vars/all/` directory stores credentials shared across all hosts.
- **Jinja2 Template**: A templating language used by Ansible. The `.j2` file loops through rule data and formats it as CSV output using `{% for %}` loops to iterate over pre-rulebase and post-rulebase entries.
- **Check Mode**: A dry-run mode (`--check`) that shows what would change without actually making changes.
- **Vault**: An Ansible feature to encrypt sensitive files like credentials. Use `ansible-vault encrypt` to protect your API key file.
- **Register**: Captures the output of a task into a variable for use in later tasks. Both rule retrieval tasks register their results for use by the template.
