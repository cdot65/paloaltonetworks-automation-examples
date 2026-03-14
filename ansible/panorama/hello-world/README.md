# Ansible Hello World Example

## Overview

This project is a minimal Ansible example intended as a starting point for beginners. It defines a simple playbook that prints a "Hello World!" message to the console using the built-in `debug` module. No external collections or network devices are required -- the playbook runs entirely on the local machine. It also demonstrates basic Ansible concepts like variables, tags, and handlers.

## Prerequisites

- Python 3.6 or later
- Ansible 2.10 or later
- No additional collections required (uses only built-in Ansible modules)

## Quickstart

1. Clone the repository and navigate to this project:

   ```bash
   git clone https://github.com/cdot65/paloaltonetworks-automation-examples.git
   cd paloaltonetworks-automation-examples/ansible/panorama/hello-world
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

4. Run the playbook:

   ```bash
   ansible-playbook hello.yaml
   ```

## Configuration

### Inventory

The inventory file `inventory.yaml` defines a single localhost target:

```yaml
all:
  hosts:
    localhost:
      ansible_connection: local
```

The `ansible_connection: local` setting tells Ansible to run tasks directly on the local machine rather than connecting via SSH. No remote hosts are needed for this example.

### Credentials

No credentials are required for this project since it runs locally and does not connect to any external systems.

To follow the standard pattern for projects that do require credentials, you would create `group_vars/all/credentials.yaml`:

```yaml
---
# No credentials needed for this example
```

To encrypt a credentials file with Ansible Vault:

```bash
ansible-vault encrypt group_vars/all/credentials.yaml
```

### Variables

| Variable | Location | Required | Description |
|---|---|---|---|
| `message` | `hello.yaml` (vars section) | No | The message to print to the console (defaults to "Hello World!") |
| `ansible_connection` | `inventory.yaml` | Yes | Set to `local` to run tasks on the control machine |

## Usage

**Basic run:**

```bash
ansible-playbook hello.yaml
```

**Dry run (check mode):**

```bash
ansible-playbook hello.yaml --check
```

Check mode simulates the playbook run without making any changes. Since the `debug` module only prints output and makes no system changes, the behavior is identical to a normal run.

**Override the message at runtime:**

```bash
ansible-playbook hello.yaml -e "message='Goodbye World!'"
```

**Run only tasks with a specific tag:**

```bash
ansible-playbook hello.yaml --tags debug
```

**Verbose debugging output:**

```bash
ansible-playbook hello.yaml -vvv
```

### Expected Output

A successful run will produce output similar to:

```
PLAY [Hello World Sample] ******************************************************

TASK [Gathering Facts] *********************************************************
ok: [localhost]

TASK [Hello Message] ***********************************************************
ok: [localhost] => {
    "msg": "Hello World!"
}

PLAY RECAP *********************************************************************
localhost                  : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

## Project Structure

```
hello-world/
├── ansible.cfg              # Ansible configuration (inventory path, basic settings)
├── hello.yaml               # Main playbook that prints a Hello World message
├── inventory.yaml           # Localhost inventory definition
└── README.md                # This file
```

## Troubleshooting

| Problem | Possible Cause | Solution |
|---|---|---|
| Connection refused | Should not occur since this runs locally | Ensure `ansible_connection: local` is set in `inventory.yaml` |
| Invalid credentials | Not applicable to this project | No credentials are needed for this example |
| Module not found: `debug` | Ansible is not installed or not on PATH | Run `pip install ansible` and verify with `ansible --version` |
| Timeout error | Should not occur for local execution | Ensure no proxy or firewall is interfering with local connections |
| "No hosts matched" warning | Inventory file not found or misconfigured | Verify `ansible.cfg` points to the correct `inventory.yaml` path |

## Ansible Concepts Used

- **Playbook**: A YAML file that defines a set of tasks to be executed on target hosts. `hello.yaml` is the main entry point for this project.
- **Inventory**: A file (`inventory.yaml`) that lists the hosts Ansible will manage. This example targets only `localhost`.
- **Module**: A unit of work in Ansible. This project uses the built-in `debug` module to print messages to the console.
- **Variables (vars)**: Values defined in the `vars` section of a play that can be referenced in tasks using `{{ variable_name }}` syntax. The `message` variable is defined this way.
- **Tags**: Labels applied to tasks that let you selectively run specific parts of a playbook using the `--tags` flag. The "Hello Message" task is tagged with `debug`.
- **Handlers**: Special tasks that only run when notified by another task. This playbook defines a handler called "Print done" that listens for the "done" notification. Handlers are commonly used for actions like restarting services after a configuration change.
- **Check Mode**: Running a playbook with `--check` simulates execution without making changes. Useful for validating playbook logic before applying.
