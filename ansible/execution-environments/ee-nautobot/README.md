# Nautobot Ansible Execution Environment

## Overview

An Ansible Execution Environment (EE) is a container image that packages Ansible, collections, and all their dependencies into a single portable unit. This ensures that every automation run uses the exact same versions of everything, regardless of where it executes.

This EE is built for automating interactions with Nautobot, a network source of truth and automation platform. It bundles the `networktocode.nautobot` Ansible collection and the `pynautobot` Python SDK, giving you everything needed to manage devices, sites, circuits, and other Nautobot objects from Ansible playbooks.

## Prerequisites

- Python 3.11+
- Docker or Podman
- `ansible-builder` 3.0.1 (included in the Poetry environment)
- `ansible-navigator` (optional, for running playbooks with the built image)
- A running Nautobot instance with API access

## Quickstart

1. Clone the repository and navigate to this directory:

   ```bash
   git clone https://github.com/cdot65/paloaltonetworks-automation-examples.git
   cd paloaltonetworks-automation-examples/ansible/execution-environments/ee-nautobot
   ```

2. Install dependencies with Poetry:

   ```bash
   poetry install
   ```

3. Build the Execution Environment image:

   ```bash
   poetry run ansible-builder build --tag nautobot-ee:latest
   ```

4. Run a playbook using the image:

   ```bash
   ansible-navigator run your-playbook.yml --eei nautobot-ee:latest
   ```

## Configuration

### execution-environment.yml

This is the primary configuration file that `ansible-builder` reads. It defines:

- **Base image**: `quay.io/fedora/fedora:latest`
- **ansible-core**: installed via pip
- **ansible-runner**: installed via pip
- **System packages**: `openssh-clients`, `sshpass`
- **Python packages**: `pynautobot`
- **Galaxy collections**: sourced from `requirements.yml`

### requirements.yml

Specifies Ansible Galaxy collections to install in the image:

| Collection | Version |
|------------|---------|
| `networktocode.nautobot` | 4.1.1 |

## Usage

### Building the Image

```bash
# Using Poetry (recommended)
poetry run ansible-builder build --tag nautobot-ee:latest

# Or if ansible-builder is installed globally
ansible-builder build --tag nautobot-ee:latest
```

### Running Playbooks

When using this EE with Nautobot modules, you typically need to provide the Nautobot URL and API token. Pass these as extra variables or environment variables -- never hardcode them.

```bash
# With ansible-navigator (interactive mode)
ansible-navigator run playbook.yml --eei nautobot-ee:latest

# With ansible-navigator (stdout mode)
ansible-navigator run playbook.yml --eei nautobot-ee:latest -m stdout

# Passing Nautobot connection details
ansible-navigator run playbook.yml --eei nautobot-ee:latest \
  -e nautobot_url=https://nautobot.example.com \
  -e nautobot_token=YOUR_API_TOKEN

# With ansible-runner
ansible-runner run /path/to/project --container-image nautobot-ee:latest
```

## What's Included

| Category | Packages |
|----------|----------|
| Ansible | `ansible-core`, `ansible-runner` |
| Collections | `networktocode.nautobot` 4.1.1 |
| Python | `pynautobot` |
| System | `openssh-clients`, `sshpass` |
| Base Image | `quay.io/fedora/fedora:latest` |

## Project Structure

```
.
├── execution-environment.yml   # EE definition: base image, deps
├── requirements.yml            # Ansible Galaxy collections to include
└── pyproject.toml              # Poetry config for ansible-builder 3.0.1
```

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| `ansible-builder: command not found` | ansible-builder not installed | Run `poetry install` first, then use `poetry run ansible-builder` |
| Build fails pulling base image | No access to `quay.io` or network issue | Check internet connectivity; try `podman pull quay.io/fedora/fedora:latest` manually |
| Nautobot modules return 403 | Invalid or expired API token | Verify your `nautobot_token` value and that the token has sufficient permissions |
| `pynautobot` import errors at runtime | Image was not built correctly | Rebuild with `ansible-builder build --tag nautobot-ee:latest` and check for build errors |
| Collection version conflict | Galaxy dependency resolution failure | Pin compatible versions in `requirements.yml` and rebuild |
