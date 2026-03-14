# vCenter Terraform Example

[View on GitHub](https://github.com/cdot65/paloaltonetworks-automation-examples/tree/main/terraform/vcenter/debian-database)

Deploys a Debian-based PostgreSQL database VM on vSphere by cloning from a template, configuring networking, and applying workload classification tags.

## What Gets Created

- Cloned VM from a Debian template
- Static IP configuration via guest OS customization
- vSphere tags for workload classification
- Custom hostname and domain settings

## Prerequisites

- vCenter Server with admin credentials
- Debian VM template pre-imported
- `vsphere` Terraform provider

## Key Variables

| Variable | Description |
|----------|-------------|
| `vsphere_server` | vCenter hostname or IP |
| `vsphere_user` | vCenter admin username |
| `vsphere_password` | vCenter admin password |
| `datacenter` | Target datacenter name |
| `cluster` | Target compute cluster |
| `template_name` | Name of the Debian template to clone |
