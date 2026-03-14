# Event-Driven Ansible Container for PAN-OS Log Remediation

## Overview

This project provides a containerized Event-Driven Ansible (EDA) environment that listens for PAN-OS firewall log events over HTTP and triggers automated remediation playbooks. The container runs an `ansible-rulebook` process that receives logs forwarded from a PAN-OS HTTP Server Profile on port 5000, then reacts based on log type:

- **Decryption logs** -- trigger a TLS remediation playbook that forwards event details to Ansible Automation Platform (AAP)
- **Data (DLP) logs** -- trigger a Slack alert playbook
- **System logs** -- trigger a ServiceNow ticket creation playbook

Use this when you want event-driven, automated responses to PAN-OS firewall events without manual intervention.

## Prerequisites

- Docker or Podman installed
- Python 3.11+ with the `invoke` package (`pip install invoke`)
- A PAN-OS firewall with an HTTP Server Profile configured to forward logs to this container
- Access to Ansible Automation Platform (for the TLS remediation workflow)
- An AAP bearer token for API authentication

## Quickstart

1. Clone the repository and navigate to this directory:

   ```bash
   git clone https://github.com/cdot65/paloaltonetworks-automation-examples.git
   cd paloaltonetworks-automation-examples/ansible/event-driven-ansible
   ```

2. Install the Python task runner:

   ```bash
   pip install invoke
   ```

3. Build the container image:

   ```bash
   invoke build
   ```

4. Start the container (listens on port 5000):

   ```bash
   invoke up
   ```

5. Configure your PAN-OS firewall to forward logs to `http://<container-host>:5000`.

## Configuration

### Files to Update

| File | What to Change |
|------|----------------|
| `roles/tls_remediation/defaults/main.yml` | Replace `aap_token` with your AAP bearer token |
| `roles/tls_remediation/tasks/main.yml` | Update the AAP URL (`https://ansible.awx.example.com/api/v2/job_templates/20/launch/`) to your actual job template endpoint |
| `inventory/inventory.yaml` | Add or modify target hosts (defaults to localhost) |
| `rulebooks/rulebook.yaml` | Adjust log type conditions or playbook paths for your environment |

### Environment Variables

The container sets:

- `JAVA_HOME=/usr/lib/jvm/jre-17-openjdk` -- required by ansible-rulebook's JPY dependency

### Mounted Volumes

When the container starts via `invoke up`, the following host directories are mounted:

| Host Path | Container Path | Purpose |
|-----------|---------------|---------|
| `./collections` | `/usr/share/ansible/collections` | Ansible collections |
| `./roles` | `/usr/share/ansible/roles` | Ansible roles |
| `./plugins` | `/usr/share/ansible/plugins` | Ansible plugins |
| `./` (project root) | `/ansible/eda` | Rulebooks, playbooks, inventory |

## Usage

All lifecycle commands use the `invoke` task runner, which auto-detects Docker or Podman:

```bash
# Build the container image
invoke build

# Start the EDA container (detached, port 5000 exposed)
invoke up

# Tail the container logs to see incoming events
invoke logs

# Open an interactive shell inside the container
invoke shell

# Stop and remove the container
invoke down
```

### PAN-OS HTTP Server Profile

On your PAN-OS firewall, create an HTTP Server Profile that forwards decryption, data, and/or system logs to `http://<container-host>:5000`. The EDA rulebook listens on `0.0.0.0:5000` and routes events by log type.

## What's Included

The container image (Fedora-based) includes:

- **Java 17** (OpenJDK) -- required by ansible-rulebook
- **Python 3.12** with pip
- **ansible** and **ansible-runner**
- **ansible-rulebook** (built with JPY from source)
- **aiohttp** 3.9.0b0
- **pan-os-python** SDK
- **xmltodict**
- **paloaltonetworks.panos** Ansible collection
- Development tools (GCC, libffi-devel, openssl-devel)

## Project Structure

```
.
├── docker/
│   └── Dockerfile               # Fedora-based image: Java 17, ansible-rulebook, PAN-OS deps
├── collections/
│   └── requirements.yml         # Galaxy collection dependencies (containers.podman)
├── inventory/
│   └── inventory.yaml           # Target hosts (default: localhost)
├── playbooks/
│   └── playbook.yaml            # Main playbook that imports the tls_remediation role
├── roles/
│   └── tls_remediation/
│       ├── defaults/main.yml    # AAP token placeholder
│       └── tasks/main.yml       # POSTs event data to AAP job template API
├── rulebooks/
│   └── rulebook.yaml            # EDA rules: decryption, DLP, and system log handlers
└── tasks.py                     # Invoke tasks: build, up, down, logs, shell, publish
```

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| `Neither podman nor docker is installed` error | Invoke cannot find a container runtime | Install Docker or Podman and ensure it is on your PATH |
| Container starts but no events arrive | PAN-OS HTTP Server Profile misconfigured | Verify the profile points to `http://<container-host>:5000` and the correct log types are selected |
| `ansible-rulebook` crashes on startup | Java not found or wrong version | Confirm the image built successfully; rebuild with `invoke build` if needed |
| AAP job template returns 401/403 | Invalid or expired `aap_token` | Update the token in `roles/tls_remediation/defaults/main.yml` |
| Port 5000 already in use | Another process is binding port 5000 | Stop the conflicting process or change the port in both the rulebook and the `invoke up` command in `tasks.py` |
