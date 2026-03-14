# PAN-OS Ansible Execution Environment

## Overview

An Ansible Execution Environment (EE) is a container image that packages Ansible, collections, and all their dependencies into a single portable unit. This ensures that every automation run uses the exact same versions of everything, regardless of where it executes.

This EE is purpose-built for automating Palo Alto Networks firewalls and Panorama. It bundles the `paloaltonetworks.panos` collection, the `pan-os-python` SDK, and supporting tools so you can run PAN-OS playbooks consistently across local machines, CI/CD pipelines, and Ansible Automation Platform.

## Prerequisites

- Python 3.11+
- Docker or Podman
- `ansible-builder` 3.0.1 (included in the Poetry environment)
- `ansible-navigator` (optional, for running playbooks with the built image)

## Quickstart

1. Clone the repository and navigate to this directory:

   ```bash
   git clone https://github.com/cdot65/paloaltonetworks-automation-examples.git
   cd paloaltonetworks-automation-examples/ansible/execution-environments/ee-ansible
   ```

2. Install dependencies with Poetry:

   ```bash
   poetry install
   ```

3. Build the Execution Environment image:

   ```bash
   poetry run ansible-builder build --tag panos-ee:latest
   ```

4. Run a playbook using the image:

   ```bash
   ansible-navigator run your-playbook.yml --eei panos-ee:latest
   ```

## Configuration

### execution-environment.yml

This is the primary configuration file that `ansible-builder` reads. It defines:

- **Base image**: `quay.io/fedora/fedora:latest`
- **ansible-core**: installed via pip
- **ansible-runner**: installed via pip
- **System packages**: `openssh-clients`, `sshpass`, `curl`
- **Python packages**: `xmltodict`
- **Galaxy collections**: sourced from `requirements.yml`
- **Additional build steps**: installs `pan-os-python` v1.11.0 from GitHub

### requirements.yml

Specifies Ansible Galaxy collections to install in the image:

| Collection | Version |
|------------|---------|
| `paloaltonetworks.panos` | 2.17.0 |
| `community.general` | 8.0.2 |

### bindep.txt

Lists system-level binary dependencies resolved by the package manager:

- `curl`

## Usage

### Building the Image

```bash
# Using Poetry (recommended)
poetry run ansible-builder build --tag panos-ee:latest

# Or if ansible-builder is installed globally
ansible-builder build --tag panos-ee:latest
```

The build process creates a container image with all dependencies baked in. This can take several minutes on the first run.

### Running Playbooks

```bash
# With ansible-navigator (interactive mode)
ansible-navigator run playbook.yml --eei panos-ee:latest

# With ansible-navigator (stdout mode, non-interactive)
ansible-navigator run playbook.yml --eei panos-ee:latest -m stdout

# With ansible-runner
ansible-runner run /path/to/project --container-image panos-ee:latest
```

## What's Included

| Category | Packages |
|----------|----------|
| Ansible | `ansible-core`, `ansible-runner` |
| Collections | `paloaltonetworks.panos` 2.17.0, `community.general` 8.0.2 |
| Python | `pan-os-python` 1.11.0, `xmltodict` |
| System | `openssh-clients`, `sshpass`, `curl` |
| Base Image | `quay.io/fedora/fedora:latest` |

## Project Structure

```
.
├── execution-environment.yml   # EE definition: base image, deps, build steps
├── requirements.yml            # Ansible Galaxy collections to include
├── bindep.txt                  # System-level package dependencies
└── pyproject.toml              # Poetry config for ansible-builder 3.0.1
```

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| `ansible-builder: command not found` | ansible-builder not installed | Run `poetry install` first, then use `poetry run ansible-builder` |
| Build fails pulling base image | No access to `quay.io` or network issue | Check internet connectivity; try `podman pull quay.io/fedora/fedora:latest` manually |
| `pan-os-python` install step fails | GitHub archive URL unreachable | Check network access to `github.com`; the build downloads the SDK tarball directly |
| `ansible-navigator` cannot find the image | Image tag mismatch | Verify the tag used in `--eei` matches what you passed to `ansible-builder build --tag` |
| SSH connection failures in playbooks | Missing SSH keys in the container | Mount your SSH key directory or use `--extra-vars` to pass credentials |
