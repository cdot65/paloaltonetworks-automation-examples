# Terraform Examples

8 Terraform configurations for provisioning and managing Palo Alto Networks infrastructure across PAN-OS, Strata Cloud Manager, GCP, and vCenter.

## Project Categories

| Category | Count | Description |
|----------|-------|-------------|
| [PAN-OS Provider](panos.md) | 4 | Firewall configuration with provider v1 and v2 |
| [Strata Cloud Manager](scm.md) | 2 | SCM address objects, groups, tags, services |
| [GCP VM-Series](gcp.md) | 1 | VM-Series NGFW deployment on Google Cloud |
| [vCenter Deployment](vcenter.md) | 1 | Debian VM deployment on vSphere |

## Common Workflow

All Terraform projects follow the same workflow:

```bash
# 1. Copy and fill in variables
cp terraform.tfvars.example terraform.tfvars

# 2. Initialize providers and modules
terraform init

# 3. Preview changes
terraform plan

# 4. Apply configuration
terraform apply

# 5. Tear down when done
terraform destroy
```

!!! warning "Credentials"
    Store credentials in `terraform.tfvars` (git-ignored) or use environment variables. Never commit real credentials.

## Providers Used

| Provider | Version | Used For |
|----------|---------|----------|
| `paloaltonetworks/panos` v1 | 1.11.1 | PAN-OS firewall configuration (basic-config, dynamic-address-groups) |
| `paloaltonetworks/panos` v2 | latest | PAN-OS NGFW and Panorama (firewall-config, provider-v2-example) |
| `scm` | latest | Strata Cloud Manager resources |
| `google` | latest | GCP infrastructure for VM-Series |
| `vsphere` | latest | vCenter VM deployment |
