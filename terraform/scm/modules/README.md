# Strata Cloud Manager Modular Configuration

## Overview

This project demonstrates a modular approach to managing Palo Alto Networks Strata Cloud Manager (SCM) resources using the Terraform `scm` provider. It uses the `paloaltonetworks/scm` provider version >= 0.10.1 and organizes resources into two child modules: `texas-address-objects` (address objects and address groups) and `texas-network-objects` (tags, services, and service groups). Authentication is performed via OAuth2 client credentials (client ID, client secret, and scope) against the SCM API. The root module provides scaffolding for composing these modules together.

## Prerequisites

- Terraform >= 1.5.7
- A Strata Cloud Manager tenant with API access
- OAuth2 client credentials (client ID and client secret) from the SCM console
- A TSG ID for the `scope` parameter
- The target folder (default: "Texas") must exist in SCM

> **New to Terraform?** Terraform uses three main commands: `terraform init` downloads provider plugins, `terraform plan` previews changes without applying them, and `terraform apply` executes the changes against your infrastructure.

## Quickstart

1. Clone the repository:
   ```bash
   git clone https://github.com/cdot65/paloaltonetworks-automation-examples.git
   cd paloaltonetworks-automation-examples/terraform/scm/modules
   ```

2. Create your variables file (for the desired child module):
   ```bash
   cd texas-address-objects
   cp terraform.tfvars.example terraform.tfvars
   ```

3. Edit `terraform.tfvars` with your SCM credentials and scope.

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
  host          = "api.strata.paloaltonetworks.com"
  client_id     = "your-client-id@12345"
  client_secret = "your-client-secret"
  scope         = "tsg_id:12345"
}
```

Alternatively, use environment variables:

```bash
export SCM_HOST="api.strata.paloaltonetworks.com"
export SCM_CLIENT_ID="your-client-id@12345"
export SCM_CLIENT_SECRET="your-client-secret"
export SCM_SCOPE="tsg_id:12345"
```

> **Security note:** Never commit `terraform.tfvars` files containing credentials to version control. Add `*.tfvars` to your `.gitignore` file.

### Variables

#### texas-address-objects module

| Variable | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `scm_host` | string | No | `api.strata.paloaltonetworks.com` | Hostname of the SCM API |
| `client_id` | string | Yes | n/a | Client ID for SCM API authentication (sensitive) |
| `client_secret` | string | Yes | n/a | Client secret for SCM API authentication (sensitive) |
| `scope` | string | Yes | n/a | Scope for SCM API authentication (e.g., `tsg_id:12345`) |
| `folder_name` | string | No | `Texas` | Folder where address objects will be created |

#### texas-network-objects module

| Variable | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `scm_host` | string | No | `api.strata.paloaltonetworks.com` | Hostname of the SCM API |
| `client_id` | string | Yes | n/a | Client ID for SCM API authentication (sensitive) |
| `client_secret` | string | Yes | n/a | Client secret for SCM API authentication (sensitive) |
| `scope` | string | Yes | n/a | Scope for SCM API authentication (e.g., `tsg_id:12345`) |
| `folder_name` | string | No | `Texas` | Folder where network objects will be created |

## Usage

Navigate to a child module directory, then:

Preview changes:
```bash
terraform plan
```

Apply the configuration:
```bash
terraform apply
```

Expected `terraform plan` output for `texas-address-objects`:

```
Terraform will perform the following actions:

  # scm_address_group.texas will be created
  # scm_address_object.austin_office will be created
  # scm_address_object.dallas_office will be created
  # scm_address_object.fort_worth_office will be created
  # scm_address_object.houston_office will be created
  # scm_address_object.san_antonio_office will be created
  # scm_address_object.texas_datacenter will be created
  # scm_address_object.texas_db_server will be created
  # scm_address_object.texas_dev_server will be created
  # scm_address_object.texas_public_ips will be created
  # scm_address_object.texas_web_server will be created

Plan: 11 to add, 0 to change, 0 to destroy.
```

Expected `terraform plan` output for `texas-network-objects`:

```
Terraform will perform the following actions:

  # scm_service.app_custom_tcp will be created
  # scm_service.app_custom_udp will be created
  # scm_service.db_mssql will be created
  # scm_service.db_mysql will be created
  # scm_service.db_postgres will be created
  # scm_service.mgmt_rdp will be created
  # scm_service.mgmt_ssh will be created
  # scm_service.web_http will be created
  # scm_service.web_https will be created
  # scm_service_group.all_texas_services will be created
  # scm_service_group.application_services will be created
  # scm_service_group.database_services will be created
  # scm_service_group.management_services will be created
  # scm_service_group.web_services will be created
  # scm_tag.automation_tag will be created
  # scm_tag.austin_tag will be created
  # scm_tag.dallas_tag will be created
  # scm_tag.database_tag will be created
  # scm_tag.datacenter_tag will be created
  # scm_tag.development_tag will be created
  # scm_tag.fort_worth_tag will be created
  # scm_tag.houston_tag will be created
  # scm_tag.production_tag will be created
  # scm_tag.san_antonio_tag will be created
  # scm_tag.staging_tag will be created
  # scm_tag.terraform_tag will be created
  # scm_tag.texas_tag will be created
  # scm_tag.web_server_tag will be created

Plan: 28 to add, 0 to change, 0 to destroy.
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
modules/
├── main.tf                                # Root module scaffolding
├── outputs.tf                             # Root module outputs (placeholder)
├── variables.tf                           # Root module variables (placeholder)
├── versions.tf                            # Terraform and SCM provider version constraints
├── README.md                              # This documentation
├── texas-address-objects/                  # Address objects child module
│   ├── main.tf                            # 10 address objects + 1 address group
│   ├── outputs.tf                         # Address object and group IDs
│   ├── provider.tf                        # SCM provider configuration
│   ├── variables.tf                       # Module input variables
│   └── terraform.tfvars.example           # Example variable values
└── texas-network-objects/                  # Network objects child module
    ├── tags.tf                            # 14 tags (location, environment, infrastructure)
    ├── services.tf                        # 9 services (web, database, management, application)
    ├── service_groups.tf                  # 5 service groups
    ├── outputs.tf                         # Tag, service, and service group IDs
    ├── provider.tf                        # SCM provider configuration
    ├── variables.tf                       # Module input variables
    └── terraform.tfvars.example           # Example variable values
```

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Provider installation fails | Network or registry issues | Run `terraform init -upgrade` or check network connectivity |
| Invalid credentials | Wrong client_id or client_secret | Verify credentials in the SCM console under API Keys |
| Connection refused | SCM API unreachable | Check network/firewall rules and verify `scm_host` value |
| Resource already exists | Object already exists in SCM folder | Delete from SCM UI or import with `terraform import` |
| State lock error | Concurrent Terraform runs | Wait for other run to finish or force unlock with `terraform force-unlock` |
| Provider version mismatch | Version constraint conflict | Run `terraform init -upgrade` to update the SCM provider |
| Folder not found | Target folder does not exist in SCM | Create the folder manually in the SCM console first |

## Terraform Concepts Used

- **Provider**: The `scm` provider interfaces with Strata Cloud Manager via OAuth2 client credentials.
- **Resource**: SCM resources include `scm_address_object`, `scm_address_group`, `scm_tag`, `scm_service`, and `scm_service_group`.
- **Module**: Child modules (`texas-address-objects`, `texas-network-objects`) encapsulate related resources for reuse and organization.
- **Variable**: Input variables parameterize credentials, API host, and folder name across modules.
- **Output**: Outputs expose resource IDs and membership lists for downstream consumption.
- **State**: Terraform tracks all SCM resources in its state file for incremental updates.
- **Plan**: The `terraform plan` command previews SCM configuration changes before applying.
