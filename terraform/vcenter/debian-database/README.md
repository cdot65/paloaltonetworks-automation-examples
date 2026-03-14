# vCenter Debian Database VM Deployment

## Overview

This project deploys a Debian-based PostgreSQL database virtual machine on VMware vSphere/vCenter using the Terraform `vsphere` provider. It clones a VM from an existing template, configures network settings with a static IP address, attaches tags for workload classification, and customizes the guest OS with hostname and domain settings. Authentication is performed via vCenter username and password with optional unverified SSL support.

## Prerequisites

- Terraform >= 1.0
- VMware vSphere/vCenter 6.7+ with API access
- A Debian VM template available in the vCenter inventory
- Network connectivity to the vCenter server
- Administrative credentials for vCenter
- The target datacenter, cluster, datastore, network, and ESXi host must exist

> **New to Terraform?** Terraform uses three main commands: `terraform init` downloads provider plugins, `terraform plan` previews changes without applying them, and `terraform apply` executes the changes against your infrastructure.

## Quickstart

1. Clone the repository:
   ```bash
   git clone https://github.com/cdot65/paloaltonetworks-automation-examples.git
   cd paloaltonetworks-automation-examples/terraform/vcenter/debian-database
   ```

2. Create your variables file:
   ```bash
   cp terraform.tfvars.example terraform.tfvars
   ```

3. Edit `terraform.tfvars` with your vCenter credentials, infrastructure names, and VM settings.

4. Initialize Terraform:
   ```bash
   terraform init
   ```

5. Preview changes:
   ```bash
   terraform plan
   ```

6. Apply the configuration:
   ```bash
   terraform apply
   ```

## Configuration

### Authentication

```hcl
provider "vsphere" {
  user                 = "administrator@vsphere.local"
  password             = "your-password"
  vsphere_server       = "vcenter.example.com"
  allow_unverified_ssl = true
}
```

Alternatively, use environment variables:

```bash
export VSPHERE_USER="administrator@vsphere.local"
export VSPHERE_PASSWORD="your-password"
export VSPHERE_SERVER="vcenter.example.com"
export VSPHERE_ALLOW_UNVERIFIED_SSL="true"
```

> **Security note:** Never commit `terraform.tfvars` files containing credentials to version control. Add `*.tfvars` to your `.gitignore` file.

### Variables

| Variable | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `vcenter_user` | string | Yes | n/a | Username for vCenter authentication |
| `vcenter_password` | string | Yes | n/a | Password for vCenter authentication (sensitive) |
| `vcenter_server` | string | Yes | n/a | vCenter server address |
| `datacenter_name` | string | Yes | n/a | Name of the vSphere datacenter |
| `datastore_name` | string | Yes | n/a | Name of the vSphere datastore |
| `cluster_name` | string | Yes | n/a | Name of the vSphere cluster |
| `network_name` | string | Yes | n/a | Name of the network to attach the VM to |
| `host_name` | string | Yes | n/a | Name of the ESXi host to deploy the VM on |
| `template_name` | string | Yes | n/a | Name of the template to clone the VM from |
| `vm_name` | string | Yes | n/a | Name of the virtual machine |
| `vm_ipv4_address` | string | Yes | n/a | Static IPv4 address for the VM |
| `vm_ipv4_netmask` | number | Yes | n/a | IPv4 netmask (e.g., 24) |
| `vm_ipv4_gateway` | string | Yes | n/a | IPv4 gateway for the VM |
| `vm_domain` | string | Yes | n/a | Domain name for the VM |
| `vm_cpu_count` | number | Yes | n/a | Number of vCPUs |
| `vm_memory` | number | Yes | n/a | Memory in MB |
| `vm_disk_size` | number | Yes | n/a | Disk size in GB |
| `tags` | list(string) | Yes | n/a | Tags to associate with the VM |

## Usage

Preview changes:
```bash
terraform plan
```

Apply the configuration:
```bash
terraform apply
```

Expected `terraform plan` output:

```
Terraform will perform the following actions:

  # vsphere_tag.database will be created
  + resource "vsphere_tag" "database" {
      + name        = "database"
      + category_id = (known after apply)
    }

  # vsphere_tag.postgres will be created
  + resource "vsphere_tag" "postgres" {
      + name        = "postgres"
      + category_id = (known after apply)
    }

  # vsphere_tag_category.workload will be created
  + resource "vsphere_tag_category" "workload" {
      + name        = "workload"
      + cardinality = "MULTIPLE"
    }

  # vsphere_virtual_machine.postgres_vm will be created
  + resource "vsphere_virtual_machine" "postgres_vm" {
      + name             = (known after apply)
      + num_cpus         = (known after apply)
      + memory           = (known after apply)
      + guest_id         = (known after apply)
    }

Plan: 4 to add, 0 to change, 0 to destroy.
```

Destroy all managed resources:
```bash
terraform destroy
```

Format and validate your configuration:
```bash
terraform fmt
terraform validate
```

## Project Structure

```
debian-database/
├── main.tf                     # VM, tag, and tag category resource definitions
├── provider.tf                 # vSphere provider configuration
├── variables.tf                # Input variable declarations
├── terraform.tfvars            # Variable values (do not commit)
└── README.md                   # This documentation
```

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Provider installation fails | Network or registry issues | Run `terraform init -upgrade` or check network connectivity |
| Invalid credentials | Wrong vCenter username/password | Verify credentials work via the vSphere web client |
| Connection refused | vCenter server unreachable | Check network connectivity and vCenter address |
| Resource already exists | VM name or tag already in vCenter | Rename the VM or delete the existing resource |
| State lock error | Concurrent Terraform runs | Wait for other run to finish or force unlock with `terraform force-unlock` |
| Provider version mismatch | Lock file conflicts | Run `terraform init -upgrade` to update providers |
| Template not found | Template name incorrect or not in datacenter | Verify template name and datacenter in vSphere inventory |
| Customization fails | VMware Tools not installed on template | Install VMware Tools/open-vm-tools on the template VM |

## Terraform Concepts Used

- **Provider**: The `vsphere` provider interfaces with VMware vCenter to manage virtual infrastructure.
- **Resource**: Resources include `vsphere_virtual_machine` (cloned from template), `vsphere_tag`, and `vsphere_tag_category`.
- **Variable**: Input variables parameterize vCenter credentials, infrastructure names, and VM specifications.
- **State**: Terraform tracks the VM, tags, and tag category in its state file for lifecycle management.
- **Plan**: The `terraform plan` command previews VM creation and tag assignment before applying.
