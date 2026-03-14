# vCenter Ansible Playbooks

## Deploy VM-Series on vCenter

[View on GitHub](https://github.com/cdot65/paloaltonetworks-automation-examples/tree/main/ansible/vcenter/deploy-vmseries)

Uses `community.vmware.vmware_guest` to clone a VM-Series firewall from a pre-imported OVA template on a specific ESXi host within a vCenter datacenter, then waits for the VM to receive an IP address.

### What It Does

1. Connects to vCenter using credentials from `group_vars/`
2. Clones the VM-Series template to a new VM on the specified ESXi host
3. Configures the VM with the defined resource allocation (CPU, memory, disk)
4. Powers on the VM and waits for VMware Tools to report an IP

### Prerequisites

- vCenter Server with admin credentials
- VM-Series OVA template pre-imported into vCenter
- `community.vmware` collection installed
- Python `PyVmomi` library
