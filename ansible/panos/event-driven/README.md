# Event-Driven Ansible for PAN-OS Log-Triggered Remediation

## Overview

This project uses Event-Driven Ansible (EDA) to listen for log events forwarded from Palo Alto Networks PAN-OS firewalls via HTTP Server Profiles and trigger automated remediation playbooks. The `paloaltonetworks.panos` collection provides a `logs` source plugin that receives decryption, DLP (data), and system log events on a configurable port. When a matching event arrives, the EDA rulebook dispatches a corresponding playbook. The included `tls_remediation` role forwards decryption failure event details to an Ansible Automation Platform (AAP) job template via its REST API. A Docker/Podman container image and Python Invoke task runner simplify deployment and lifecycle management.

## Prerequisites

- Python 3.12+
- Ansible Core 2.15+
- Java 17 (OpenJDK) -- required by `ansible-rulebook`
- `ansible-rulebook`, `pan-os-python`, `xmltodict` Python packages
- Docker or Podman
- Collections: `paloaltonetworks.panos`, `containers.podman`
- Network access from PAN-OS firewall to the EDA listener on port 5000
- (Optional) Ansible Automation Platform instance with a valid API bearer token

## Quickstart

1. Clone the repository and navigate to the project directory:

   ```bash
   git clone https://github.com/cdot65/paloaltonetworks-automation-examples.git
   cd paloaltonetworks-automation-examples/ansible/panos/event-driven
   ```

2. Create and activate a Python virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install Python dependencies:

   ```bash
   pip install ansible ansible-runner ansible-rulebook pan-os-python xmltodict invoke
   ```

4. Install required Ansible collections:

   ```bash
   ansible-galaxy collection install paloaltonetworks.panos containers.podman
   ```

5. Create the credentials file (see Configuration below):

   ```bash
   mkdir -p group_vars/all
   # Edit group_vars/all/credentials.yaml with your AAP token
   ```

6. Run with the container approach:

   ```bash
   invoke build
   invoke up
   invoke logs
   ```

   Or run directly without a container:

   ```bash
   ansible-rulebook --rulebook=rulebooks/rulebook.yaml -i inventory/inventory.yaml --verbose
   ```

## Configuration

### Inventory

The inventory at `inventory/inventory.yaml` defines the EDA controller host:

```yaml
all:
  hosts:
    localhost:
      ansible_connection: local
```

The `ansible_host` value is implicit as `localhost`. Since the EDA listener runs locally, `ansible_connection: local` avoids SSH overhead.

### Credentials

Create `group_vars/all/credentials.yaml` with your Ansible Automation Platform bearer token:

```yaml
aap_token: "your-aap-bearer-token-here"
```

Encrypt the file with Ansible Vault to keep secrets out of version control:

```bash
ansible-vault encrypt group_vars/all/credentials.yaml
```

You must also update the AAP job template URL in `roles/tls_remediation/tasks/main.yml` to match your environment.

### Variables

| Variable | Location | Required | Description |
|----------|----------|----------|-------------|
| `aap_token` | `group_vars/all/credentials.yaml` | Yes | Bearer token for Ansible Automation Platform REST API |
| `host` | `rulebooks/rulebook.yaml` | Yes | Listen address for incoming logs (default `0.0.0.0`) |
| `port` | `rulebooks/rulebook.yaml` | Yes | Listen port for incoming logs (default `5000`) |
| `type` | `rulebooks/rulebook.yaml` | Yes | Log type filter (default `decryption`) |
| `ansible_connection` | `inventory/inventory.yaml` | Yes | Must be `local` for the EDA controller |

## Usage

### Basic Run

```bash
ansible-rulebook --rulebook=rulebooks/rulebook.yaml -i inventory/inventory.yaml --verbose
```

### Dry Run

EDA does not support `--check` mode directly. To test the underlying remediation playbook in check mode:

```bash
ansible-playbook playbooks/playbook.yaml --check
```

Check mode simulates the playbook run without making actual changes. Tasks using the `uri` module (API calls) will be skipped since they cannot be simulated.

### Variable Override

```bash
ansible-rulebook --rulebook=rulebooks/rulebook.yaml -i inventory/inventory.yaml -e "aap_token=my-new-token"
```

### Verbose Debugging

```bash
ansible-rulebook --rulebook=rulebooks/rulebook.yaml -i inventory/inventory.yaml -vvv
```

### Expected Output

When a decryption log event arrives and the TLS remediation playbook triggers:

```
PLAY [Copy Certificates to Remote Hosts] **************************************

TASK [Collect System Facts] ****************************************************
ok: [localhost]

TASK [tls_remediation : Debug all vars] ****************************************
ok: [localhost]

TASK [tls_remediation : Execute Job Template on Ansible Automation Platform] ***
changed: [localhost]

TASK [tls_remediation : Output job result] *************************************
ok: [localhost]

PLAY RECAP *********************************************************************
localhost                  : ok=4    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

- `ok=4` -- all four tasks completed successfully.
- `changed=1` -- the AAP job template was launched (the API call returned HTTP 201).
- `failed=0` -- no errors occurred. If the API call fails, this counter increments.

## Project Structure

```
event-driven/
├── collections/
│   └── requirements.yml              # Required Ansible collections
├── docker/
│   └── Dockerfile                    # Fedora-based image with Java 17, Python 3.12, EDA
├── group_vars/
│   └── all/
│       └── credentials.yaml          # AAP bearer token (encrypt with Vault)
├── inventory/
│   └── inventory.yaml                # Localhost inventory for EDA controller
├── playbooks/
│   └── playbook.yaml                 # Remediation playbook importing tls_remediation role
├── roles/
│   └── tls_remediation/
│       ├── defaults/
│       │   └── main.yml              # Default variable values (token placeholder)
│       └── tasks/
│           └── main.yml              # Debug event data, POST to AAP job template API
├── rulebooks/
│   └── rulebook.yaml                 # EDA rulebook: log sources, conditions, actions
└── tasks.py                          # Invoke tasks: build, up, down, logs, shell
```

## Troubleshooting

| Problem | Possible Cause | Solution |
|---------|---------------|----------|
| Connection refused on port 5000 | EDA listener not running or port blocked by host firewall | Verify container is running (`invoke logs`); check host firewall rules allow inbound TCP 5000 |
| Invalid credentials / HTTP 401 from AAP | Incorrect or expired `aap_token` | Regenerate the bearer token in AAP and update `group_vars/all/credentials.yaml` |
| Module not found: `paloaltonetworks.panos.logs` | PAN-OS collection not installed or outdated | Run `ansible-galaxy collection install paloaltonetworks.panos --force` |
| Timeout -- no events received | PAN-OS HTTP Server Profile not pointing to EDA host | In PAN-OS, verify the HTTP Server Profile destination IP and port match the EDA listener |
| Java not found / `jpy` build error | Missing Java 17 or development headers | Install OpenJDK 17; set `JAVA_HOME=/usr/lib/jvm/jre-17-openjdk` |
| Container build fails with "command not found" | Neither Docker nor Podman installed | Install Docker or Podman and ensure the binary is in your `PATH` |

## Ansible Concepts Used

- **Playbook**: A YAML file defining tasks to execute on hosts. `playbooks/playbook.yaml` gathers system facts and imports the `tls_remediation` role.

- **Inventory**: A file listing the hosts Ansible manages. This project uses a single `localhost` entry with a local connection since EDA runs on the control node.

- **Role**: A reusable, self-contained unit of Ansible content with its own tasks, defaults, and directory structure. The `tls_remediation` role packages the API call logic and default variables.

- **Module**: A unit of code Ansible runs on hosts. This project uses `ansible.builtin.setup` (gather facts), `ansible.builtin.uri` (HTTP requests to AAP), `ansible.builtin.debug` (print variables), and `ansible.builtin.import_role` (include a role).

- **Collection**: A distribution format for Ansible content (modules, roles, plugins). `paloaltonetworks.panos` provides the `logs` EDA source plugin and PAN-OS modules. `containers.podman` provides container management modules.

- **Event-Driven Ansible (EDA)**: A framework that watches for external events and automatically triggers Ansible actions based on rules. It requires `ansible-rulebook` and Java.

- **Rulebook**: An EDA-specific YAML file defining sources (where events come from), conditions (what to match), and actions (what to run). This project's rulebook listens for three log types and dispatches different playbooks for each.

- **Group Vars**: Variable files in `group_vars/` that apply to all hosts in a group. Credentials are stored here to separate secrets from playbook logic.

- **Vault**: Ansible Vault encrypts sensitive data (tokens, passwords) at rest. Run `ansible-vault encrypt <file>` to protect credentials files and `--ask-vault-pass` at runtime to decrypt.

- **Check Mode**: A dry-run mode (`--check`) that shows what changes a playbook would make without actually applying them. Not directly supported by EDA, but usable with individual playbooks.
