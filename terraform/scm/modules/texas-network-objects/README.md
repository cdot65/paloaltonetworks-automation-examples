# Texas Network Objects

This Terraform configuration creates tags, services, and service groups in the Palo Alto Networks Strata Cloud Manager (SCM) under the "Texas" folder.

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

## Resources Created

### Tags

- **Location Tags**: Texas, Dallas, Austin, Houston, San Antonio, Fort Worth
- **Environment Tags**: Production, Development, Staging
- **Infrastructure Tags**: Datacenter, WebServer, Database
- **Management Tags**: Automation, Terraform

### Services

- **Web Services**: 
  - HTTP (tcp/80)
  - HTTPS (tcp/443)
- **Database Services**:
  - MySQL (tcp/3306)
  - Microsoft SQL (tcp/1433)
  - PostgreSQL (tcp/5432)
- **Management Services**:
  - SSH (tcp/22)
  - RDP (tcp/3389)
- **Application Services**:
  - Custom TCP Application (tcp/8080-8090)
  - Custom UDP Application (udp/9000-9010)

### Service Groups

- **Web Services Group**: Contains HTTP and HTTPS services
- **Database Services Group**: Contains MySQL, MSSQL, and PostgreSQL services
- **Management Services Group**: Contains SSH and RDP services
- **Application Services Group**: Contains custom TCP and UDP services
- **All Texas Services Group**: Contains all service groups

## Dependency Handling

Terraform automatically manages dependencies between resources:

1. Tags are created first
2. Services are created with references to tags
3. Service groups are created with references to services
4. The "All Texas Services" group references other service groups

## Notes

- The "Texas" folder must exist in SCM before running this configuration. Folder creation may need to be done manually in the SCM interface.
- All resources are cross-referenced using implicit dependencies in Terraform's resource graph.
- This configuration uses standard port numbers. Adjust as needed for your environment.

## Security Considerations

- Do not commit `terraform.tfvars` to version control as it contains sensitive credentials.
- Consider using environment variables or a secrets manager for production deployments.