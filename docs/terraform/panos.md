# PAN-OS Terraform Examples

4 Terraform configurations demonstrating both v1 and v2 of the PAN-OS Terraform provider.

## Projects

| Project | Provider | Description |
|---------|----------|-------------|
| [basic-config](https://github.com/cdot65/paloaltonetworks-automation-examples/tree/main/terraform/panos/basic-config) | v1 (1.11.1) | Minimal starter template initializing the PAN-OS provider with no active resources -- a baseline for building firewall-as-code. |
| [dynamic-address-groups](https://github.com/cdot65/paloaltonetworks-automation-examples/tree/main/terraform/panos/dynamic-address-groups) | v1 | Creates `panos_ip_tag` resources that register IP-to-tag mappings for use with dynamic address groups in security policies. |
| [firewall-config](https://github.com/cdot65/paloaltonetworks-automation-examples/tree/main/terraform/panos/firewall-config) | v2 | Configures DNS settings (`panos_dns_settings`) using provider v2 with location-based resource targeting. |
| [provider-v2-example](https://github.com/cdot65/paloaltonetworks-automation-examples/tree/main/terraform/panos/provider-v2-example) | v2 | Comprehensive 34-resource Panorama example covering templates, stacks, device groups, zones, interfaces, virtual routers, addresses, services, security policies, and custom URL categories. |

## Provider v1 vs v2

| Feature | v1 | v2 |
|---------|----|----|
| Resource naming | `panos_address_object` | `panos_address_object` (same) |
| Location targeting | Implicit (device/vsys) | Explicit `location` blocks |
| Panorama support | Separate resource types | Unified with location |
| Status | Maintenance mode | Active development |

!!! tip "Migration"
    New projects should use provider v2. The `provider-v2-example` project is the best starting point for Panorama-managed configurations.
