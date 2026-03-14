# Strata Cloud Manager Terraform Examples

2 Terraform configurations for managing Strata Cloud Manager (SCM) resources using the SCM Terraform provider with OAuth2 authentication.

## Projects

| Project | Description |
|---------|-------------|
| [basic-example](https://github.com/cdot65/paloaltonetworks-automation-examples/tree/main/terraform/scm/basic-example) | Creates 34 SCM resources (6 tags, 18 address objects, 10 address groups) organized by environment tier in an "Austin" folder. Demonstrates OAuth2 client credential authentication. |
| [modules](https://github.com/cdot65/paloaltonetworks-automation-examples/tree/main/terraform/scm/modules) | Organizes SCM resources into two reusable child modules -- `texas-address-objects` (addresses + groups) and `texas-network-objects` (tags, services, service groups) -- demonstrating Terraform module patterns. |

## Authentication

SCM uses OAuth2 client credentials:

```hcl
provider "scm" {
  client_id     = var.client_id
  client_secret = var.client_secret
  scope         = var.scope
}
```

!!! info "Getting Credentials"
    Create a service account in the Strata Cloud Manager console under **Settings > Identity & Access > Service Accounts**. The scope format is `tsg_id:{your-tsg-id}`.
