# Override and Disable Captive Portal on PAN-OS

## Overview

This Ansible playbook overrides and disables the captive portal feature on a Palo Alto Networks firewall. It uses a role-based structure with two task files: one sends a CLI override command via `ansible.netcommon.cli_config`, and another uses the PAN-OS XML API through `ansible.builtin.uri` to edit the captive portal configuration and set `enable-captive-portal` to `no`. The `panos_config` role encapsulates both approaches, allowing each to be included independently.

## Prerequisites

- Python 3.8 or later
- Ansible 2.12 or later
- The `ansible.netcommon` Ansible collection
- API key access and CLI (SSH) access to a PAN-OS firewall
- Network reachability to the firewall management interface (HTTPS for API, SSH for CLI)

## Quickstart

1. Clone the repository and navigate to this project:

   ```bash
   git clone https://github.com/cdot65/paloaltonetworks-automation-examples.git
   cd paloaltonetworks-automation-examples/ansible/panos/override-captive-portal
   ```

2. Create and activate a Python virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install Ansible:

   ```bash
   pip install ansible
   ```

4. Install the required Ansible collections:

   ```bash
   ansible-galaxy collection install ansible.netcommon
   ```

5. Update the inventory and credentials (see Configuration below).

6. Run the playbook:

   ```bash
   ansible-playbook playbook.yaml
   ```

## Configuration

### Inventory

Edit `inventory.yaml` to point to your PAN-OS firewall. The hostname listed under `hosts` is the FQDN or IP address of the device.

```yaml
all:
  children:
    panos_firewall:
      hosts:
        firewall.example.com:
```

Replace `firewall.example.com` with the FQDN or IP address of your firewall.

### Credentials

Credentials are stored in `group_vars/all/secrets.yaml`. Never commit real passwords or API keys to version control.

```yaml
---
ansible_user: "your-username-here"
ansible_password: "your-password-here"
api_key: "your-api-key-here"
```

Encrypt sensitive files with Ansible Vault:

```bash
ansible-vault encrypt group_vars/all/secrets.yaml
```

### Variables

| Variable              | Location                       | Required | Description                                                |
|-----------------------|--------------------------------|----------|------------------------------------------------------------|
| `ansible_user`        | `group_vars/all/secrets.yaml`  | Yes      | SSH username for CLI access to the firewall                |
| `ansible_password`    | `group_vars/all/secrets.yaml`  | Yes      | SSH password for CLI access to the firewall                |
| `api_key`             | `group_vars/all/secrets.yaml`  | Yes      | API key for PAN-OS XML API calls                           |
| `ansible_host`        | `inventory.yaml`               | Yes      | FQDN or IP of the firewall                                |
| `ansible_connection`  | `group_vars/all/settings.yaml` | Yes      | Connection type (set to `ansible.netcommon.network_cli`)   |

## Usage

**Basic run:**

```bash
ansible-playbook playbook.yaml
```

**Dry run (check mode):**

```bash
ansible-playbook playbook.yaml --check
```

Check mode simulates the playbook without making changes. The CLI config task and the API call will not be executed, allowing you to verify connectivity and variable resolution before modifying the firewall.

**Override variables at runtime:**

```bash
ansible-playbook playbook.yaml -e "api_key=your-new-api-key"
```

**Verbose debugging:**

```bash
ansible-playbook playbook.yaml -vvv
```

### Expected Output

```
PLAY [Override and Disable Captive Portal] *************************************

TASK [Override Captive Portal] *************************************************
ok: [firewall.example.com]

TASK [Display configuration output] ********************************************
ok: [firewall.example.com] => {
    "config_result": ...
}

TASK [Disable Captive Portal] **************************************************
changed: [firewall.example.com]

TASK [Display disable output] **************************************************
ok: [firewall.example.com] => {
    "disable_result": ...
}

PLAY RECAP *********************************************************************
firewall.example.com       : ok=4    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

The `ok=4` shows all four tasks completed. `changed=1` indicates the captive portal configuration was modified on the firewall via the API call.

## Project Structure

```
override-captive-portal/
├── ansible.cfg                                    # Ansible configuration (connection type, timeouts)
├── group_vars/
│   └── all/
│       ├── python.yaml                            # Python interpreter setting
│       ├── secrets.yaml                           # Credentials (username, password, API key)
│       └── settings.yaml                          # Connection and network OS settings
├── inventory.yaml                                 # Target firewall host definition
├── playbook.yaml                                  # Main playbook that calls the panos_config role
└── roles/
    └── panos_config/
        └── tasks/
            ├── configure_captive_portal.yaml       # CLI-based captive portal override task
            └── disable_captive_portal.yaml         # API-based captive portal disable task
```

## Troubleshooting

| Problem                        | Possible Cause                                      | Solution                                                                  |
|-------------------------------|-----------------------------------------------------|---------------------------------------------------------------------------|
| Connection refused             | Firewall is unreachable or wrong IP/FQDN            | Verify network connectivity and the host in `inventory.yaml`              |
| Invalid credentials            | Username, password, or API key is incorrect          | Update `group_vars/all/secrets.yaml` with correct values                  |
| Module not found               | `ansible.netcommon` collection not installed         | Run `ansible-galaxy collection install ansible.netcommon`                  |
| Timeout                        | Firewall is slow to respond                         | Increase `timeout` in `ansible.cfg` or `command_timeout`                  |
| SSL certificate error          | Self-signed cert on firewall management interface    | The `validate_certs: no` option in the API task handles this; verify it is set |
| `ignore_errors` masking issues | Task fails silently due to `ignore_errors: yes`     | Run with `-vvv` to see full error details from each task                  |

## Ansible Concepts Used

- **Playbook**: A YAML file defining plays and tasks. `playbook.yaml` orchestrates the captive portal override and disable steps.
- **Inventory**: Defines target hosts. `inventory.yaml` lists the firewall under the `panos_firewall` group.
- **Role**: A reusable, structured set of tasks organized into a standard directory layout. The `panos_config` role contains two separate task files that can be included independently.
- **Module**: Reusable units of work. `cli_config` sends CLI commands over SSH. `uri` makes HTTP API calls. `debug` prints variable contents to the console.
- **Collection**: A packaged set of modules and plugins. `ansible.netcommon` provides network device modules like `cli_config` and the `network_cli` connection plugin.
- **Group Vars**: Variables applied to all hosts in a group, split across multiple files: `secrets.yaml` (credentials), `settings.yaml` (connection config), and `python.yaml` (interpreter setting).
- **Include Role**: The `include_role` directive with `tasks_from` loads a specific task file from a role rather than the default `main.yml`, allowing selective execution of role tasks.
- **Check Mode**: A dry-run mode activated with `--check` that previews changes without applying them to the firewall.
- **Vault**: An Ansible feature to encrypt sensitive files. Use `ansible-vault encrypt group_vars/all/secrets.yaml` to protect credentials at rest.
- **Register**: Captures task output into a variable for display or conditional logic in subsequent tasks.
