# Distribute TLS Decryption Certificates from PAN-OS to Endpoints

## Overview

This Ansible playbook exports TLS decryption certificates from a Palo Alto Networks firewall and deploys them to endpoint trust stores on RHEL and Windows machines. It uses the `paloaltonetworks.panos` collection to export three certificates (GlobalSign Root CA, Root CA, and Forward-Trust-CA-ECDSA) in PEM format. Three roles handle the workflow: the `panos` role exports certificates from the firewall to the local filesystem, the `rhel` role copies the Forward-Trust-CA-ECDSA certificate to the RHEL trust store and runs `update-ca-trust`, and the `windows` role imports the Root CA certificate into the Windows Trusted Root certificate store.

## Prerequisites

- Python 3.8 or later
- Ansible 2.12 or later
- The `paloaltonetworks.panos` Ansible collection
- The `community.general` Ansible collection
- The `ansible.windows` Ansible collection (for Windows targets)
- The `pan-os-python` and `pywinrm` Python libraries
- Username/password access to a PAN-OS firewall
- SSH access to RHEL endpoints and WinRM access to Windows endpoints
- Root/Administrator privileges on target endpoints for certificate installation

## Quickstart

1. Clone the repository and navigate to this project:

   ```bash
   git clone https://github.com/cdot65/paloaltonetworks-automation-examples.git
   cd paloaltonetworks-automation-examples/ansible/panos/tls-decryption-remediation
   ```

2. Create and activate a Python virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install Ansible and required Python packages:

   ```bash
   pip install ansible pan-os-python pywinrm
   ```

4. Install the required Ansible collections:

   ```bash
   ansible-galaxy collection install -r collections/requirements.yml
   ansible-galaxy collection install ansible.windows
   ```

5. Create `inventory.yaml` and `group_vars/all/credentials.yaml` (see Configuration below).

6. Run the playbook:

   ```bash
   ansible-playbook playbook.yaml -e "target_server=my-rhel-server"
   ```

## Configuration

### Inventory

Create an `inventory.yaml` file in the project root. The first play runs on `localhost` to export certificates from the firewall. The second play targets whichever host matches the `target_server` variable, applying the appropriate role based on the detected OS family.

```yaml
all:
  hosts:
    rhel-workstation-01:
      ansible_host: 192.168.1.10
      ansible_user: admin
    win-workstation-01:
      ansible_host: 192.168.1.20
      ansible_connection: winrm
      ansible_winrm_transport: ntlm
      ansible_user: Administrator
```

Replace the hostnames and IPs with your actual endpoint details.

### Credentials

Store firewall credentials in `group_vars/all/credentials.yaml` rather than in role defaults. Create the `group_vars/all/` directory if it does not exist.

```yaml
---
panos_username: "your-firewall-username"
panos_password: "your-firewall-password"
panos_firewall: "firewall.example.com"
```

Encrypt sensitive files with Ansible Vault:

```bash
ansible-vault encrypt group_vars/all/credentials.yaml
```

### Variables

| Variable            | Location                          | Required | Description                                                        |
|---------------------|-----------------------------------|----------|--------------------------------------------------------------------|
| `panos_username`    | `group_vars/all/credentials.yaml` | Yes      | Username for PAN-OS API authentication                             |
| `panos_password`    | `group_vars/all/credentials.yaml` | Yes      | Password for PAN-OS API authentication                             |
| `panos_firewall`    | `group_vars/all/credentials.yaml` | Yes      | FQDN or IP of the PAN-OS firewall                                 |
| `target_server`     | Extra vars (`-e`)                 | Yes      | Inventory hostname of the endpoint to receive the certificate      |

## Usage

**Basic run (deploy to a specific RHEL server):**

```bash
ansible-playbook playbook.yaml -e "target_server=rhel-workstation-01"
```

**Basic run (deploy to a Windows machine):**

```bash
ansible-playbook playbook.yaml -e "target_server=win-workstation-01"
```

**Dry run (check mode):**

```bash
ansible-playbook playbook.yaml --check -e "target_server=rhel-workstation-01"
```

Check mode simulates the playbook without making changes. Certificate export and file copy tasks will be skipped, allowing you to verify connectivity and variable resolution before modifying anything.

**Override variables at runtime:**

```bash
ansible-playbook playbook.yaml -e "target_server=rhel-workstation-01 panos_firewall=10.0.0.1"
```

**Verbose debugging:**

```bash
ansible-playbook playbook.yaml -vvv -e "target_server=rhel-workstation-01"
```

### Expected Output

```
PLAY [Pull Firewall Certificate] ***********************************************

TASK [Export GlobalSign-Root-CA] ************************************************
changed: [localhost]

TASK [Read file contents of /var/tmp/GlobalSign-Root-CA.pem] *******************
ok: [localhost]

TASK [Export Root CA] **********************************************************
changed: [localhost]

TASK [Read file contents of /var/tmp/Root-CA.pem] ******************************
ok: [localhost]

TASK [Export Forward-Trust-CA-ECDSA certificate] ********************************
changed: [localhost]

TASK [Read file contents of /var/tmp/Forward-Trust-CA-ECDSA.pem] ***************
ok: [localhost]

PLAY [Push Certificate to Server] **********************************************

TASK [Gathering Facts] *********************************************************
ok: [rhel-workstation-01]

TASK [Copy Forward-Trust-CA-ECDSA Certificate to Remote Server] ****************
changed: [rhel-workstation-01]

TASK [Update Certificate Trust] ************************************************
changed: [rhel-workstation-01]

PLAY RECAP *********************************************************************
localhost                  : ok=6    changed=3    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
rhel-workstation-01        : ok=3    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

The first play shows `changed=3` for the three certificate exports from the firewall. The second play shows `changed=2` for copying the certificate file and updating the system trust store on the RHEL endpoint.

## Project Structure

```
tls-decryption-remediation/
├── ansible.cfg                            # Ansible configuration (roles path, inventory)
├── collections/
│   └── requirements.yml                   # Required Ansible collections list
├── playbook.yaml                          # Main playbook (export certs, then push to endpoints)
└── roles/
    ├── panos/
    │   ├── defaults/
    │   │   └── main.yaml                  # Default variables (firewall credentials)
    │   └── tasks/
    │       └── main.yml                   # Export certificates from PAN-OS firewall
    ├── rhel/
    │   └── tasks/
    │       └── main.yml                   # Copy cert and update trust store on RHEL
    └── windows/
        └── tasks/
            └── main.yml                   # Copy cert and import to Windows trust store
```

## Troubleshooting

| Problem                             | Possible Cause                                     | Solution                                                                  |
|------------------------------------|----------------------------------------------------|---------------------------------------------------------------------------|
| Connection refused                  | Firewall or endpoint is unreachable                | Verify network connectivity and hostnames in `inventory.yaml`             |
| Invalid credentials                 | Firewall username/password is incorrect             | Update credentials in `group_vars/all/credentials.yaml`                   |
| Module not found                    | `paloaltonetworks.panos` collection not installed   | Run `ansible-galaxy collection install -r collections/requirements.yml`   |
| Timeout                             | Firewall or endpoint is slow to respond             | Increase `timeout` in `ansible.cfg`                                       |
| Certificate not found on firewall   | Certificate name does not match exactly             | Verify exact certificate names in the PAN-OS GUI under Device > Certificates |
| Permission denied on RHEL           | Not running with elevated privileges               | Ensure `become: true` is set in the RHEL role tasks (it is by default)    |
| WinRM connection failure            | WinRM not configured on the Windows target          | Enable WinRM on the target and install `pywinrm` (`pip install pywinrm`) |
| `target_server` not set             | Missing required extra variable                    | Pass `-e "target_server=hostname"` when running the playbook              |

## Ansible Concepts Used

- **Playbook**: A YAML file defining plays. `playbook.yaml` contains two plays: one runs locally to export certificates from the firewall, and one targets endpoints to install them.
- **Inventory**: Defines target hosts. You must create `inventory.yaml` listing the RHEL and/or Windows endpoints that will receive certificates.
- **Role**: A reusable, structured set of tasks organized into a standard directory layout. Three roles divide the work: `panos` (export), `rhel` (Linux trust store install), and `windows` (Windows trust store import).
- **Role Defaults**: Variables defined in `roles/<name>/defaults/main.yaml`. These have the lowest precedence and can be overridden by group vars, extra vars, or any other variable source.
- **Module**: Reusable units of work. `panos_export` exports certificates from PAN-OS. `slurp` reads file contents. `copy` transfers files to RHEL. `win_copy` and `win_certificate_store` handle Windows certificate deployment.
- **Collection**: A packaged set of modules, roles, and plugins. `paloaltonetworks.panos` provides firewall modules. `ansible.windows` provides Windows modules. `community.general` provides utility modules.
- **Group Vars**: Variables shared across all hosts. Store firewall credentials in `group_vars/all/credentials.yaml` for centralized, secure management.
- **Block/Rescue**: An error-handling structure in Ansible. The second play wraps role imports in a `block` with a `rescue` section that catches errors and prints a debug message instead of failing the entire play.
- **Gather Facts**: When `gather_facts: true` is set, Ansible collects system information (like `ansible_facts['os_family']`) at the start of the play. This project uses it to determine whether to apply the RHEL or Windows role based on the target OS.
- **Import Role**: The `import_role` directive statically includes all tasks from a role at playbook parse time. Combined with `when` conditions, it selects the correct role based on the detected OS family.
- **Check Mode**: A dry-run mode activated with `--check` that previews changes without applying them to any system.
- **Vault**: An Ansible feature to encrypt sensitive files. Use `ansible-vault encrypt group_vars/all/credentials.yaml` to protect firewall credentials at rest.
