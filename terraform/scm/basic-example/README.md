# Strata Cloud Manager Basic Example

## Overview

This project provides a basic example of managing Palo Alto Networks Strata Cloud Manager (SCM) resources using the Terraform `scm` provider. It uses the `PaloAltoNetworks/scm` provider version ~> 1.0.1 to create tags, address objects, and address groups organized by environment tier (web, app, data, DMZ) within the "Austin" folder. Authentication is performed via OAuth2 client credentials (client ID, client secret, scope, and auth URL) against the SCM API. The project creates 34 resources total: 6 tags, 18 addresses, and 10 address groups.

## Prerequisites

- Terraform >= 1.0
- A Strata Cloud Manager tenant with API access
- OAuth2 client credentials from the SCM console
- The "Austin" folder must exist in SCM
- A TSG ID for the scope parameter

> **New to Terraform?** Terraform uses three main commands: `terraform init` downloads provider plugins, `terraform plan` previews changes without applying them, and `terraform apply` executes the changes against your infrastructure.

## Quickstart

1. Clone the repository:
   ```bash
   git clone https://github.com/cdot65/paloaltonetworks-automation-examples.git
   cd paloaltonetworks-automation-examples/terraform/scm/basic-example
   ```

2. Create your variables file:
   ```bash
   cp terraform.tfvars.example terraform.tfvars
   ```

3. Edit `terraform.tfvars` with your SCM credentials.

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
provider "scm" {
  host          = "api.sase.paloaltonetworks.com"
  auth_url      = "https://auth.apps.paloaltonetworks.com/auth/v1/oauth2/access_token"
  client_id     = "your-client-id"
  client_secret = "your-client-secret"
  scope         = "tsg_id:12345"
  logging       = "quiet"
}
```

Alternatively, use environment variables:

```bash
export SCM_HOST="api.sase.paloaltonetworks.com"
export SCM_AUTH_URL="https://auth.apps.paloaltonetworks.com/auth/v1/oauth2/access_token"
export SCM_CLIENT_ID="your-client-id"
export SCM_CLIENT_SECRET="your-client-secret"
export SCM_SCOPE="tsg_id:12345"
```

> **Security note:** Never commit `terraform.tfvars` files containing credentials to version control. Add `*.tfvars` to your `.gitignore` file.

### Variables

| Variable | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `scm_host` | string | No | `api.sase.paloaltonetworks.com` | Hostname of the SCM API |
| `scm_auth_url` | string | No | `https://auth.apps.paloaltonetworks.com/auth/v1/oauth2/access_token` | OAuth2 token endpoint URL |
| `scm_client_id` | string | Yes | `""` | Client ID for authentication (sensitive) |
| `scm_client_secret` | string | Yes | `""` | Client secret for authentication (sensitive) |
| `scm_scope` | string | Yes | `""` | Client scope / TSG ID (sensitive) |
| `scm_auth_file` | string | No | `""` | Path to JSON auth credentials file |
| `scm_logging` | string | No | `quiet` | Provider logging level (quiet, action, path, info, debug) |
| `folder` | string | No | `Shared` | Folder for resource creation |
| `environment` | string | No | `development` | Environment name for tagging |
| `project_name` | string | No | `scm-test` | Project name for resource naming |

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

  # scm_address.api_endpoint will be created
  # scm_address.app_dev_subnet will be created
  # scm_address.app_prod_1 will be created
  # scm_address.app_prod_2 will be created
  # scm_address.app_prod_range will be created
  # scm_address.cdn_endpoint will be created
  # scm_address.db_dev_subnet will be created
  # scm_address.db_prod_1 will be created
  # scm_address.db_prod_2 will be created
  # scm_address.db_prod_range will be created
  # scm_address.dmz_proxy_1 will be created
  # scm_address.dmz_proxy_2 will be created
  # scm_address.dmz_subnet will be created
  # scm_address.web_dev_1 will be created
  # scm_address.web_dev_subnet will be created
  # scm_address.web_prod_1 will be created
  # scm_address.web_prod_2 will be created
  # scm_address.web_prod_subnet will be created
  # scm_address_group.all_prod_infrastructure will be created
  # scm_address_group.all_web_servers will be created
  # scm_address_group.dev_app_servers will be created
  # scm_address_group.dev_db_servers will be created
  # scm_address_group.dev_web_servers will be created
  # scm_address_group.dmz_servers will be created
  # scm_address_group.external_endpoints will be created
  # scm_address_group.prod_app_servers will be created
  # scm_address_group.prod_db_servers will be created
  # scm_address_group.prod_web_servers will be created
  # scm_tag.app_tier will be created
  # scm_tag.data_tier will be created
  # scm_tag.development will be created
  # scm_tag.dmz will be created
  # scm_tag.production will be created
  # scm_tag.web_tier will be created

Plan: 34 to add, 0 to change, 0 to destroy.
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
basic-example/
├── addresses.tf                   # 18 address objects (web, app, data, DMZ, FQDN)
├── address-groups.tf              # 10 address groups (prod, dev, combined, DMZ)
├── tags.tf                        # 6 tags (environment and tier classification)
├── outputs.tf                     # Detailed outputs by tier, group, and summary
├── provider.tf                    # SCM provider with OAuth2 configuration
├── variables.tf                   # Input variable declarations
├── versions.tf                    # Terraform and SCM provider version constraints
├── terraform.tfvars               # Variable values (do not commit)
└── README.md                      # This documentation
```

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Provider installation fails | Network or registry issues | Run `terraform init -upgrade` or check network connectivity |
| Invalid credentials | Wrong client_id, client_secret, or scope | Verify credentials in the SCM console under API Keys |
| Connection refused | SCM API unreachable | Check network/firewall rules; verify `scm_host` and `scm_auth_url` |
| Resource already exists | Object already exists in SCM folder | Delete from SCM UI or import with `terraform import` |
| State lock error | Concurrent Terraform runs | Wait for other run to finish or force unlock with `terraform force-unlock` |
| Provider version mismatch | Version constraint conflict | Run `terraform init -upgrade` to update the SCM provider |
| Folder not found | "Austin" folder does not exist in SCM | Create the folder manually in the SCM console first |
| Auth URL error | Incorrect OAuth2 endpoint | Verify `scm_auth_url` matches your SCM tenant region |

## Terraform Concepts Used

- **Provider**: The `scm` provider interfaces with Strata Cloud Manager via OAuth2 client credentials and an auth URL.
- **Resource**: Resources include `scm_tag` (6), `scm_address` (18), and `scm_address_group` (10) organized by environment tier.
- **Variable**: Input variables parameterize credentials, folder, environment, and project name.
- **Output**: Detailed outputs group resources by tier (web, app, data, DMZ, external) and by environment (production, development).
- **State**: Terraform tracks all 34 SCM resources in its state file for incremental updates.
- **Plan**: The `terraform plan` command previews SCM configuration changes before applying.
