# Basic PAN-OS Configuration 📚

This README provides an overview of our Terraform project and guides you through the setup and execution process. 🚀

## Table of Contents

- [Basic PAN-OS Configuration 📚](#basic-pan-os-configuration-)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Prerequisites](#prerequisites)
  - [Setup](#setup)
    - [Creating a Terraform Environment](#creating-a-terraform-environment)
    - [Installing Dependencies](#installing-dependencies)
  - [Project Structure](#project-structure)
  - [Execution Workflow](#execution-workflow)
    - [Screenshots](#screenshots)

## Overview

Our Terraform project aims to manage the configuration of PAN-OS devices like firewalls and Panorama. It includes setting up ethernet interfaces, virtual routers, security zones, service objects, NAT policies, and security policies. 🎯

## Prerequisites

Before getting started, ensure that you have the following prerequisites installed on your local machine:

- Terraform (version 1.20+) 🔧

## Setup

### Creating a Terraform Environment

To create a Terraform environment, follow these steps:

1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Create a `terraform.tfvars` file and provide the necessary variable values (see `terraform.tfvars` for reference).

### Installing Dependencies

Install our project's dependencies:

```bash
terraform init
```

## Project Structure

Our project consists of the following Terraform files:

- `configure_panos.tf`: Contains resource definitions for configuring PAN-OS devices, including ethernet interfaces, virtual routers, security zones, service objects, NAT policies, and security policies.
- `variables.tf`: Defines input variables used in the configuration.
- `terraform.tfvars`: Provides values for the defined variables.
- `panos_provider.tf`: Configures the PAN-OS provider for Terraform.

These files work together to manage the configuration of PAN-OS devices. The `configure_panos.tf` file uses the variables defined in `variables.tf` and the values provided in `terraform.tfvars` to create the necessary resources on the PAN-OS device specified in `panos_provider.tf`.

## Execution Workflow

To execute our Terraform project, follow these steps:

1. Ensure you have completed the setup steps mentioned above.
2. Run the following command to preview the changes:

    ```bash
    terraform plan
    ```

3. If the plan looks good, apply the changes:

    ```bash
    terraform apply
    ```

4. Confirm the execution by typing `yes` when prompted.

### Screenshots

Here are some screenshots showcasing the execution of our PAN-OS configuration management:

![Screenshot 1](screenshots/screenshot1.png)

![Screenshot 2](screenshots/screenshot2.png)

Feel free to explore the project and customize it according to your specific requirements. Happy automating! 😄
