# Create Security Policies on Panorama

## Overview

This project demonstrates three progressively mature approaches to creating security policy rules on Palo Alto Networks Panorama using the `paloaltonetworks.panos` Ansible collection. All three approaches use the `panos_security_rule` module to push pre-rules to a Panorama device group. Approach 1 (`1-simple`) hardcodes credentials and rule parameters directly in the playbook. Approach 2 (`2-variable-files`) extracts credentials into `group_vars` and rule definitions into `host_vars`. Approach 3 (`3-ansible-vault`) builds on Approach 2 by encrypting the credentials file with Ansible Vault. This progression teaches best practices for separating configuration from code and protecting secrets.

## Prerequisites

- Python 3.8+
- Ansible Core 2.10+
- `paloaltonetworks.panos` Ansible collection
- `pan-os-python` Python library
- Network access to Panorama management interface
- Panorama admin credentials with configuration privileges

## Quickstart

1. Clone the repository and navigate to the project directory:

   ```bash
   git clone https://github.com/cdot65/paloaltonetworks-automation-examples.git
   cd paloaltonetworks-automation-examples/ansible/panos/create-security-policy
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

5. Choose an approach directory, update configuration, and run:

   ```bash
   cd 3-ansible-vault
   # Edit group_vars/panorama.yaml with your credentials
   # Edit host_vars/panorama.yaml with your rule parameters
   # Edit inventory.yaml with your Panorama hostname
   ansible-vault encrypt group_vars/panorama.yaml
   ansible-playbook playbook.yaml --ask-vault-pass
   ```

## Configuration

### Inventory

Each approach has its own `inventory.yaml`. Update the Panorama hostname:

```yaml
all:
  children:
    panorama:
      hosts:
        panorama.example.com:
```

Replace `panorama.example.com` with your Panorama's FQDN or IP. The hostname becomes the `ansible_host` value used by the `panos_security_rule` module's `provider.ip_address`.

### Credentials

For Approaches 2 and 3, create or edit `group_vars/all/credentials.yaml` (or `group_vars/panorama.yaml` as used in the source):

```yaml
panorama_credentials:
  username: "your-panorama-admin-username"
  password: "your-panorama-admin-password"
```

Encrypt with Ansible Vault to prevent plaintext secrets in version control:

```bash
ansible-vault encrypt group_vars/panorama.yaml
```

For Approach 1, credentials are inline in the playbook as placeholders. Replace them before running, or better yet, use Approach 3.

### Variables

| Variable | Location | Required | Description |
|----------|----------|----------|-------------|
| `panorama_credentials.username` | `group_vars/panorama.yaml` | Yes | Panorama admin username |
| `panorama_credentials.password` | `group_vars/panorama.yaml` | Yes | Panorama admin password |
| `security_rule.rule_name` | `host_vars/panorama.yaml` | Yes | Name of the security rule |
| `security_rule.description` | `host_vars/panorama.yaml` | Yes | Rule description |
| `security_rule.source_zone` | `host_vars/panorama.yaml` | Yes | List of source zones (e.g., `["DMZ"]`) |
| `security_rule.destination_zone` | `host_vars/panorama.yaml` | Yes | List of destination zones (e.g., `["WAN"]`) |
| `security_rule.source_ip` | `host_vars/panorama.yaml` | Yes | List of source IPs or `["any"]` |
| `security_rule.destination_ip` | `host_vars/panorama.yaml` | Yes | List of destination IPs or `["any"]` |
| `security_rule.application` | `host_vars/panorama.yaml` | Yes | List of applications (e.g., `["web-browsing"]`) |
| `security_rule.service` | `host_vars/panorama.yaml` | Yes | List of services (e.g., `["application-default"]`) |
| `security_rule.action` | `host_vars/panorama.yaml` | Yes | Rule action: `allow`, `deny`, or `drop` |
| `security_rule.device_group` | `host_vars/panorama.yaml` | Yes | Panorama device group name |

## Usage

### Basic Run (Approach 1 -- Simple)

```bash
cd 1-simple
ansible-playbook playbook.yaml
```

### Basic Run (Approach 2 -- Variable Files)

```bash
cd 2-variable-files
ansible-playbook playbook.yaml
```

### Basic Run (Approach 3 -- Ansible Vault)

```bash
cd 3-ansible-vault
ansible-playbook playbook.yaml --ask-vault-pass
```

### Dry Run

```bash
ansible-playbook playbook.yaml --check
```

Check mode simulates the playbook run without creating or modifying any security rules on Panorama. The `panos_security_rule` module reports whether it would create or update the rule.

### Variable Override

Override the rule action at runtime:

```bash
ansible-playbook playbook.yaml -e '{"security_rule": {"action": "deny"}}' --ask-vault-pass
```

### Verbose Debugging

```bash
ansible-playbook playbook.yaml -vvv --ask-vault-pass
```

### Expected Output

```
PLAY [Create Security Policy] **************************************************

TASK [Add test pre-rule to Panorama] *******************************************
changed: [panorama.example.com]

TASK [Print results to console] ************************************************
ok: [panorama.example.com] => {
    "msg": {
        "changed": true,
        "msg": "oobject was created"
    }
}

PLAY RECAP *********************************************************************
panorama.example.com       : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

- `ok=2` -- both tasks (create rule and print results) completed.
- `changed=1` -- the security rule was created on Panorama. On subsequent runs with identical parameters, this becomes `changed=0`.
- `failed=0` -- no errors. If Panorama rejects the rule, this counter increments.

## Project Structure

```
create-security-policy/
├── 1-simple/
│   ├── ansible.cfg                          # Ansible settings
│   ├── inventory.yaml                       # Panorama host
│   └── playbook.yaml                        # Credentials and rule params inline
├── 2-variable-files/
│   ├── ansible.cfg                          # Ansible settings
│   ├── inventory.yaml                       # Panorama host
│   ├── playbook.yaml                        # References variables from group/host vars
│   ├── group_vars/
│   │   └── panorama.yaml                   # Panorama credentials
│   └── host_vars/
│       └── panorama.yaml                   # Security rule parameters
├── 3-ansible-vault/
│   ├── ansible.cfg                          # Ansible settings
│   ├── inventory.yaml                       # Panorama host
│   ├── playbook.yaml                        # References variables from group/host vars
│   ├── group_vars/
│   │   └── panorama.yaml                   # Vault-encrypted Panorama credentials
│   └── host_vars/
│       └── panorama.yaml                   # Security rule parameters
└── README.md
```

## Troubleshooting

| Problem | Possible Cause | Solution |
|---------|---------------|----------|
| Connection refused to Panorama | Panorama management interface unreachable | Verify network connectivity and that HTTPS API is enabled |
| Invalid credentials / authentication failure | Wrong username or password | Update `group_vars/panorama.yaml` with correct credentials |
| Module not found: `paloaltonetworks.panos.panos_security_rule` | Collection not installed | Run `ansible-galaxy collection install paloaltonetworks.panos` |
| Timeout during API call | Panorama under heavy load or slow network | Increase `timeout` in `ansible.cfg` |
| Device group not found | Incorrect `device_group` value | Verify the device group name exists in Panorama and matches the variable exactly |
| Vault decryption error | Wrong vault password or file not encrypted | Re-encrypt with `ansible-vault encrypt` and provide the correct password |

## Ansible Concepts Used

- **Playbook**: A YAML file defining tasks to run against hosts. Each approach has its own `playbook.yaml` that creates a security rule and prints results.

- **Inventory**: A file listing hosts and groups. The `panorama` group contains the Panorama management appliance.

- **Module**: A unit of code Ansible executes. `paloaltonetworks.panos.panos_security_rule` creates or updates security policy rules. `ansible.builtin.debug` prints task results.

- **Collection**: A distribution format for Ansible content. `paloaltonetworks.panos` provides the `panos_security_rule` module.

- **Group Vars**: Variable files in `group_vars/` that apply to all hosts in a group. Approaches 2 and 3 store Panorama credentials in `group_vars/panorama.yaml`.

- **Host Vars**: Variable files in `host_vars/<hostname>/` that apply to a specific host. Approaches 2 and 3 define security rule parameters in `host_vars/panorama.yaml`.

- **Vault**: Ansible Vault encrypts sensitive files at rest. Approach 3 demonstrates encrypting `group_vars/panorama.yaml` and decrypting at runtime with `--ask-vault-pass`.

- **Check Mode**: A dry-run mode (`--check`) that shows what the playbook would change without creating rules on Panorama.
