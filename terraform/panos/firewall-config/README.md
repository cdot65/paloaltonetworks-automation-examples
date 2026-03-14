# PAN-OS NGFW DNS Configuration with Provider v2

## Overview

This project configures DNS settings on a Palo Alto Networks next-generation firewall (NGFW) using the Terraform `panos` provider v2. It uses the `PaloAltoNetworks/panos` provider version 2.0.0, which provides an updated resource schema compared to v1. The project creates a `panos_dns_settings` resource targeting the NGFW system-level DNS configuration. Authentication is handled via hostname, username, and password with optional certificate verification skip.

## Prerequisites

- Terraform >= 1.0
- PAN-OS NGFW with API access enabled (PAN-OS 10.1+ recommended for v2 provider)
- Network connectivity to the firewall management interface
- Administrative credentials with configuration permissions

> **New to Terraform?** Terraform uses three main commands: `terraform init` downloads provider plugins, `terraform plan` previews changes without applying them, and `terraform apply` executes the changes against your infrastructure.

## Quickstart

1. Clone the repository:
   ```bash
   git clone https://github.com/cdot65/paloaltonetworks-automation-examples.git
   cd paloaltonetworks-automation-examples/terraform/panos/firewall-config
   ```

2. Create your variables file:
   ```bash
   cp terraform.tfvars.example terraform.tfvars
   ```

3. Edit `terraform.tfvars` with your NGFW connection details and DNS settings.

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
  hostname                = "192.168.1.1"
  username                = "admin"
  password                = "your-password"
  skip_verify_certificate = true
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
| `ngfw` | object | Yes | n/a | NGFW connection details containing `hostname`, `username`, and `password` |
| `dns_settings` | map(object) | Yes | n/a | Map of DNS settings resources with location, server IPs, and FQDN refresh time |

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

  # panos_dns_settings.NGFW will be created
  + resource "panos_dns_settings" "NGFW" {
      + dns_settings      = {
          + servers = {
              + primary   = "10.0.0.70"
              + secondary = "10.0.0.90"
            }
        }
      + fqdn_refresh_time = 3600
      + location          = {
          + system = {}
        }
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
firewall-config/
├── main.tf                     # DNS settings resource definition
├── outputs.tf                  # Output values (currently commented out)
├── provider.tf                 # Provider v2 and version configuration
├── variables.tf                # Input variable declarations
└── README.md                   # This documentation
```

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Provider installation fails | Network or registry issues | Run `terraform init -upgrade` or check network connectivity |
| Invalid credentials | Wrong username/password | Verify credentials work via the PAN-OS web UI |
| Connection refused | Firewall unreachable | Check network connectivity and management interface IP |
| Resource already exists | DNS settings already configured | Import with `terraform import` or modify existing config |
| State lock error | Concurrent Terraform runs | Wait for other run to finish or force unlock with `terraform force-unlock` |
| Provider version mismatch | v1 vs v2 resource schema conflict | Ensure provider version is `2.0.0` and resource syntax matches v2 |

## Terraform Concepts Used

- **Provider**: The `panos` provider (v2) interfaces with PAN-OS devices via an updated API schema with location-based resource targeting.
- **Resource**: `panos_dns_settings` configures system-level DNS servers and FQDN refresh timers on the NGFW.
- **Variable**: Input variables parameterize connection details and DNS configuration for reuse across environments.
- **Output**: Output values (commented out) can expose created resource attributes for downstream consumption.
- **State**: Terraform tracks the DNS settings in its state file for incremental updates.
- **Plan**: The `terraform plan` command previews DNS configuration changes before applying.
