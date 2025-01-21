# PAN-OS Firewall Configuration Automation 📚

This README provides an overview of our Ansible project for configuring and managing PAN-OS firewalls. 🚀

## Table of Contents

- [PAN-OS Firewall Configuration Automation 📚](#pan-os-firewall-configuration-automation-)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Prerequisites](#prerequisites)
  - [Project Structure](#project-structure)
  - [Setup](#setup)
    - [Creating a Python Virtual Environment](#creating-a-python-virtual-environment)
    - [Installing Ansible](#installing-ansible)
  - [Playbook Structure](#playbook-structure)
  - [Inventory](#inventory)
  - [Roles](#roles)
  - [Group Variables](#group-variables)
  - [Execution Workflow](#execution-workflow)
  - [Working with Ansible Vault](#working-with-ansible-vault)

## Overview

Our Ansible project aims to automate the configuration of PAN-OS firewalls, specifically focusing on overriding and disabling the captive portal. This project uses a combination of CLI commands and API calls to achieve the desired configuration. 🎯

## Prerequisites

Before getting started, ensure that you have the following prerequisites:

- Python (version 3.6+) 🐍
- pip (Python package manager) 📦
- Access to a PAN-OS firewall
- SSH access and API key for the PAN-OS firewall

## Project Structure

```
.
├── playbook.yaml
├── inventory.yaml
├── roles
│   └── panos_config
│       └── tasks
│           ├── configure_captive_portal.yaml
│           └── disable_captive_portal.yaml
└── group_vars
    └── all
        ├── settings.yaml
        ├── secrets.yaml
        └── python.yaml
```

## Setup

### Creating a Python Virtual Environment

To create a Python virtual environment, follow these steps:

1. Open a terminal and navigate to the project directory.
2. Run the following command to create a virtual environment:

   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - For Windows:

     ```bash
     venv\Scripts\activate
     ```

   - For macOS and Linux:

     ```bash
     source venv/bin/activate
     ```

### Installing Ansible

With the virtual environment activated, install Ansible using pip:

```bash
pip install ansible
```

## Playbook Structure

Our main Ansible playbook (`playbook.yaml`) is structured to override and disable the captive portal on PAN-OS firewalls. It includes two main tasks:

1. Override Captive Portal
2. Disable Captive Portal

Each task is implemented as a separate role, allowing for modular and reusable code.

## Inventory

The `inventory.yaml` file defines the target PAN-OS firewall:

```yaml
all:
  children:
    panos_firewall:
      hosts:
        firewall.example.io:
```

## Roles

The project uses a `panos_config` role with two main tasks:

1. `configure_captive_portal.yaml`: Uses CLI commands to override the captive portal.
2. `disable_captive_portal.yaml`: Uses API calls to disable the captive portal.

## Group Variables

Group variables are stored in the `group_vars/all/` directory:

- `settings.yaml`: Contains connection and authentication settings.
- `secrets.yaml`: Stores sensitive information like usernames, passwords, and API keys.
- `python.yaml`: Specifies the Python interpreter to use.

## Execution Workflow

To execute our Ansible playbook, follow these steps:

1. Ensure that you have activated the Python virtual environment.
2. Update the `group_vars/all/secrets.yaml` file with your actual credentials and API key.
3. Run the following command:

   ```bash
   ansible-playbook -i inventory.yaml playbook.yaml
   ```

4. Ansible will connect to the PAN-OS firewall and execute the tasks to override and disable the captive portal. 🚀

## Working with Ansible Vault

For enhanced security, it's recommended to use Ansible Vault to encrypt sensitive information in the `group_vars/all/secrets.yaml` file:

1. Encrypt the secrets file:

   ```bash
   ansible-vault encrypt group_vars/all/secrets.yaml
   ```

2. When running the playbook, use the `--ask-vault-pass` flag:

   ```bash
   ansible-playbook -i inventory.yaml playbook.yaml --ask-vault-pass
   ```

This approach ensures that sensitive data like passwords and API keys are not stored in plain text. 🔒

Feel free to explore the playbook and customize it according to your specific requirements. Happy automating! 😄