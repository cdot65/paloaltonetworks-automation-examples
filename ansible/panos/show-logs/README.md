# Retrieve and Display PAN-OS Traffic Logs

## Overview

This Ansible playbook retrieves traffic log entries from a Palo Alto Networks firewall using the PAN-OS XML API. It queries for dropped traffic logs by initiating an asynchronous log job, waits for completion, then parses the XML response into structured YAML and displays the results. The playbook uses `ansible.builtin.uri` to make raw API calls and the `ansible.utils` collection's `from_xml` filter to convert XML responses into readable data. This is useful for quick log inspection without needing the firewall GUI.

## Prerequisites

- Python 3.8 or later
- Ansible 2.12 or later
- The `ansible.utils` Ansible collection (provides the `from_xml` filter)
- The `xmltodict` Python library
- API key access to a PAN-OS firewall

## Quickstart

1. Clone the repository and navigate to this project:

   ```bash
   git clone https://github.com/cdot65/paloaltonetworks-automation-examples.git
   cd paloaltonetworks-automation-examples/ansible/panos/show-logs
   ```

2. Create and activate a Python virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install Ansible and required Python packages:

   ```bash
   pip install ansible xmltodict
   ```

4. Install the required Ansible collections:

   ```bash
   ansible-galaxy collection install ansible.utils
   ```

5. Create `group_vars/all/credentials.yaml` and update the inventory (see Configuration below).

6. Run the playbook:

   ```bash
   ansible-playbook playbook.yaml
   ```

## Configuration

### Inventory

Edit `inventory.yaml` to list your PAN-OS firewall. The `ansible_host` value provides the IP address or FQDN used for API connections.

```yaml
all:
  children:
    firewalls:
      hosts:
        my-firewall:
          ansible_host: 192.168.1.1
```

Replace `my-firewall` with a descriptive name and `192.168.1.1` with the actual management IP of your firewall.

### Credentials

Store the API key in `group_vars/all/credentials.yaml` rather than inline in the playbook. Create the `group_vars/all/` directory if it does not exist.

```yaml
---
api_key: "your-api-key-here"
```

Encrypt sensitive files with Ansible Vault:

```bash
ansible-vault encrypt group_vars/all/credentials.yaml
```

### Variables

| Variable                    | Location                          | Required | Description                                           |
|-----------------------------|-----------------------------------|----------|-------------------------------------------------------|
| `api_key`                   | `group_vars/all/credentials.yaml` | Yes      | API key for PAN-OS XML API authentication             |
| `amount_of_logs_to_return`  | `playbook.yaml` (vars section)    | No       | Number of log entries to retrieve (default: 5)        |
| `ansible_host`              | `inventory.yaml`                  | Yes      | Management IP or FQDN of the firewall                 |

## Usage

**Basic run:**

```bash
ansible-playbook playbook.yaml
```

**Dry run (check mode):**

```bash
ansible-playbook playbook.yaml --check
```

Check mode simulates the playbook without making changes. Since this playbook only reads logs (no configuration changes), the API calls will be skipped in check mode.

**Override variables at runtime:**

```bash
ansible-playbook playbook.yaml -e "amount_of_logs_to_return=20"
```

**Verbose debugging:**

```bash
ansible-playbook playbook.yaml -vvv
```

### Expected Output

```
PLAY [Retrieve and format PAN-OS firewall log data] ****************************

TASK [Initial API request] *****************************************************
ok: [my-firewall]

TASK [Extract job ID] **********************************************************
ok: [my-firewall]

TASK [Wait for 2 seconds] ******************************************************
Pausing for 2 seconds
ok: [my-firewall]

TASK [Retrieve log data] *******************************************************
ok: [my-firewall]

TASK [Parse XML and convert to YAML] *******************************************
ok: [my-firewall]

TASK [Extract log entries] *****************************************************
ok: [my-firewall]

TASK [Display log data in YAML format] *****************************************
ok: [my-firewall] => {
    "log_data": [
        {
            "src": "10.0.1.5",
            "dst": "203.0.113.10",
            "app": "web-browsing",
            "action": "drop",
            ...
        }
    ]
}

PLAY RECAP *********************************************************************
my-firewall                : ok=7    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

The `ok=7` indicates all seven tasks completed. `changed=0` is expected because this playbook only reads log data and does not modify any firewall configuration.

## Project Structure

```
show-logs/
├── ansible.cfg              # Ansible configuration (inventory path, timeouts)
├── inventory.yaml           # Target firewall host definition with ansible_host IP
├── playbook.yaml            # Main playbook that queries and displays traffic logs
└── screenshots/             # Reference screenshots (optional)
```

## Troubleshooting

| Problem                        | Possible Cause                                     | Solution                                                                 |
|-------------------------------|----------------------------------------------------|--------------------------------------------------------------------------|
| Connection refused             | Firewall is unreachable or wrong IP/FQDN           | Verify network connectivity and `ansible_host` in `inventory.yaml`       |
| Invalid credentials            | API key is incorrect or expired                     | Generate a new API key and update `group_vars/all/credentials.yaml`      |
| Module not found               | `ansible.utils` collection not installed            | Run `ansible-galaxy collection install ansible.utils`                    |
| Timeout                        | Firewall is slow to respond or log query is large   | Increase `timeout` in `ansible.cfg` or reduce `amount_of_logs_to_return` |
| Empty log data                 | No matching traffic logs on the firewall            | Adjust the query filter in the API URL or check that drop logs exist     |
| XML parsing error              | `xmltodict` Python library not installed            | Run `pip install xmltodict` in your virtual environment                  |
| Job ID extraction fails        | API response format has changed                    | Run with `-vvv` to inspect `initial_response.content`                    |

## Ansible Concepts Used

- **Playbook**: A YAML file defining tasks to run. `playbook.yaml` orchestrates the multi-step log retrieval workflow (initiate query, wait, retrieve results, parse, display).
- **Inventory**: Defines target hosts. `inventory.yaml` lists the firewall with its management IP under the `firewalls` group.
- **Module**: Reusable units of work. `uri` makes HTTP requests to the PAN-OS API. `set_fact` stores intermediate data like the job ID and parsed results. `debug` prints results. `pause` introduces a wait between the asynchronous API calls.
- **Collection**: A packaged set of modules and plugins. `ansible.utils` provides the `from_xml` filter plugin used to parse the XML API response.
- **Filter Plugin**: A plugin that transforms data within Jinja2 expressions. `from_xml` converts XML strings into Python dictionaries. `regex_search` extracts the job ID from the initial API response using a regular expression.
- **Group Vars**: Variables applied to all hosts in a group. Store the API key in `group_vars/all/credentials.yaml` rather than inline in playbooks.
- **Register**: Captures task output into variables (`initial_response`, `log_response`) for use in subsequent tasks.
- **Check Mode**: A dry-run mode activated with `--check` that previews what would happen without executing API calls.
- **Vault**: An Ansible feature to encrypt sensitive files. Use `ansible-vault encrypt group_vars/all/credentials.yaml` to protect your API key at rest.
