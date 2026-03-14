# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This repository contains Terraform example projects for Palo Alto Networks Strata Cloud Manager (SCM). We use the SCM Terraform provider (documented in the api-docs directory) to demonstrate infrastructure-as-code management of various SCM resources.

## Project Structure

- `api-docs/` - Documentation and implementation of the SCM Terraform provider
- Example templates for SCM resources are available at `api-docs/examples/resources/`
- Example templates for SCM data sources are available at `api-docs/examples/data-sources/`

## Working with the SCM Terraform Provider

### Provider Configuration

The SCM provider needs to be configured with your Strata Cloud Manager credentials:

```hcl
provider "scm" {
  host          = "api.strata.paloaltonetworks.com"
  client_id     = "your-id@12345"
  client_secret = "secret"
  scope         = "tsg_id:12345"
}

terraform {
  required_providers {
    scm = {
      source  = "paloaltonetworks/scm"
      version = "0.1.0"
    }
  }
}
```

### Creating Example Projects

When creating example Terraform configurations:

1. Start with a provider configuration block (see above)
2. Reference the resource examples in `api-docs/examples/resources/` for specific resources
3. For data sources, reference examples in `api-docs/examples/data-sources/`
4. Follow best practices for resource organization:
   - Group related resources together
   - Use descriptive names for resources
   - Add comments to explain configuration choices

### Common Terraform Operations

```bash
# Initialize your working directory
terraform init

# Validate your configuration
terraform validate

# Preview changes 
terraform plan

# Apply changes
terraform apply

# Destroy resources when finished
terraform destroy
```

## Common SCM Resource Types

Some commonly used SCM resources:

- `scm_address_object` - Manage IP address objects
- `scm_address_group` - Manage address groups
- `scm_security_rule` - Manage security policy rules
- `scm_nat_rule` - Manage NAT rules
- `scm_service` - Manage service definitions
- `scm_service_group` - Manage service groups
- `scm_tag` - Manage tags

For complete documentation on all available resources, refer to the documentation in `api-docs/docs/resources/`.

## Example Use Cases

When designing examples, consider these common use cases:

1. Basic network security configuration 
2. Site-to-site VPN setup
3. Policy organization using tags and groups
4. Application filtering and control
5. Integration with security profiles and threat protection features

## Important Notes

- The SCM provider is experimental and not officially supported:
  > THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED
  > 
  > THIS SOFTWARE IS RELEASED AS A PROOF OF CONCEPT FOR EXPERIMENTAL PURPOSES ONLY. USE IT AT OWN RISK. THIS SOFTWARE IS NOT SUPPORTED.
  
- When testing configurations, use a non-production SCM environment first
- Always use environment variables or a secrets manager for sensitive credentials in production