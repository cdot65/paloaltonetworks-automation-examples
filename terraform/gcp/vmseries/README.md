# Palo Alto Networks VM-Series Firewall on Google Cloud Platform

## Overview

This project deploys a Palo Alto Networks VM-Series next-generation firewall on Google Cloud Platform using the Terraform `google` provider and the official `PaloAltoNetworks/swfw-modules` module. It creates VPC networks (management, untrust, trust) with subnets, firewall rules, an optional public IP for management access, and a VM-Series instance with three network interfaces. The `google` provider authenticates via Application Default Credentials or a service account key. The project requires Terraform >= 1.5 and the Google provider ~> 5.0.

## Prerequisites

- Terraform >= 1.5, < 2.0
- A GCP project with billing enabled
- `gcloud` CLI authenticated (`gcloud auth application-default login`)
- Compute Engine API enabled on the project
- SSH key pair for VM-Series access
- Sufficient quota for `n1-standard-4` (or chosen machine type) in the target zone

> **New to Terraform?** Terraform uses three main commands: `terraform init` downloads provider plugins, `terraform plan` previews changes without applying them, and `terraform apply` executes the changes against your infrastructure.

## Quickstart

1. Clone the repository:
   ```bash
   git clone https://github.com/cdot65/paloaltonetworks-automation-examples.git
   cd paloaltonetworks-automation-examples/terraform/gcp/vmseries
   ```

2. Create your variables file:
   ```bash
   cp terraform.tfvars.example terraform.tfvars
   ```

3. Edit `terraform.tfvars` with your GCP project ID, SSH keys, and network settings.

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

The Google provider authenticates using Application Default Credentials:

```hcl
provider "google" {
  project = "your-gcp-project-id"
  region  = "us-central1"
}
```

Set up credentials via:

```bash
gcloud auth application-default login
```

Or use a service account key:

```bash
export GOOGLE_CREDENTIALS="/path/to/service-account-key.json"
```

> **Security note:** Never commit `terraform.tfvars` files or service account keys to version control. Add `*.tfvars` and `*.json` to your `.gitignore` file.

### Variables

| Variable | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `project_id` | string | Yes | n/a | GCP project ID where resources will be created |
| `region` | string | No | `us-central1` | GCP region for resource deployment |
| `zone` | string | No | `us-central1-a` | GCP zone for resource deployment |
| `name_prefix` | string | No | `vmseries` | Prefix added to all resource names |
| `ssh_keys` | string | Yes | n/a | SSH public keys for VM-Series access (format: `username:ssh-rsa AAAA...`) |
| `vmseries_image_name` | string | No | `vmseries-flex-bundle2-1022` | VM-Series image from Palo Alto Networks public project |
| `machine_type` | string | No | `n1-standard-4` | GCE machine type for the VM-Series instance |
| `min_cpu_platform` | string | No | `Intel Skylake` | Minimum CPU platform (must match machine_type family) |
| `bootstrap_bucket_name` | string | No | `null` | GCS bucket name for bootstrap configuration |
| `bootstrap_options` | map(string) | No | `{}` | Bootstrap key-value options for VM-Series |
| `mgmt_network_name` | string | No | `mgmt-network` | Management VPC network name |
| `mgmt_subnet_name` | string | No | `mgmt-subnet` | Management subnet name |
| `mgmt_subnet_cidr` | string | No | `10.0.0.0/24` | Management subnet CIDR range |
| `untrust_network_name` | string | No | `untrust-network` | Untrust VPC network name |
| `untrust_subnet_name` | string | No | `untrust-subnet` | Untrust subnet name |
| `untrust_subnet_cidr` | string | No | `10.0.1.0/24` | Untrust subnet CIDR range |
| `trust_network_name` | string | No | `trust-network` | Trust VPC network name |
| `trust_subnet_name` | string | No | `trust-subnet` | Trust subnet name |
| `trust_subnet_cidr` | string | No | `10.0.2.0/24` | Trust subnet CIDR range |
| `create_networks` | bool | No | `true` | Whether to create new VPC networks or use existing ones |
| `allowed_mgmt_ips` | list(string) | No | `["0.0.0.0/0"]` | IP addresses/ranges allowed to access management interface |
| `tags` | list(string) | No | `["vmseries"]` | Network tags applied to resources |
| `scopes` | list(string) | No | (see variables.tf) | GCE service account scopes |
| `create_public_ip` | bool | No | `true` | Whether to attach a public IP to the management interface |

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

  # google_compute_address.mgmt[0] will be created
  # google_compute_firewall.mgmt_ingress will be created
  # google_compute_firewall.trust_ingress will be created
  # google_compute_firewall.untrust_ingress will be created
  # google_compute_network.mgmt[0] will be created
  # google_compute_network.trust[0] will be created
  # google_compute_network.untrust[0] will be created
  # google_compute_subnetwork.mgmt[0] will be created
  # google_compute_subnetwork.trust[0] will be created
  # google_compute_subnetwork.untrust[0] will be created
  # module.vmseries.google_compute_instance.this will be created

Plan: 11 to add, 0 to change, 0 to destroy.

Changes to Outputs:
  + mgmt_public_ip          = (known after apply)
  + mgmt_url                = (known after apply)
  + ssh_command              = (known after apply)
  + vmseries_instance_name  = "vmseries-fw"
  + vmseries_instance_id    = (known after apply)
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
vmseries/
├── main.tf                        # VPC networks, subnets, firewall rules, public IP, VM-Series module
├── outputs.tf                     # Instance name, IPs, management URL, SSH command
├── variables.tf                   # All input variable declarations
├── versions.tf                    # Terraform and Google provider version constraints
├── terraform.tfvars.example       # Example variable values with documentation
├── terraform.tfvars               # Your variable values (do not commit)
└── README.md                      # This documentation
```

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Provider installation fails | Network or registry issues | Run `terraform init -upgrade` or check network connectivity |
| Invalid credentials | ADC not configured or expired | Run `gcloud auth application-default login` |
| Connection refused / API not enabled | Compute Engine API disabled | Enable via `gcloud services enable compute.googleapis.com` |
| Resource already exists | Network/instance name collision | Change `name_prefix` or delete existing resources |
| State lock error | Concurrent Terraform runs | Wait for other run to finish or force unlock with `terraform force-unlock` |
| Quota exceeded | Insufficient CPU/IP quota | Request quota increase in GCP Console |
| Image not found | Invalid `vmseries_image_name` | List available images: `gcloud compute images list --project=paloaltonetworksgcp-public --filter="name~vmseries-flex"` |
| CPU platform incompatible | Wrong `min_cpu_platform` for machine type | n1 machines support up to Skylake; n2 supports Cascade Lake+ |

## Terraform Concepts Used

- **Provider**: The `google` provider manages GCP resources using Application Default Credentials.
- **Resource**: GCP resources include VPC networks, subnets, firewall rules, and static IP addresses.
- **Module**: The `PaloAltoNetworks/swfw-modules/google//modules/vmseries` module handles VM-Series instance creation with proper network interface configuration.
- **Variable**: Input variables parameterize project, region, network CIDRs, machine type, and VM-Series image.
- **Output**: Outputs expose the management IP, SSH command, instance name, and management URL.
- **State**: Terraform tracks all GCP resources in its state file for incremental updates.
- **Plan**: The `terraform plan` command previews all infrastructure changes before applying.
