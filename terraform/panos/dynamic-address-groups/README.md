# PAN-OS Dynamic Address Groups with IP Tagging

## Overview

This project demonstrates IP address tagging on a Palo Alto Networks PAN-OS firewall using the Terraform `panos` provider (v1). It uses the `PaloAltoNetworks/panos` provider version 1.11.0 to create `panos_ip_tag` resources, which register IP-to-tag mappings on the firewall. These tagged IPs can then be referenced by dynamic address groups in security policies. Authentication is performed via hostname, username, and password against the PAN-OS XML API.

## Prerequisites

- Terraform >= 1.0
- PAN-OS firewall with API access enabled
- Network connectivity to the firewall management interface
- Administrative credentials with API permissions

> **New to Terraform?** Terraform uses three main commands: `terraform init` downloads provider plugins, `terraform plan` previews changes without applying them, and `terraform apply` executes the changes against your infrastructure.

## Quickstart

1. Clone the repository:
   ```bash
   git clone https://github.com/cdot65/paloaltonetworks-automation-examples.git
   cd paloaltonetworks-automation-examples/terraform/panos/dynamic-address-groups
   ```

2. Create your variables file:
   ```bash
   cp terraform.tfvars.example terraform.tfvars
   ```

3. Edit `terraform.tfvars` with your firewall connection details.

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
provider "panos" {
  hostname = "192.168.1.1"
  username = "admin"
  password = "your-password"
}
```

Alternatively, use environment variables:

```bash
export PANOS_HOSTNAME="192.168.1.1"
export PANOS_USERNAME="admin"
export PANOS_PASSWORD="your-password"
```

> **Security note:** Never commit `terraform.tfvars` files containing credentials to version control. Add `*.tfvars` to your `.gitignore` file.

### Variables

| Variable | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `firewall` | object | Yes | n/a | Firewall connection details containing `fw_ip`, `username`, and `password` |

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

  # panos_ip_tag.example1 will be created
  + resource "panos_ip_tag" "example1" {
      + ip   = "10.2.3.4"
      + tags = [
          + "Automation",
        ]
    }

Plan: 1 to add, 0 to change, 0 to destroy.
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
dynamic-address-groups/
├── main.tf                     # IP tag resource definitions
├── provider.tf                 # Provider and version configuration
├── variables.tf                # Input variable declarations
├── terraform.tfvars            # Variable values (do not commit)
└── README.md                   # This documentation
```

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Provider installation fails | Network or registry issues | Run `terraform init -upgrade` or check network connectivity |
| Invalid credentials | Wrong username/password | Verify credentials work via the PAN-OS web UI |
| Connection refused | Firewall unreachable | Check network connectivity and management interface IP |
| Resource already exists | IP tag already registered | Import with `terraform import` or clear tag on firewall |
| State lock error | Concurrent Terraform runs | Wait for other run to finish or force unlock with `terraform force-unlock` |
| Provider version mismatch | Lock file conflicts | Run `terraform init -upgrade` to update providers |

## Terraform Concepts Used

- **Provider**: The `panos` provider (v1) interfaces with PAN-OS devices via the XML API.
- **Resource**: `panos_ip_tag` registers an IP address with one or more tags on the firewall for use in dynamic address groups.
- **Variable**: The `firewall` variable encapsulates connection details as a structured object.
- **State**: Terraform tracks the IP tag registration in its state file.
- **Plan**: The `terraform plan` command previews tag registration changes before applying.
