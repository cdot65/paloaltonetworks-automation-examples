# Palo Alto Networks Strata Cloud Manager (SCM) Terraform Example

This project demonstrates how to use the [Palo Alto Networks SCM Terraform Provider](https://registry.terraform.io/providers/PaloAltoNetworks/scm/1.0.1) to manage cloud-based firewall configurations through Infrastructure as Code.

## Overview

This example shows how to manage Palo Alto Networks Strata Cloud Manager resources using Terraform, with a focus on:

- **Organized Configuration** - Resources separated by type into logical files
- **Tag-based Organization** - Multi-dimensional tagging for environment and tier classification
- **Dependency Management** - Proper resource ordering with explicit dependencies
- **Three-tier Architecture** - Web, application, and data tier examples
- **Best Practices** - Production-ready patterns and naming conventions

## What This Example Creates

The configuration creates **34 resources** in the Austin folder:

- **6 Tags** - For environment (production, development) and tier (web, app, data, dmz) classification
- **18 Address Objects** - IP addresses, subnets, ranges, and FQDNs across all tiers
- **10 Address Groups** - Collections organized by environment and tier

## Prerequisites

- [Terraform](https://www.terraform.io/downloads.html) v1.0 or later
- Palo Alto Networks Strata Cloud Manager account with API access
- SCM API credentials (Client ID, Client Secret, and Scope in format `tsg_id:XXXXXXXX`)
- Access to the Austin folder in your SCM tenant (or modify to use your folder)

## Project Structure

```
.
├── README.md                    # This file
├── QUICKSTART.md               # Quick start guide
├── versions.tf                 # Terraform and provider version constraints
├── provider.tf                 # SCM provider configuration
├── variables.tf                # Input variables
├── terraform.tfvars.example    # Example variables file
├── tags.tf                     # Tag resource definitions
├── addresses.tf                # Address object definitions
├── address-groups.tf           # Address group definitions
├── outputs.tf                  # Output definitions
├── Makefile                    # Make targets for common operations
└── terraform-provider-scm/     # Local provider source code (reference)
```

## Quick Start

See [QUICKSTART.md](./QUICKSTART.md) for a 5-minute getting started guide.

## Detailed Setup

### 1. Configure Authentication

You have three options for configuring authentication with SCM:

#### Option 1: Environment Variables (Recommended)

Export the following environment variables:

```bash
export SCM_HOST="api.sase.paloaltonetworks.com"
export SCM_AUTH_URL="https://auth.apps.paloaltonetworks.com/auth/v1/oauth2/access_token"
export SCM_CLIENT_ID="your-client-id"
export SCM_CLIENT_SECRET="your-client-secret"
export SCM_SCOPE="tsg_id:your-tenant-id"
```

**Important:** The scope MUST be in the format `tsg_id:1234567890`, not just the numeric ID.

#### Option 2: JSON Configuration File

Create a JSON file with your credentials:

```json
{
  "client_id": "your-client-id",
  "client_secret": "your-client-secret",
  "scope": "tsg_id:your-tenant-id",
  "host": "api.sase.paloaltonetworks.com",
  "auth_url": "https://auth.apps.paloaltonetworks.com/auth/v1/oauth2/access_token"
}
```

Then reference it in your terraform.tfvars:

```hcl
scm_auth_file = "/path/to/your/scm-auth.json"
```

#### Option 3: Terraform Variables

Copy the example variables file and fill in your values:

```bash
cp terraform.tfvars.example terraform.tfvars
```

Edit `terraform.tfvars` with your credentials (NOT recommended for production):

```hcl
scm_client_id     = "your-client-id"
scm_client_secret = "your-client-secret"
scm_scope         = "tsg_id:your-tenant-id"
```

**Important:** Never commit `terraform.tfvars` or any file containing credentials to version control!

### 2. Initialize Terraform

Initialize the Terraform working directory:

```bash
terraform init
```

### 3. Customize Configuration

Edit the variables in `terraform.tfvars` to match your environment:

```hcl
folder       = "Austin"           # SCM folder for resources
environment  = "development"      # Environment name
project_name = "scm-test"         # Project identifier
```

**Important:** If you use a different folder than "Austin", update the `folder` parameter in:

- `tags.tf`
- `addresses.tf`
- `address-groups.tf`

### 4. Plan and Apply

Preview the changes Terraform will make:

```bash
terraform plan
```

Apply the configuration:

```bash
terraform apply
```

Type `yes` when prompted to confirm the changes.

## Resource Details

### Tags (tags.tf)

The configuration creates 6 tags for organizing resources:

**Environment Tags:**

- `production` (Red) - Production environment resources
- `development` (Blue) - Development environment resources

**Tier Tags:**

- `web-tier` (Green) - Web tier resources
- `app-tier` (Orange) - Application tier resources
- `data-tier` (Purple) - Data tier resources
- `dmz` (Yellow) - DMZ resources

### Address Objects (addresses.tf)

18 address objects organized by tier:

**Web Tier (5 addresses):**

- Production: web-prod-1, web-prod-2, web-prod-subnet
- Development: web-dev-1, web-dev-subnet

**Application Tier (4 addresses):**

- Production: app-prod-1, app-prod-2, app-prod-range (IP range)
- Development: app-dev-subnet

**Data Tier (4 addresses):**

- Production: db-prod-1, db-prod-2, db-prod-range (IP range)
- Development: db-dev-subnet

**DMZ (3 addresses):**

- dmz-proxy-1, dmz-proxy-2, dmz-subnet

**External (2 FQDN addresses):**

- api-endpoint (api.company.com)
- cdn-endpoint (cdn.company.com)

### Address Groups (address-groups.tf)

10 address groups organized by environment and purpose:

**Production Groups:**

- prod-web-servers - All production web servers
- prod-app-servers - All production application servers
- prod-db-servers - All production database servers

**Development Groups:**

- dev-web-servers - All development web servers
- dev-app-servers - All development application servers
- dev-db-servers - All development database servers

**Combined Groups:**

- all-web-servers - All web servers (prod + dev)
- dmz-servers - All DMZ servers
- external-endpoints - External API and CDN endpoints
- all-prod-infrastructure - All production infrastructure (web, app, db)

### Outputs (outputs.tf)

Comprehensive outputs organized by category:

- **tags** - All tag IDs
- **address_objects_web_tier** - Web tier address details
- **address_objects_app_tier** - App tier address details
- **address_objects_data_tier** - Data tier address details
- **address_objects_dmz** - DMZ address details
- **address_objects_external** - External FQDN address details
- **address_groups_production** - Production group details
- **address_groups_development** - Development group details
- **address_groups_combined** - Combined group details
- **resource_summary** - Resource count summary
- **address_count_by_tier** - Address count by tier
- **folder_location** - Folder where resources are located

## Configuration Examples

### Adding a New Address Object

Add to `addresses.tf`:

```hcl
resource "scm_address" "web_prod_3" {
  folder      = "Austin"
  name        = "web-prod-3"
  description = "Production web server 3"
  ip_netmask  = "10.1.10.12/32"
  tag         = [scm_tag.production.name, scm_tag.web_tier.name]
  depends_on  = [scm_tag.production, scm_tag.web_tier]
}
```

### Adding a New Address Group

Add to `address-groups.tf`:

```hcl
resource "scm_address_group" "prod_all_servers" {
  folder      = "Austin"
  name        = "prod-all-servers"
  description = "All production servers"
  static = [
    scm_address.web_prod_1.name,
    scm_address.web_prod_2.name,
    scm_address.app_prod_1.name,
    scm_address.app_prod_2.name,
    scm_address.db_prod_1.name,
    scm_address.db_prod_2.name
  ]
  tag = [scm_tag.production.name]

  depends_on = [
    scm_address.web_prod_1,
    scm_address.web_prod_2,
    scm_address.app_prod_1,
    scm_address.app_prod_2,
    scm_address.db_prod_1,
    scm_address.db_prod_2,
    scm_tag.production
  ]
}
```

### Adding a New Tag

Add to `tags.tf`:

```hcl
resource "scm_tag" "staging" {
  folder   = "Austin"
  name     = "staging"
  color    = "Cyan"
  comments = "Staging environment"
}
```

## Provider Configuration

### Authentication Parameters

| Parameter | Description | Environment Variable | Default |
|-----------|-------------|---------------------|---------|
| `host` | SCM API hostname | `SCM_HOST` | `api.sase.paloaltonetworks.com` |
| `auth_url` | OAuth token URL | `SCM_AUTH_URL` | `https://auth.apps.paloaltonetworks.com/auth/v1/oauth2/access_token` |
| `client_id` | OAuth client ID | `SCM_CLIENT_ID` | - |
| `client_secret` | OAuth client secret | `SCM_CLIENT_SECRET` | - |
| `scope` | OAuth scope | `SCM_SCOPE` | - |
| `logging` | Log level | `SCM_LOGGING` | `quiet` |

### Logging Levels

- `quiet` - No logging (default)
- `action` - Log actions only
- `path` - Log API paths
- `info` - Log informational messages
- `debug` - Full debug logging

## Resource Location

SCM resources can be placed in three different locations:

1. **Folder** - Shared across multiple configurations (e.g., "Austin", "Shared", "Mobile Users")
2. **Snippet** - Configuration snippets for specific use cases
3. **Device** - Device-specific configurations

This example uses the `folder` parameter set to "Austin".

## Dependency Management

The configuration demonstrates proper dependency management:

1. **Tags** are created first (no dependencies)
2. **Address Objects** depend on tags using `depends_on`
3. **Address Groups** depend on both tags and address objects

This ensures resources are created in the correct order and prevents errors.

Example:

```hcl
resource "scm_address" "web_prod_1" {
  folder      = "Austin"
  name        = "web-prod-1"
  description = "Production web server 1"
  ip_netmask  = "10.1.10.10/32"
  tag         = [scm_tag.production.name, scm_tag.web_tier.name]
  depends_on  = [scm_tag.production, scm_tag.web_tier]  # Explicit dependency
}
```

## Best Practices

1. **Organized File Structure** - Separate resources by type for maintainability
2. **Use Tags** - Apply tags to all resources for organization and tracking
3. **Explicit Dependencies** - Use `depends_on` to ensure proper resource ordering
4. **Consistent Naming** - Use descriptive, consistent names across resources
5. **Folder Consistency** - Keep all related resources in the same folder
6. **State Management** - Use remote state storage (S3, Terraform Cloud, etc.)
7. **Version Control** - Track all Terraform files in Git (except terraform.tfvars)
8. **Security** - Never commit credentials; use environment variables or secure vaults
9. **Testing** - Always run `terraform plan` before `apply`
10. **Documentation** - Document custom resources and non-obvious configurations

## Known Limitations

1. **Wildcard Addresses** - Cannot have tags assigned (SCM API limitation)
2. **Folder Consistency** - Tags and resources must be in the same folder
3. **Scope Format** - Must be `tsg_id:XXXXXXXX`, not just the numeric ID

## Debugging

Enable detailed logging for troubleshooting:

```bash
# Terraform logging
export TF_LOG=DEBUG

# SCM provider logging
export SCM_LOGGING=debug

terraform apply
```

Or set in terraform.tfvars:

```hcl
scm_logging = "debug"
```

## Common Issues

### Authentication Failures

**Error:** `auth error: invalid_scope`

**Solution:** Ensure your scope is in the format `tsg_id:1234567890`, not just `1234567890`

### Folder Mismatch

**Error:** 400 Bad Request when creating resources

**Solution:** Verify that tags and address objects are in the same folder. Update the `folder` parameter in all resource files if needed.

### Resource Already Exists

**Error:** Resource with name already exists

**Solution:** Either delete the existing resource in SCM, rename your resource, or import it:

```bash
terraform import scm_address.web_prod_1 Austin:::resource-id
```

### Dependency Errors

**Error:** Resource not found during creation

**Solution:** Add explicit `depends_on` to ensure proper ordering:

```hcl
depends_on = [scm_tag.production, scm_tag.web_tier]
```

## Extending This Example

This example can be extended with additional SCM resources:

### Security Rules

```hcl
resource "scm_security_rule" "allow_web" {
  folder      = "Austin"
  name        = "allow-web-traffic"
  description = "Allow inbound web traffic"
  position    = "pre"

  action      = "allow"
  application = ["web-browsing", "ssl"]
  service     = ["service-http", "service-https"]

  from = ["untrust"]
  to   = ["trust"]

  source      = ["any"]
  destination = ["prod-web-servers"]

  log_end = true
}
```

### Service Objects

```hcl
resource "scm_service" "custom_app" {
  folder      = "Austin"
  name        = "custom-app-8080"
  description = "Custom application port 8080"
  protocol = {
    tcp = {
      port = "8080"
    }
  }
}
```

### NAT Rules

```hcl
resource "scm_nat_rule" "dnat_web" {
  folder      = "Austin"
  name        = "dnat-web-servers"
  description = "DNAT for web servers"
  position    = "pre"

  nat_type = "ipv4"

  source_translation {
    type = "dynamic-ip-and-port"
    translated_address = ["public-ip"]
  }
}
```

## Using Make

The included Makefile provides convenient targets:

```bash
make help      # Show all targets
make init      # Initialize Terraform
make validate  # Validate configuration
make fmt       # Format Terraform files
make plan      # Preview changes
make apply     # Apply changes
make destroy   # Destroy all resources
make clean     # Clean local files
```

## Provider Documentation

- [Terraform Registry - SCM Provider](https://registry.terraform.io/providers/PaloAltoNetworks/scm/1.0.1)
- [GitHub - terraform-provider-scm](https://github.com/PaloAltoNetworks/terraform-provider-scm)
- [Strata Cloud Manager Documentation](https://docs.paloaltonetworks.com/strata-cloud-manager)

## Version History

- **1.0.1** - Current version used in this example
- Refer to the [provider changelog](https://github.com/PaloAltoNetworks/terraform-provider-scm/releases) for updates

## Contributing

This is an example project. Feel free to modify and extend it for your needs.

## Support

For provider issues, please report them on the [GitHub repository](https://github.com/PaloAltoNetworks/terraform-provider-scm/issues).

For SCM API questions, consult the [Palo Alto Networks documentation](https://docs.paloaltonetworks.com/).

## License

See the LICENSE file in the provider repository for details.
