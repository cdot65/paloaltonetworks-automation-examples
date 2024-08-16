# Palo Alto Networks Create Security Policy (ansible vault) 📚

This README provides an overview of our Ansible project and guides you through the setup and execution process. 🚀

## Table of Contents

- [Palo Alto Networks Create Security Policy (ansible vault) 📚](#palo-alto-networks-create-security-policy-ansible-vault-)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Prerequisites](#prerequisites)
  - [Setup](#setup)
    - [Creating a Python Virtual Environment](#creating-a-python-virtual-environment)
    - [Installing Ansible](#installing-ansible)
  - [Inventory](#inventory)
  - [Playbook Structure](#playbook-structure)
  - [Execution Workflow](#execution-workflow)
    - [Screenshots](#screenshots)
  - [Working with Ansible Vault](#working-with-ansible-vault)

## Overview

Our Ansible project aims to automate the configuration and deployment of security policies on a Palo Alto Networks Panorama. By leveraging Ansible's powerful automation capabilities, we can streamline the process and ensure consistent and reproducible results across multiple environments. 🎯

## Prerequisites

Before getting started, ensure that you have the following prerequisites installed on your local machine:

- Python (version 3.11+) 🐍
- pip (Python package manager) 📦

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

## Inventory

Our Ansible inventory file (`inventory.yaml`) defines the target hosts and groups for our playbook. If needed, you can adjust the inventory to match your environment. 📝

> **Note:** When using a Python virtual environment, make sure to specify the Python interpreter path in the `ansible.cfg` file (if different from the default):
>
> ```ini
> [defaults]
> interpreter_python = /path/to/venv/bin/python
> ```

## Playbook Structure

Our Ansible playbook (`playbook.yaml`) is structured as follows:

```yaml
- name: Create Security Policy
  hosts: panorama
  connection: local
  gather_facts: false
  become: false
  tasks:
    - name: Add test pre-rule to Panorama
      paloaltonetworks.panos.panos_security_rule:
        provider:
          ip_address: "{{ ansible_host }}"
          username: "{{ panorama_credentials.username }}"
          password: "{{ panorama_credentials.password }}"
        rule_name: "{{ security_rule.rule_name }}"
        description: "{{ security_rule.description }}"
        source_zone: "{{ security_rule.source_zone }}"
        destination_zone: "{{ security_rule.destination_zone }}"
        source_ip: "{{ security_rule.source_ip }}"
        source_user: "{{ security_rule.source_user }}"
        destination_ip: "{{ security_rule.destination_ip }}"
        category: "{{ security_rule.category }}"
        application: "{{ security_rule.application }}"
        service: "{{ security_rule.service }}"
        hip_profiles: "{{ security_rule.hip_profiles }}"
        action: "{{ security_rule.action }}"
        device_group: "{{ security_rule.device_group }}"
      register: results

    - name: Print results to console
      ansible.builtin.debug:
        msg: "{{ results }}"
```

The playbook consists of one or more plays, each targeting specific hosts or groups. Variables can be defined at the playbook level or within individual plays. Tasks are the core components of the playbook, representing the actions to be performed on the target hosts. 🎭

## Execution Workflow

To execute our Ansible playbook, follow these steps:

1. Ensure that you have activated the Python virtual environment.
2. Run the following command:

   ```bash
   ansible-playbook -i inventory.yaml playbook.yaml
   ```

   This command specifies the inventory file (`inventory.yaml`) and the playbook file (`playbook.yaml`) to be executed.

3. Ansible will connect to the target hosts and execute the tasks defined in the playbook. 🚀

### Screenshots

Here are some screenshots showcasing the execution of our Ansible playbook:

![Screenshot 1](screenshots/screenshot1.png)
![Screenshot 2](screenshots/screenshot2.png)

## Working with Ansible Vault

It's important to secure sensitive information such as API keys and usernames. This project uses Ansible Vault to encrypt the `group_vars/vault.yaml` file, which contains the Panorama username and API token.

```bash
ansible-vault encrypt group_vars/panorama.yaml
```

You'll be prompted to enter a password. Make sure to remember this password, as you'll need it to decrypt the file or edit its contents. To edit the encrypted file, use:

```bash
ansible-vault edit group_vars/panorama.yaml
```

To decrypt the file, use:

```bash
ansible-vault decrypt group_vars/panorama.yaml
```

When running the playbook, you'll need to provide the vault password using the `--ask-vault-pass` flag:

```bash
ansible-playbook playbook.yaml --ask-vault-pass
```

This project is an iteration on the previous and focuses on using Ansible Vault to protect our variable files with sensitive data. The `group_vars/panorama.yaml` file is encrypted with the ansible-vault command, while `host_vars` is not. Ansible Vault will require a password at runtime to decrypt or point to a file where the password is stored. If the vault password is not provided, the execution will be unable to read the encrypted variables file and will fail.

Feel free to explore the playbook and customize it according to your specific requirements. Happy automating! 😄
