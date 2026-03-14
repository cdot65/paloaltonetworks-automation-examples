# Build and Load PAN-OS XML Configuration with Jinja2 Templates

## Overview

This project generates a complete PAN-OS XML configuration from Jinja2 templates and per-host variable files, then uploads and loads it onto a Palo Alto Networks firewall via the PAN-OS REST API. Three Ansible roles work in sequence: `directories` creates clean local build folders, `build_config` renders Jinja2 templates for management, shared, and device configuration sections into XML fragments, and `assemble` merges those fragments into a single XML file. The completed configuration is then uploaded to the firewall using `curl` and loaded into the candidate configuration for review before committing. No external Ansible collections are required -- this project uses only `ansible.builtin` modules.

## Prerequisites

- Python 3.8+
- Ansible Core 2.10+
- `curl` installed on the Ansible control node
- PAN-OS firewall with API access enabled
- A valid PAN-OS API key (`X-PAN-KEY`)

## Quickstart

1. Clone the repository and navigate to the project directory:

   ```bash
   git clone https://github.com/cdot65/paloaltonetworks-automation-examples.git
   cd paloaltonetworks-automation-examples/ansible/panos/create-config-and-load
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

4. Update inventory and host variables for your firewall (see Configuration below).

5. Run the playbook:

   ```bash
   ansible-playbook playbook.yaml -e "api_token=YOUR_API_KEY"
   ```

## Configuration

### Inventory

Edit `inventory.yaml` to list your firewall hostnames. The hostname is used as `ansible_host` for API calls and as part of generated file paths.

```yaml
all:
  children:
    firewalls:
      hosts:
        dal-vfw-01:
```

The `ansible_host` value defaults to the inventory hostname (e.g., `dal-vfw-01`). If your firewall's DNS name or IP differs, add `ansible_host` explicitly:

```yaml
        dal-vfw-01:
          ansible_host: 10.0.0.1
```

### Credentials

Create `group_vars/all/credentials.yaml` with your PAN-OS API key:

```yaml
api_token: "your-panos-api-key-here"
```

Encrypt it with Ansible Vault to keep secrets out of version control:

```bash
ansible-vault encrypt group_vars/all/credentials.yaml
```

Alternatively, pass the API key at runtime with `-e "api_token=YOUR_API_KEY"`.

### Variables

| Variable | Location | Required | Description |
|----------|----------|----------|-------------|
| `api_token` | `group_vars/all/credentials.yaml` or `-e` flag | Yes | PAN-OS API key for REST API authentication |
| `temporary_folder` | `host_vars/<host>/paths.yml` | Yes | Local path for temporary XML fragments |
| `completed_folder` | `host_vars/<host>/paths.yml` | Yes | Local path for assembled XML output |
| `completed_config_file` | `host_vars/<host>/paths.yml` | Yes | Full path to the final assembled XML file |
| `deviceconfig` | `host_vars/<host>/deviceconfig.yaml` | Yes | System settings: hostname, IP, DNS, timezone, Panorama |
| `network` | `host_vars/<host>/network.yaml` | Yes | Ethernet interface definitions |
| `users` | `host_vars/<host>/users.yaml` | Yes | Admin user accounts with password hashes |
| `vr` | `host_vars/<host>/vr.yaml` | Yes | Virtual router and BGP configuration |
| `vsys` | `host_vars/<host>/vsys.yaml` | Yes | Zones, address objects, vsys settings |
| `configuration` | `roles/build_config/vars/main.yaml` | Yes | Flags controlling which config sections to render |
| `any_errors_fatal` | Playbook | No | Stop on first error (default `true`) |

## Usage

### Basic Run

Build and load configuration for all firewalls in the inventory:

```bash
ansible-playbook playbook.yaml -e "api_token=YOUR_API_KEY"
```

### Dry Run

```bash
ansible-playbook playbook.yaml --check -e "api_token=YOUR_API_KEY"
```

Check mode simulates the playbook run without creating files, uploading configurations, or making API calls. Template rendering and file operations will show as "changed" but nothing is written to disk or sent to the firewall.

### Variable Override

Target a specific host and override the timezone:

```bash
ansible-playbook playbook.yaml --limit dal-vfw-01 -e "api_token=YOUR_API_KEY" -e "deviceconfig_timezone=US/Eastern"
```

### Verbose Debugging

```bash
ansible-playbook playbook.yaml -vvv -e "api_token=YOUR_API_KEY"
```

### Expected Output

```
PLAY [all] *********************************************************************

TASK [directories : remove previous temporary build directory] ******************
changed: [dal-vfw-01]

TASK [directories : create new temporary directory] ****************************
changed: [dal-vfw-01]

TASK [directories : ensure a completed config directory exists] *****************
ok: [dal-vfw-01]

TASK [build_config : building '<mgt-config>' config document] ******************
changed: [dal-vfw-01]

TASK [build_config : building '<shared>' config document] **********************
changed: [dal-vfw-01]

TASK [build_config : building '<devices>' config document] *********************
changed: [dal-vfw-01]

TASK [assemble : check if directory is present] ********************************
ok: [dal-vfw-01]

TASK [assemble : assemble configurations to temp completed folder] *************
changed: [dal-vfw-01]

TASK [assemble : Remove blank lines between matches] ***************************
changed: [dal-vfw-01]

TASK [Upload our generated configuration file] *********************************
changed: [dal-vfw-01]

TASK [Load our generated configuration into the candidate configuration] *******
changed: [dal-vfw-01]

PLAY RECAP *********************************************************************
dal-vfw-01                 : ok=11   changed=8    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

- `ok=11` -- all eleven tasks completed successfully.
- `changed=8` -- directories were created, templates rendered, config assembled, uploaded, and loaded.
- `failed=0` -- no errors. If the firewall API rejects the upload, this counter increments.

## Project Structure

```
create-config-and-load/
├── ansible.cfg                              # Ansible settings (inventory path, timeouts)
├── inventory.yaml                           # Firewall hosts
├── playbook.yaml                            # Main playbook: roles + upload + load tasks
├── config/
│   ├── completed/                           # Assembled XML output files
│   │   └── dal-vfw-01_ansible.xml
│   └── tmp/                                 # Per-host temporary XML fragments
│       └── dal-vfw-01/
│           ├── 01_mgt_config.xml
│           ├── 02_shared.xml
│           └── 03_devices.xml
├── host_vars/
│   └── dal-vfw-01/                          # Per-firewall variables
│       ├── deviceconfig.yaml                # System settings (hostname, DNS, timezone)
│       ├── devices.yaml                     # Device entry configuration
│       ├── full.yml                         # Full config mode toggle
│       ├── network.yaml                     # Interface definitions
│       ├── paths.yml                        # Build directory paths and python interpreter
│       ├── users.yaml                       # Admin user accounts and password hashes
│       ├── vr.yaml                          # Virtual router and BGP configuration
│       └── vsys.yaml                        # Zones and address objects
└── roles/
    ├── assemble/
    │   └── tasks/main.yml                   # Merge XML fragments; remove blank lines
    ├── build_config/
    │   ├── tasks/main.yml                   # Render Jinja2 templates to XML fragments
    │   ├── templates/
    │   │   ├── mgt_config.j2               # Management config: users, passwords
    │   │   ├── shared.j2                   # Shared config: botnet, applications
    │   │   ├── devices.j2                  # Devices: interfaces, routing, zones, deviceconfig
    │   │   └── full.j2                     # Full standalone config (alternative to fragments)
    │   └── vars/main.yaml                  # Flags for which config sections to build
    └── directories/
        └── tasks/main.yaml                  # Create/clean build directories
```

## Troubleshooting

| Problem | Possible Cause | Solution |
|---------|---------------|----------|
| Connection refused when uploading | Firewall management interface unreachable | Verify network connectivity and that HTTPS API access is enabled on the firewall |
| Invalid credentials / HTTP 403 | Wrong or expired API key | Generate a new API key via PAN-OS: `curl -k 'https://FIREWALL/api/?type=keygen&user=admin&password=PASSWORD'` |
| Module not found: `ansible.builtin.template` | Ansible not installed or too old | Run `pip install ansible` and verify version with `ansible --version` |
| Timeout during upload | Large config file or slow network | Increase `timeout` in `ansible.cfg` (current value: 240 seconds) |
| `curl: command not found` | `curl` not installed on control node | Install curl: `apt install curl` or `yum install curl` |
| Jinja2 template rendering error | Missing or misnamed host variable | Verify all required variables exist in `host_vars/<hostname>/` and match template expectations |

## Ansible Concepts Used

- **Playbook**: A YAML file that defines tasks and role imports to execute against inventory hosts. `playbook.yaml` imports three roles and runs two shell tasks.

- **Inventory**: A file listing hosts and groups. The `firewalls` group in `inventory.yaml` contains the target firewall hostnames.

- **Role**: A reusable, self-contained unit of Ansible content. This project uses three roles: `directories` (file management), `build_config` (template rendering), and `assemble` (file merging).

- **Module**: A unit of code Ansible executes. This project uses `ansible.builtin.template` (render Jinja2), `ansible.builtin.file` (manage directories), `ansible.builtin.assemble` (merge files), `ansible.builtin.lineinfile` (remove blank lines), and `ansible.builtin.shell` (run curl commands).

- **Jinja2**: A Python templating engine used by Ansible. The `templates/` directory contains `.j2` files that combine XML structure with variable substitution and control flow (`{% for %}`, `{% if %}`). Jinja2 renders these into valid PAN-OS XML configuration fragments.

- **Host Vars**: Variable files in `host_vars/<hostname>/` that apply only to a specific host. Each firewall gets its own directory with device-specific settings like IP addresses, interfaces, and routing configuration.

- **Group Vars**: Variable files that apply to all hosts in a group. Used here for credentials shared across all firewalls.

- **Vault**: Ansible Vault encrypts files containing sensitive data (API keys). Use `ansible-vault encrypt` to protect credentials and `--ask-vault-pass` at runtime.

- **Check Mode**: A dry-run mode (`--check`) that shows what the playbook would change without making actual modifications.
