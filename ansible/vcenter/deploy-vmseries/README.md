# Deploying a VM-Series Firewall on vCenter with Ansible

## Overview

This project automates the deployment of a Palo Alto Networks VM-Series virtual firewall on a VMware vCenter environment. It uses the `community.vmware` collection's `vmware_guest` module to clone a VM from a pre-imported template, place it on a specific ESXi host within a datacenter and folder, and wait for the VM to receive an IP address. All vCenter and VM parameters are defined in `host_vars/localhost.yaml` for clean separation of configuration from playbook logic. The playbook runs locally and communicates with the vCenter API to create the virtual machine.

## Prerequisites

- Python 3.6 or later
- Ansible 2.10 or later
- The `community.vmware` collection installed
- The `pyvmomi` Python library installed (required by the VMware modules)
- Network access to your vCenter server on HTTPS (TCP/443)
- Valid vCenter credentials with permissions to create virtual machines
- A VM-Series OVA/OVF template already imported into vCenter

## Quickstart

1. Clone the repository and navigate to this project:

   ```bash
   git clone https://github.com/cdot65/paloaltonetworks-automation-examples.git
   cd paloaltonetworks-automation-examples/ansible/vcenter/deploy-vmseries
   ```

2. Create and activate a Python virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install Ansible, the required collection, and Python dependency:

   ```bash
   pip install ansible pyvmomi
   ansible-galaxy collection install community.vmware
   ```

4. Edit `host_vars/localhost.yaml` with your vCenter connection details and VM parameters (see Configuration below).

5. Run the playbook:

   ```bash
   ansible-playbook playbook.yaml
   ```

## Configuration

### Inventory

The inventory file `inventory.yaml` defines localhost as the only target:

```yaml
all:
  hosts:
    localhost:
      ansible_connection: local
```

The `ansible_connection: local` setting tells Ansible to run tasks on the control machine rather than connecting via SSH. The playbook communicates with vCenter over its API, not via SSH to the ESXi host.

### Credentials

Store your vCenter credentials in `group_vars/all/credentials.yaml`:

```yaml
---
vcenter_hostname: "vcenter.example.com"
vcenter_username: "administrator@vsphere.local"
vcenter_password: "your-password-here"
```

To encrypt this file with Ansible Vault:

```bash
ansible-vault encrypt group_vars/all/credentials.yaml
```

You will then need to pass `--ask-vault-pass` when running the playbook.

### Variables

| Variable | Location | Required | Description |
|---|---|---|---|
| `vcenter_hostname` | `host_vars/localhost.yaml` or `group_vars/all/credentials.yaml` | Yes | FQDN or IP of the vCenter server |
| `vcenter_username` | `host_vars/localhost.yaml` or `group_vars/all/credentials.yaml` | Yes | vCenter login username |
| `vcenter_password` | `host_vars/localhost.yaml` or `group_vars/all/credentials.yaml` | Yes | vCenter login password |
| `datacenter` | `host_vars/localhost.yaml` | Yes | Name of the vSphere datacenter |
| `folder` | `host_vars/localhost.yaml` | Yes | VM folder path where the VM will be created |
| `esxi_host` | `host_vars/localhost.yaml` | Yes | Name of the ESXi host to deploy the VM on |
| `template` | `host_vars/localhost.yaml` | Yes | Name of the VM-Series template to clone from |
| `vm_name` | `host_vars/localhost.yaml` | Yes | Name for the new VM-Series virtual machine |
| `validate_certs` | `host_vars/localhost.yaml` | No | Whether to validate vCenter SSL certificates (default: `false`) |

## Usage

**Basic run:**

```bash
ansible-playbook playbook.yaml
```

**Deploy with a custom VM name:**

```bash
ansible-playbook playbook.yaml -e "vm_name=fw-branch-01"
```

**Dry run (check mode):**

```bash
ansible-playbook playbook.yaml --check
```

Check mode simulates the playbook run without making any changes. The `vmware_guest` module will verify connectivity to vCenter and validate parameters, but will not create the virtual machine.

**Deploy to a different ESXi host:**

```bash
ansible-playbook playbook.yaml -e "esxi_host=esxi02.example.com vm_name=vmseries-fw-03"
```

**Verbose debugging output:**

```bash
ansible-playbook playbook.yaml -vvv
```

### Expected Output

A successful run will produce output similar to:

```
PLAY [Deploy VM series firewall] ***********************************************

TASK [Create VM series] ********************************************************
changed: [localhost]

TASK [Print VM series details] *************************************************
ok: [localhost] => {
    "vmseries_details": {
        "changed": true,
        "instance": {
            "hw_name": "fw-branch-01",
            "hw_power_status": "poweredOn",
            "ipv4": "192.168.1.100"
        }
    }
}

PLAY RECAP *********************************************************************
localhost                  : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

The `changed=1` indicates the VM was successfully created. The `ipv4` field shows the IP address assigned to the VM after boot.

## Project Structure

```
deploy-vmseries/
├── ansible.cfg                  # Ansible configuration (SSH, privilege escalation, logging)
├── host_vars/
│   └── localhost.yaml           # vCenter connection details and VM parameters
├── inventory.yaml               # Localhost inventory definition
├── playbook.yaml                # Main playbook that deploys the VM-Series firewall
└── README.md                    # This file
```

## Troubleshooting

| Problem | Possible Cause | Solution |
|---|---|---|
| Connection refused | vCenter is unreachable or HTTPS is not enabled | Verify network connectivity and that the vCenter URL is correct |
| Invalid credentials / 403 error | vCenter username or password is incorrect | Verify credentials in `host_vars/localhost.yaml` or `group_vars/all/credentials.yaml` |
| Module not found: `community.vmware.vmware_guest` | The `community.vmware` collection is not installed | Run `ansible-galaxy collection install community.vmware` |
| Timeout waiting for IP address | VM booted but did not get an IP from DHCP | Check VM network settings and ensure the portgroup has DHCP or assign a static IP |
| Template not found | The specified template name does not exist in vCenter | Verify the `template` variable matches the exact template name in vCenter |
| `pyvmomi` import error | The `pyvmomi` Python library is not installed | Run `pip install pyvmomi` |
| SSL certificate error | vCenter uses a self-signed certificate | Set `validate_certs: false` in `host_vars/localhost.yaml` |

## Ansible Concepts Used

- **Playbook**: A YAML file that defines a set of tasks to be executed on target hosts. `playbook.yaml` is the main entry point for this project.
- **Inventory**: A file (`inventory.yaml`) that lists the hosts Ansible will manage. This project targets `localhost` since it communicates with vCenter via API rather than SSH.
- **Module**: A unit of work in Ansible. This project uses `community.vmware.vmware_guest` to create virtual machines and `debug` to print deployment details.
- **Collection**: A packaged set of modules, roles, and plugins. The `community.vmware` collection provides VMware management modules.
- **Host Variables (host_vars)**: Variables stored in the `host_vars/` directory that apply to a specific host. `host_vars/localhost.yaml` contains all vCenter and VM configuration parameters for this project. This is different from group_vars, which apply to all hosts in a group.
- **Register**: The `register` keyword captures the output of a task into a variable for use in later tasks. Here it captures the full VM creation details including the assigned IP address.
- **delegate_to**: A keyword that explicitly directs a task to run on a specific host. Used here to ensure the vCenter API call runs from the localhost.
- **Vault**: Ansible Vault lets you encrypt sensitive files like credential files so secrets are not stored in plain text.
- **Check Mode**: Running a playbook with `--check` simulates execution without making changes, useful for validating parameters and connectivity before deploying a VM.
