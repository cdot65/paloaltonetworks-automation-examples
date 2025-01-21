# Terraform Project: Deploy a Debian Linux VM on VMware vCenter

This Terraform project automates the deployment of a Debian Linux virtual machine (VM) on VMware vCenter. The VM is configured with specific resources (CPU, memory, disk), a static IP address, and tags for workload identification.

## Prerequisites

Before using this project, ensure you have the following:

1. **Terraform Installed**: Download and install Terraform from [here](https://www.terraform.io/downloads.html).
2. **VMware vCenter Access**: You need credentials (username and password) for a vCenter account with sufficient permissions to create and manage VMs.
3. **Debian Template**: A Debian template or VM must be available in your vCenter environment for cloning.
4. **Environment Variables**: For sensitive data like `vcenter_user` and `vcenter_password`, use environment variables or a secrets management tool.

## Project Structure

The project consists of the following files:

### 1. `provider.tf`
- **Purpose**: Configures the VMware vSphere provider, which allows Terraform to interact with your vCenter environment.
- **Key Settings**:
  - `user`: vCenter username.
  - `password`: vCenter password.
  - `vsphere_server`: Address of your vCenter server.
  - `allow_unverified_ssl`: Set to `true` to disable SSL certificate verification (use only in development environments).

### 2. `variables.tf`
- **Purpose**: Defines the input variables used in the project. These variables are used to customize the VM deployment.
- **Key Variables**:
  - `vcenter_user`, `vcenter_password`, `vcenter_server`: Credentials for vCenter access.
  - `datacenter_name`, `datastore_name`, `cluster_name`, `network_name`, `host_name`: Details about your vCenter environment.
  - `template_name`: Name of the Debian template to clone.
  - `vm_name`, `vm_ipv4_address`, `vm_ipv4_netmask`, `vm_ipv4_gateway`: Configuration for the VM.
  - `vm_cpu_count`, `vm_memory`, `vm_disk_size`: Resource allocation for the VM.
  - `tags`: List of tags to associate with the VM.

### 3. `terraform.tfvars`
- **Purpose**: Provides values for the variables defined in `variables.tf`. This file is used to customize the deployment without modifying the code.
- **Example**:
  ```hcl
  vcenter_user           = "your_vcenter_user"
  vcenter_password       = "your_vcenter_password"
  vcenter_server         = "vcenter.example.io"
  datacenter_name        = "Datacenter"
  datastore_name         = "datastore1"
  cluster_name           = "Cluster"
  network_name           = "database"
  host_name              = "esx1.example.io"
  template_name          = "debian-template"
  vm_name                = "postgres-vm"
  vm_ipv4_address        = "192.168.1.100"
  vm_ipv4_netmask        = 24
  vm_ipv4_gateway        = "192.168.1.1"
  vm_domain              = "example.io"
  vm_cpu_count           = 4
  vm_memory              = 4096
  vm_disk_size           = 24
  tags                   = ["postgres", "database"]
  ```

### 4. `main.tf`
- **Purpose**: Contains the main Terraform configuration for deploying the VM.
- **Key Resources**:
  - **Data Sources**: Fetch information about the datacenter, datastore, cluster, network, host, and template.
  - **VM Resource**: Defines the VM configuration, including CPU, memory, disk, network, and customization.
  - **Tags**: Creates and associates tags with the VM for workload identification.

### 5. `outputs.tf`
- **Purpose**: Defines the outputs that Terraform will display after the deployment.
- **Example Outputs**:
  - `vm_id`: The ID of the deployed VM.
  - `vm_ipv4_address`: The static IPv4 address of the VM.
  - `vm_tags`: The tags associated with the VM.

---

## How to Use This Project

### Step 1: Clone the Repository
Clone this repository to your local machine:
```bash
git clone https://github.com/cdot65/paloaltonetworks-automation-examples.git
cd terraform/vcenter_debian_database
```

### Step 2: Customize the Configuration
1. Open `terraform.tfvars` and update the values to match your vCenter environment and VM requirements.
2. If you prefer to use environment variables for sensitive data, set them as follows:
   ```bash
   export TF_VAR_vcenter_user="your_vcenter_user"
   export TF_VAR_vcenter_password="your_vcenter_password"
   ```

### Step 3: Initialize Terraform
Run the following command to initialize Terraform and download the required provider plugins:
```bash
terraform init
```

### Step 4: Review the Execution Plan
Run the following command to see what Terraform will do:
```bash
terraform plan
```

### Step 5: Deploy the VM
Apply the configuration to deploy the VM:
```bash
terraform apply
```
Confirm the action by typing `yes` when prompted.

### Step 6: Verify the Deployment
After the deployment is complete, Terraform will display the outputs (e.g., VM ID, IP address). You can also log in to your vCenter console to verify the VM.

### Step 7: Destroy the VM (Optional)
To clean up and delete the VM, run:
```bash
terraform destroy
```

---

## Notes
- **SSL Verification**: The `allow_unverified_ssl` setting is disabled in this configuration. For production environments, ensure your vCenter server has a valid SSL certificate and set this to `false`.
- **Sensitive Data**: Avoid committing sensitive data (e.g., `terraform.tfvars`) to version control. Use `.gitignore` to exclude these files.

---

## Troubleshooting
- **Data Source Errors**: If Terraform fails to fetch data (e.g., datacenter, template), double-check the names in `terraform.tfvars`.
- **VM Customization Issues**: Ensure the Debian template is properly configured for customization (e.g., cloud-init or VMware tools installed).

---

Feel free to reach out if you have any questions or need further assistance!