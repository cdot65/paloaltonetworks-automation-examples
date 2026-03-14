# PAN-OS Basic Configuration Starter Template

## Overview

This project is a starter template for managing Palo Alto Networks PAN-OS firewalls using the Terraform `panos` provider (v1). It uses the `PaloAltoNetworks/panos` provider version 1.11.1, which communicates with PAN-OS firewalls via the XML API. The project contains the initialized provider binary and lock file but no active resource definitions, serving as a baseline for building firewall-as-code configurations. Authentication is handled by providing hostname, username, and password to the provider block.

## Prerequisites

- Terraform >= 1.0
- A PAN-OS firewall or Panorama appliance with API access enabled
- Network connectivity to the firewall management interface
- Administrative credentials for the PAN-OS device

> **New to Terraform?** Terraform uses three main commands: `terraform init` downloads provider plugins, `terraform plan` previews changes without applying them, and `terraform apply` executes the changes against your infrastructure.

## Quickstart

1. Clone the repository:
   ```bash
   git clone https://github.com/cdot65/paloaltonetworks-automation-examples.git
   cd paloaltonetworks-automation-examples/terraform/panos/basic-config
   ```

2. Create your variables file:
   ```bash
   cp terraform.tfvars.example terraform.tfvars
   ```

3. Edit `terraform.tfvars` with your firewall credentials.

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

Configure the provider with your PAN-OS firewall credentials:

```hcl
provider "panos" {
  hostname = "firewall.example.com"
  username = "admin"
  password = "your-password"
}
```

Alternatively, use environment variables:

```bash
export PANOS_HOSTNAME="firewall.example.com"
export PANOS_USERNAME="admin"
export PANOS_PASSWORD="your-password"
```

> **Security note:** Never commit `terraform.tfvars` files containing credentials to version control. Add `*.tfvars` to your `.gitignore` file.

### Variables

This is a starter template with no variables defined yet. Add variables to `variables.tf` as you extend the configuration.

## Usage

Preview changes:
```bash
terraform plan
```

Apply the configuration:
```bash
terraform apply
```

Since this is a starter template with no resources defined, the expected plan output is:

```
No changes. Your infrastructure matches the configuration.

Terraform has compared your real infrastructure against your configuration
and found no differences, so no changes are needed.
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
basic-config/
├── .terraform/                 # Provider binaries (auto-generated)
├── .terraform.lock.hcl         # Provider version lock file
└── README.md                   # This documentation
```

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Provider installation fails | Network or registry issues | Run `terraform init -upgrade` or check network connectivity |
| Invalid credentials | Wrong username/password | Verify credentials work via the PAN-OS web UI |
| Connection refused | Firewall unreachable | Check network connectivity and management interface IP |
| Resource already exists | Object exists on firewall | Import with `terraform import` or remove from firewall |
| State lock error | Concurrent Terraform runs | Wait for other run to finish or force unlock with `terraform force-unlock` |
| Provider version mismatch | Lock file conflicts | Run `terraform init -upgrade` to update providers |

## Terraform Concepts Used

- **Provider**: The `panos` provider interfaces with PAN-OS devices via the XML API to manage firewall configuration as code.
- **Resource**: Terraform resources (to be added) represent PAN-OS configuration objects like security rules, address objects, and zones.
- **Variable**: Input variables allow parameterizing configurations so credentials and settings can differ per environment.
- **State**: Terraform tracks managed resources in a state file, enabling incremental updates and drift detection.
- **Plan**: The `terraform plan` command previews changes before applying, providing a safety check.
