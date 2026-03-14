# Getting Started

This repository is a collection of self-contained automation examples. Each project has its own dependencies, configuration, and README with step-by-step instructions.

## Quick Start

1. **Clone the repository:**

    ```bash
    git clone https://github.com/cdot65/paloaltonetworks-automation-examples.git
    cd paloaltonetworks-automation-examples
    ```

2. **Pick a project** by browsing the technology sections ([Ansible](../ansible/overview.md), [Python](../python/overview.md), [Terraform](../terraform/overview.md), [Go](../go/overview.md), [Jenkins](../jenkins/overview.md)).

3. **Navigate to the project directory** and follow its README.

## Common Prerequisites

Most projects require one or more of the following:

| Requirement | Used By |
|-------------|---------|
| Python 3.11+ | Python projects, Ansible |
| Go 1.18+ | Go CLI tools |
| Terraform >= 1.5 | Terraform modules |
| Docker | Ansible EEs, Jenkins agents |
| PAN-OS firewall or Panorama | Most projects |
| API key or admin credentials | All device-targeting projects |

## Configuration Pattern

Every project that connects to a device or API follows the same pattern:

1. Copy the example config file (`.env.example`, `terraform.tfvars.example`, `group_vars/` templates)
2. Fill in your credentials and device details
3. Run the tool

!!! warning "Credentials"
    Never commit real credentials. All `.env`, `terraform.tfvars`, and `.secrets.yaml` files are excluded by the root `.gitignore`.
