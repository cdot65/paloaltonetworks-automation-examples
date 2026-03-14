# Quick Start Guide

Get up and running with the SCM Terraform provider in 5 minutes.

## Step 1: Prerequisites

Ensure you have:

- Terraform installed (v1.0+)
- SCM API credentials (client_id, client_secret, scope)
- Access to a Strata Cloud Manager tenant with the Austin folder

## Step 2: Set Up Authentication

The fastest way is using environment variables:

```bash
export SCM_CLIENT_ID="your-client-id"
export SCM_CLIENT_SECRET="your-client-secret"
export SCM_SCOPE="tsg_id:your-tenant-id"
```

**Important:** The scope must be in the format `tsg_id:1234567890`, not just the numeric ID.

Alternatively, create a `terraform.tfvars` file:

```bash
cp terraform.tfvars.example terraform.tfvars
```

Edit `terraform.tfvars` with your credentials:

```hcl
scm_client_id     = "your-client-id"
scm_client_secret = "your-client-secret"
scm_scope         = "tsg_id:your-tenant-id"
```

## Step 3: Initialize Terraform

```bash
terraform init
```

## Step 4: Customize Variables (Optional)

Edit `terraform.tfvars` to customize your deployment:

```hcl
folder       = "Austin"        # SCM folder where resources will be created
environment  = "development"   # Environment name for resource naming
project_name = "scm-test"      # Project identifier
```

## Step 5: Preview Changes

```bash
terraform plan
```

Review the planned changes to ensure they match your expectations.

## Step 6: Apply Configuration

```bash
terraform apply
```

Type `yes` when prompted.

## Step 7: Verify

Log into your Strata Cloud Manager console and verify the resources were created in the Austin folder.

## Using Make (Optional)

If you prefer using Make:

```bash
make init      # Initialize
make validate  # Validate config
make plan      # Preview changes
make apply     # Apply changes
```

## What Gets Created

The default configuration creates **34 resources** in the Austin folder:

### Tags (6)
- production
- development
- web-tier
- app-tier
- data-tier
- dmz

### Address Objects (18)
- **Web Tier**: 5 addresses (prod servers, dev servers, subnets)
- **App Tier**: 4 addresses (prod servers with ranges, dev subnet)
- **Data Tier**: 4 addresses (prod database servers with ranges, dev subnet)
- **DMZ**: 3 addresses (proxy servers and subnet)
- **External**: 2 FQDN addresses (API and CDN endpoints)

### Address Groups (10)
- **Production Groups**: prod-web-servers, prod-app-servers, prod-db-servers
- **Development Groups**: dev-web-servers, dev-app-servers, dev-db-servers
- **Combined Groups**: all-web-servers, dmz-servers, external-endpoints, all-prod-infrastructure

## Resource Dependencies

The configuration demonstrates proper dependency management:

1. **Tags** are created first
2. **Address objects** depend on tags
3. **Address groups** depend on both tags and address objects

This ensures resources are created in the correct order.

## Viewing Outputs

After applying, you can view comprehensive outputs:

```bash
# View all outputs
terraform output

# View specific output
terraform output tags
terraform output address_objects_web_tier
terraform output resource_summary
```

## Cleanup

To remove all created resources:

```bash
terraform destroy
```

Or:

```bash
make destroy
```

Type `yes` when prompted to confirm deletion.

## Next Steps

1. Review the configuration files:
   - `tags.tf` - Tag definitions
   - `addresses.tf` - Address object definitions
   - `address-groups.tf` - Address group definitions
   - `outputs.tf` - Output definitions

2. Modify the configuration to match your environment:
   - Add more address objects to `addresses.tf`
   - Create additional groups in `address-groups.tf`
   - Add new tags in `tags.tf`

3. Explore additional SCM resources:
   - Security rules
   - NAT rules
   - Service objects
   - Application filters

4. Check out the README.md for detailed documentation

## Common Commands

```bash
# Format code
terraform fmt

# Validate configuration
terraform validate

# Show current state
terraform show

# List resources
terraform state list

# Show specific resource
terraform state show scm_tag.production

# Get help
terraform --help
```

## Troubleshooting

### Authentication errors?

- Double-check your credentials
- Verify scope format is `tsg_id:1234567890`
- Ensure credentials haven't expired
- Confirm proper SCM permissions

### Resources failing to create?

- Verify the Austin folder exists in your SCM tenant
- Check you have write permissions to the folder
- Review error messages in the output
- Enable debug logging: `export TF_LOG=DEBUG`

### Folder mismatch errors?

- Tags and address objects MUST be in the same folder
- All resources in this example use the "Austin" folder
- Update the `folder` parameter in all files if using a different folder

### Need more help?

- Check the README.md
- Review provider docs: <https://registry.terraform.io/providers/PaloAltoNetworks/scm/1.0.1>
- Enable debug logging: `export TF_LOG=DEBUG`
- Set provider logging: `scm_logging = "debug"` in terraform.tfvars

## Important Notes

1. **Folder Consistency**: All resources must use the same folder name
2. **Scope Format**: Must be `tsg_id:XXXXXXXX`, not just the numeric ID
3. **Wildcard Addresses**: Cannot have tags assigned (SCM limitation)
4. **Dependencies**: Explicitly defined with `depends_on` for proper ordering
