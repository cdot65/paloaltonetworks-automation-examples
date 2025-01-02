# PAN-OS Infrastructure as Code with Terraform
Terraform configuration for PAN-OS Panorama management using the panos provider v2.0.0 alpha.

## Table of Contents
- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
- [Configuration Structure](#configuration-structure)
- [Core Concepts](#core-concepts)
- [Usage](#usage)

## Overview
This project provides infrastructure as code capabilities for PAN-OS using Terraform. It manages Panorama configuration including templates, device groups, and security policies.

## Prerequisites
- Terraform v1.5.0+
- PAN-OS Provider v2.0.0-alpha
- Panorama credentials
- Basic understanding of Panorama configuration hierarchy

## Getting Started

### Installation
1. Download Terraform from [terraform.io](https://terraform.io)
2. Configure provider:
```hcl
provider "panos" {
  hostname = "panorama.example.com"
  username = "admin"
  password = "password"
}
```

### Basic Commands
- `terraform init` - Initialize provider
- `terraform plan` - Preview changes 
- `terraform apply` - Apply changes
- `terraform destroy` - Remove infrastructure

## Configuration Structure

### Main Components
This project configures:
- Templates & Template Stacks
- Device Groups & Hierarchy
- Security Zones
- Address Objects & Groups
- Service Objects & Groups
- Security Policies
- URL Categories
- Network Interfaces
- Virtual Routers

### Files
- `main.tf` - Resource definitions
- `variables.tf` - Variable type definitions
- `terraform.tfvars.example` - Sample variable values (rename to terraform.tfvars)
- `outputs.tf` - Output definitions

## Core Concepts

### Location Attribute
Resources use a `location` attribute to specify configuration placement within Panorama:
- Template/Template Stack level
- Device Group level  
- Shared level

Example:
```hcl
location = {
  device_group = {
    name = "Branch-DG"
  }
}
```

### Order of Operations 
Resources must be created in correct order due to dependencies:
1. Templates 
2. Template Stacks
3. Device Groups
4. Objects & Rules

Dependencies are managed via `depends_on` blocks.

## Usage

1. Copy `terraform.tfvars.example` to `terraform.tfvars`
2. Update variables for your environment  
3. Initialize:
```bash
terraform init
```
4. Preview changes:
```bash
terraform plan
```
5. Apply configuration:
```bash 
terraform apply
```

## Limitations

- Provider is in alpha state
- No commit capability (must be done manually in Panorama)
- Some resource types still under development

## Contributing
Submit issues and pull requests to help improve configurations.
