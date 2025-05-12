# Texas Address Objects

This Terraform configuration creates address objects in the Palo Alto Networks Strata Cloud Manager (SCM) under the "Texas" folder.

## Prerequisites

- Terraform v1.0.0 or newer
- Access to Palo Alto Networks Strata Cloud Manager (SCM)
- SCM API credentials with appropriate permissions

## Usage

1. Clone this repository
2. Create a `terraform.tfvars` file based on the example:

   ```bash
   cp terraform.tfvars.example terraform.tfvars
   ```

3. Edit `terraform.tfvars` with your SCM credentials

4. Initialize the Terraform workspace:

   ```bash
   terraform init
   ```

5. Validate the configuration:

   ```bash
   terraform validate
   ```

6. Preview changes:

   ```bash
   terraform plan
   ```

7. Apply the configuration:

   ```bash
   terraform apply
   ```

8. When finished, you can destroy the resources:

   ```bash
   terraform destroy
   ```

## Address Objects Created

This configuration creates the following address objects:

- **Office Locations**
  - Dallas Office (`dallas-office`)
  - Austin Office (`austin-office`)
  - Houston Office (`houston-office`)
  - San Antonio Office (`san-antonio-office`)
  - Fort Worth Office (`fort-worth-office`)

- **Data Center and Servers**
  - Texas Data Center (`texas-datacenter`)
  - Texas Development Server (`texas-dev-server`)
  - Texas Web Server (`texas-web-server`)
  - Texas Database Server (`texas-db-server`)

- **Public IP Range**
  - Texas Public IPs (`texas-public-ips`)

## Notes

- The "Texas" folder must exist in SCM before running this configuration. Folder creation may need to be done manually in the SCM interface.
- All resources are tagged appropriately for easier management and policy creation.
- This configuration uses fictitious IP addresses. Replace with actual network addresses before using in production.

## Security Considerations

- Do not commit `terraform.tfvars` to version control as it contains sensitive credentials.
- Consider using environment variables or a secrets manager for production deployments.