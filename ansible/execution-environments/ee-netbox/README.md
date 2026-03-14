# NetBox Ansible Execution Environment

## Overview

An Ansible Execution Environment (EE) is a container image that packages Ansible, collections, and all their dependencies into a single portable unit. This ensures that every automation run uses the exact same versions of everything, regardless of where it executes.

This EE is built for automating interactions with NetBox, a network source of truth and IPAM (IP Address Management) platform. It bundles the `netbox.netbox` Ansible collection along with the `pynetbox` and `pytz` Python packages, providing everything needed to manage devices, IP addresses, prefixes, sites, and other NetBox objects from Ansible playbooks.

## Prerequisites

- Python 3.11+
- Docker or Podman
- `ansible-builder` 3.0.1 (included in the Poetry environment)
- `ansible-navigator` (optional, for running playbooks with the built image)
- A running NetBox instance with API access

## Quickstart

1. Clone the repository and navigate to this directory:

   ```bash
   git clone https://github.com/cdot65/paloaltonetworks-automation-examples.git
   cd paloaltonetworks-automation-examples/ansible/execution-environments/ee-netbox
   ```

2. Install dependencies with Poetry:

   ```bash
   poetry install
   ```

3. Build the Execution Environment image:

   ```bash
   poetry run ansible-builder build --tag netbox-ee:latest
   ```

4. Run a playbook using the image:

   ```bash
   ansible-navigator run your-playbook.yml --eei netbox-ee:latest
   ```

## Configuration

### execution-environment.yml

This is the primary configuration file that `ansible-builder` reads. It defines:

- **Base image**: `quay.io/fedora/fedora:latest`
- **ansible-core**: installed via pip
- **ansible-runner**: installed via pip
- **System packages**: `openssh-clients`, `sshpass`
- **Python packages**: `pynetbox`, `pytz`
- **Galaxy collections**: sourced from `requirements.yml`

### requirements.yml

Specifies Ansible Galaxy collections to install in the image:

| Collection | Version |
|------------|---------|
| `netbox.netbox` | 3.18.0 |

## Usage

### Building the Image

```bash
# Using Poetry (recommended)
poetry run ansible-builder build --tag netbox-ee:latest

# Or if ansible-builder is installed globally
ansible-builder build --tag netbox-ee:latest
```

### Running Playbooks

When using this EE with NetBox modules, you typically need to provide the NetBox URL and API token. Pass these as extra variables or environment variables -- never hardcode them.

```bash
# With ansible-navigator (interactive mode)
ansible-navigator run playbook.yml --eei netbox-ee:latest

# With ansible-navigator (stdout mode)
ansible-navigator run playbook.yml --eei netbox-ee:latest -m stdout

# Passing NetBox connection details
ansible-navigator run playbook.yml --eei netbox-ee:latest \
  -e netbox_url=https://netbox.example.com \
  -e netbox_token=YOUR_API_TOKEN

# With ansible-runner
ansible-runner run /path/to/project --container-image netbox-ee:latest
```

## What's Included

| Category | Packages |
|----------|----------|
| Ansible | `ansible-core`, `ansible-runner` |
| Collections | `netbox.netbox` 3.18.0 |
| Python | `pynetbox`, `pytz` |
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
| NetBox modules return 403 | Invalid or expired API token | Verify your `netbox_token` value and that the token has sufficient permissions |
| `pynetbox` import errors at runtime | Image was not built correctly | Rebuild with `ansible-builder build --tag netbox-ee:latest` and check for build errors |
| Timezone-related errors | `pytz` not loaded or incorrect timezone string | Confirm the image includes `pytz`; verify timezone strings match IANA format (e.g., `America/New_York`) |
