# PAN-OS Panorama Full Configuration with Provider v2

## Overview

This project provides a comprehensive Panorama configuration example using the Terraform `panos` provider v2. It uses the `PaloAltoNetworks/panos` provider version 2.0.0 to manage a full branch office deployment through Panorama, creating templates, template stacks, device groups, security zones, interfaces, virtual routers, address objects, address groups, services, service groups, security policies, and custom URL categories. Authentication is performed via hostname, username, and password against the Panorama XML API.

## Prerequisites

- Terraform >= 1.0
- Palo Alto Networks Panorama with API access enabled (PAN-OS 10.1+ recommended)
- Network connectivity to the Panorama management interface
- Administrative credentials with full configuration permissions
- Managed firewalls registered to Panorama (for template stack device assignment)

> **New to Terraform?** Terraform uses three main commands: `terraform init` downloads provider plugins, `terraform plan` previews changes without applying them, and `terraform apply` executes the changes against your infrastructure.

## Quickstart

1. Clone the repository:
   ```bash
   git clone https://github.com/cdot65/paloaltonetworks-automation-examples.git
   cd paloaltonetworks-automation-examples/terraform/panos/provider-v2-example
   ```

2. Create your variables file:
   ```bash
   cp terraform.tfvars.example terraform.tfvars
   ```

3. Edit `terraform.tfvars` with your Panorama connection details and desired configuration.

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
  hostname = "panorama.example.com"
  username = "admin"
  password = "your-password"
}
```

Alternatively, use environment variables:

```bash
export PANOS_HOSTNAME="panorama.example.com"
export PANOS_USERNAME="admin"
export PANOS_PASSWORD="your-password"
```

> **Security note:** Never commit `terraform.tfvars` files containing credentials to version control. Add `*.tfvars` to your `.gitignore` file.

### Variables

| Variable | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `panorama` | object | Yes | n/a | Panorama connection details: `hostname`, `username`, `password` |
| `dns_settings` | map(object) | Yes | n/a | DNS server configuration per location (system/template/template_stack) |
| `ntp_settings` | map(object) | Yes | n/a | NTP server configuration per location |
| `templates` | map(object) | Yes | n/a | Panorama templates with name and description |
| `template_stacks` | map(object) | Yes | n/a | Template stacks with devices and default vsys |
| `template_variables` | map(object) | Yes | n/a | Template variables for interface assignments |
| `interface_management_profiles` | map(object) | Yes | n/a | Management profiles with permitted IPs and protocols |
| `ethernet_interfaces` | map(object) | Yes | n/a | Ethernet interface configurations (layer3, DHCP, IPs) |
| `loopback_interfaces` | map(object) | Yes | n/a | Loopback interface configurations |
| `zones` | map(object) | Yes | n/a | Security zones with network interface assignments |
| `virtual_routers` | map(object) | Yes | n/a | Virtual routers with interfaces and routing tables |
| `device_groups` | map(object) | Yes | n/a | Device groups with device assignments |
| `device_group_parents` | map(object) | Yes | n/a | Parent-child relationships between device groups |
| `administrative_tags` | map(object) | Yes | n/a | Tags with color and comments |
| `addresses` | map(object) | Yes | n/a | Address objects (IP, FQDN, range) |
| `address_groups` | map(object) | Yes | n/a | Static and dynamic address groups |
| `services` | map(object) | Yes | n/a | Service definitions (TCP/UDP ports) |
| `service_groups` | map(object) | Yes | n/a | Service groups with member services |
| `security_policies` | map(object) | Yes | n/a | Security policy rules with zones, apps, and actions |
| `custom_url_categories` | map(object) | Yes | n/a | Custom URL category lists |

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

  # panos_administrative_tag.Automation will be created
  # panos_administrative_tag.Critical will be created
  # panos_administrative_tag.Production will be created
  # panos_administrative_tag.Staging will be created
  # panos_address_group.Branch_Cloud_Workloads will be created
  # panos_address_group.Branch_Databases will be created
  # panos_address_group.Branch_Webservers will be created
  # panos_addresses.Branch will be created
  # panos_custom_url_category.blocked_sites will be created
  # panos_device_group.Branch will be created
  # panos_device_group.Dallas will be created
  # panos_device_group.Woodlands will be created
  # panos_device_group_parent.Dallas will be created
  # panos_device_group_parent.Woodlands will be created
  # panos_dns_settings.Branch will be created
  # panos_dns_settings.Panorama will be created
  # panos_ethernet_interface.ethernet1 will be created
  # panos_ethernet_interface.ethernet2 will be created
  # panos_interface_management_profile.Local_Management will be created
  # panos_loopback_interface.Loopback1 will be created
  # panos_ntp_settings.Branch will be created
  # panos_ntp_settings.Panorama will be created
  # panos_security_policy.branch_policy will be created
  # panos_service.dns_dev will be created
  # panos_service.web_service_dev will be created
  # panos_service_group.web_group_dev will be created
  # panos_template.Branch will be created
  # panos_template_stack.Dallas will be created
  # panos_template_stack.Woodlands will be created
  # panos_template_variable.interface_lan will be created
  # panos_template_variable.interface_wan will be created
  # panos_virtual_router.branch_vr will be created
  # panos_zone.trust_zone will be created
  # panos_zone.untrust_zone will be created

Plan: 34 to add, 0 to change, 0 to destroy.

Changes to Outputs:
  + branch_device_group      = "Branch-DG"
  + branch_security_rules    = [...]
  + branch_template          = "Branch-Template"
  + dallas_device_group      = "Dallas-DG"
  + dallas_template_stack    = "Dallas-TemplateStack"
  + dns_service              = "dns-service"
  + trust_zone               = "Trust-Zone"
  + untrust_zone             = "Untrust-Zone"
  + web_service              = "web-service-developer"
  + woodlands_device_group   = "Woodlands-DG"
  + woodlands_template_stack = "Woodlands-TemplateStack"
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
provider-v2-example/
├── main.tf                        # All resource definitions (DNS, NTP, templates, zones, policies, etc.)
├── outputs.tf                     # Output values for templates, device groups, zones, services
├── provider.tf                    # Provider v2 configuration and version constraints
├── variables.tf                   # Input variable declarations for all resource types
├── terraform.tfvars.example       # Example variable values with sample configuration
└── README.md                      # This documentation
```

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Provider installation fails | Network or registry issues | Run `terraform init -upgrade` or check network connectivity |
| Invalid credentials | Wrong username/password | Verify credentials work via the Panorama web UI |
| Connection refused | Panorama unreachable | Check network connectivity and management interface IP |
| Resource already exists | Object already configured on Panorama | Import with `terraform import` or remove from Panorama |
| State lock error | Concurrent Terraform runs | Wait for other run to finish or force unlock with `terraform force-unlock` |
| Provider version mismatch | v1 vs v2 schema differences | Ensure provider version is `2.0.0`; v2 uses `location` blocks |
| Dependency ordering errors | Resources created out of order | Review `depends_on` blocks; template must exist before stacks |
| GRPCProvider request cancelled | Template stack override issue | Known v2 bug with overrides; use template-level config instead |

## Terraform Concepts Used

- **Provider**: The `panos` provider (v2) interfaces with Panorama via the XML API using location-based resource targeting.
- **Resource**: 34 resources spanning DNS/NTP settings, templates, template stacks, interfaces, zones, virtual routers, device groups, address objects/groups, services/groups, security policies, and custom URL categories.
- **Variable**: Complex nested object variables parameterize the entire Panorama configuration for reuse.
- **Output**: Outputs expose created template, device group, zone, and service names.
- **State**: Terraform tracks all 34 Panorama resources in its state file for incremental updates.
- **Plan**: The `terraform plan` command previews the full Panorama configuration before applying.
