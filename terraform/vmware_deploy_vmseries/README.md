# VMware Deploy VM-Series 📚

This README provides an overview of our Terraform project and guides you through the setup and execution process. 🚀

## Table of Contents

- [VMware Deploy VM-Series 📚](#vmware-deploy-vm-series-)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Prerequisites](#prerequisites)
  - [Setup](#setup)
    - [Creating a Terraform Environment](#creating-a-terraform-environment)
    - [Installing Dependencies](#installing-dependencies)
  - [Project Structure](#project-structure)
  - [Terraform Provider Configuration](#terraform-provider-configuration)
  - [Terraform Resources](#terraform-resources)
  - [Terraform Variables](#terraform-variables)
  - [Terraform Variable Definitions](#terraform-variable-definitions)
  - [Execution Workflow](#execution-workflow)
  - [Example Workflow for Deploying VMs](#example-workflow-for-deploying-vms)
    - [Screenshots](#screenshots)

## Overview

Our Terraform project aims to manage the deployment and configuration of PAN-OS Virtual Machines on a vSphere environment. 🎯

## Prerequisites

Before getting started, ensure that you have the following prerequisites installed on your local machine:

- Terraform (version 1.20+) 🔧
- vSphere environment

## Setup

### Creating a Terraform Environment

To create a Terraform environment, follow these steps:

1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Create `fw1.tfvars`, `fw2.tfvars`, and `shared.tfvars` files and provide the necessary variable values (see provided tfvars files for reference).

### Installing Dependencies

Install our project's dependencies:

```bash
terraform init
```

## Project Structure

Our project consists of the following Terraform files:

- `fw1.tfvars`: Contains configuration values for the first firewall VM.
- `fw2.tfvars`: Contains configuration values for the second firewall VM.
- `shared.tfvars`: Contains shared configuration values used by both firewall VMs.
- `variables.tf`: Defines input variables used in the configuration.
- `vmseries.tf`: Contains resource definitions for deploying and configuring the PAN-OS Virtual Machines.

These files work together to deploy and manage the PAN-OS Virtual Machines on a vSphere environment. The `vmseries.tf` file uses the variables defined in `variables.tf` and the values provided in `fw1.tfvars`, `fw2.tfvars`, and `shared.tfvars` to create the necessary resources.

## Terraform Provider Configuration

The `vmseries.tf` file contains the configuration for the vSphere provider in Terraform. It specifies the connection details for the vSphere environment.

In our example, the `vmseries.tf` file includes the following:

- `provider` block:
    - `vsphere` provider:
    - `vsphere_server`: Specifies the vCenter server FQDN or IP, using the value from the `vsphere_server` variable.
    - `user`: Sets the username for authentication, using the value from the `user` variable.
    - `password`: Sets the password for authentication, using the value from the `password` variable.
    - `allow_unverified_ssl`: Allows unverified SSL connections.

This configuration ensures that the vSphere provider is properly initialized and connected to the specified vSphere environment using the provided connection details.

## Terraform Resources

The `vmseries.tf` file defines several Terraform resources to manage the deployment and configuration of PAN-OS Virtual Machines. Here's a brief explanation of each resource:

- `vsphere_datacenter`: Fetches data about the specified vSphere datacenter.
- `vsphere_compute_cluster`: Fetches data about the specified vSphere compute cluster.
- `vsphere_host`: Fetches data about the specified vSphere host.
- `vsphere_datastore`: Fetches data about the specified vSphere datastore.
- `vsphere_network`: Fetches data about the specified vSphere networks (management, untrust, trust).
- `vsphere_virtual_machine`: Deploys a PAN-OS VM from a specified template with custom configurations.
- `local_file`: Creates local bootstrap files for VM configuration.
- `null_resource`: Executes a local command to create an ISO file for bootstrapping the VM.
- `vsphere_file`: Uploads the created ISO file to the specified datastore in vSphere.
- `vsphere_folder`: Creates a folder in vSphere to store the VM.

These resources are created and managed by Terraform based on the configuration provided in the `vmseries.tf` file and the values defined in `variables.tf` and the `*.tfvars` files.

## Terraform Variables

The `*.tfvars` files are used to provide values for the input variables defined in the `variables.tf` file. They allow you to customize the configuration without modifying the main Terraform files.

Here's an overview of the provided `*.tfvars` files:

- `fw1.tfvars`

```hcl
// vSphere specifications
vsphere_vm_name   = "fw-01"
vsphere_vm_folder = "fw-01"

// VM specific parameters
pavm_hostname   = "fw-01"
pavm_ip_address = "10.0.0.251"

// Panorama details
# panorama_vm_auth_key = ""
```

- `fw2.tfvars`

```hcl
// vSphere specifications
vsphere_vm_name   = "fw-02"
vsphere_vm_folder = "fw-02"

// VM specific parameters
pavm_hostname   = "fw-02"
pavm_ip_address = "10.0.0.252"

// Panorama details
# panorama_vm_auth_key = ""
```

- `shared.tfvars`

```hcl
// vSphere Authentication
user           = "automation@vsphere.local"
vsphere_server = "10.0.0.2"
password       = "mysecretpassword"

// vSphere specifications
vsphere_datacenter         = "Redtail"
vsphere_vm_template        = "PA-VM-ESX-10.2.3"
vsphere_cluster            = "headquarters"
vsphere_host               = "dal-esx-01"
vsphere_vcpu_number        = "2"
vsphere_memory_size        = "6656"
vsphere_datastore          = "dal-dst-03"
vsphere_port_group_mgmt    = "Management"
vsphere_port_group_untrust = "Dallas_WAN"
vsphere_port_group_trust   = "Dallas_DMZ"

// VM specific parameters
pavm_netmask       = "/16"
pavm_gateway       = "10.0.0.1"
pavm_dns_primary   = "10.30.0.50"
pavm_dns_secondary = "10.30.0.51"
pavm_authcode      = "MYAUTHCODE"

// Panorama details
panorama_server_ip = "10.0.0.46"
panorama_tplname   = "BaseTemplate"
panorama_dgname    = "branch"
# panorama_vm_auth_key = ""
```

## Terraform Variable Definitions

The `variables.tf` file defines the input variables used in the Terraform configuration. It specifies the structure and type of each variable, allowing you to parameterize the configuration.

In `variables.tf`, the input variables are defined as follows:

```hcl
// vCenter connection

variable "user" {
    description = "vSphere user name"
}

variable "password" {
    description = "vSphere password"
}

variable "vsphere_server" {
    description = "vCenter server FQDN or IP"
}

...

variable "pavm_authcode" {
    description = "VM-Series license auth code (Optional)"
}
```

## Execution Workflow

To execute our Terraform project, follow these steps:

1. Ensure you have completed the setup steps mentioned above.
2. Run the following command to preview the changes:

    ```shell
    terraform plan
    ```

3. If the plan looks good, apply the changes:

    ```shell
    terraform apply
    ```

4. Confirm the execution by typing `yes` when prompted.

## Example Workflow for Deploying VMs

Follow these steps to deploy different hosts using unique variable files:

1. Initialize the providers

    ```bash
    terraform init
    ```

2. Create a workspace and deploy the first firewall (fw1)

    ```bash
    terraform workspace new fw1
    terraform plan --var-file shared.tfvars --var-file fw1.tfvars
    terraform apply --var-file shared.tfvars --var-file fw1.tfvars
    ```

3. Create a workspace and deploy the second firewall (fw2)

    ```bash
    terraform workspace new fw2
    terraform plan --var-file shared.tfvars --var-file fw2.tfvars
    terraform apply --var-file shared.tfvars --var-file fw2.tfvars
    ```

### Screenshots

Here are some screenshots showcasing the execution of our PAN-OS configuration management:

`terraform init`

![Screenshot 1](screenshots/screenshot1.png)

`terraform plan`

![Screenshot 2](screenshots/screenshot2.png)

`terraform apply`

![Screenshot 3](screenshots/screenshot3.png)

Feel free to explore the project and customize it according to your specific requirements. Happy automating! 😄
