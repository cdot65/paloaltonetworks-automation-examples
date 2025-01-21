# TLS Decryption Remediation 📚

This README provides an overview of our Ansible project and guides you through the setup and execution process. 🚀

## Table of Contents

- [TLS Decryption Remediation 📚](#tls-decryption-remediation-)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Prerequisites](#prerequisites)
  - [Setup](#setup)
    - [Creating a Python Virtual Environment](#creating-a-python-virtual-environment)
    - [Installing Ansible](#installing-ansible)
    - [Installing Required Collections and Dependencies](#installing-required-collections-and-dependencies)
  - [Inventory](#inventory)
  - [Playbook Structure](#playbook-structure)
  - [Execution Workflow](#execution-workflow)
    - [Screenshots](#screenshots)

## Overview

Our Ansible project aims to automate the configuration and deployment of firewall certificates across different environments using `paloaltonetworks.panos`, `community.general`, and other Ansible capabilities. By leveraging Ansible's power, we ensure a streamlined and consistent process for managing certificates on RedHat and Windows machines. 🎯

## Prerequisites

Before getting started, ensure that you have the following prerequisites installed on your local machine:

- Python (version 3.11) 🐍
- pip (Python package manager) 📦
- Ansible (version 2.10.0 or higher)

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

### Installing Required Collections and Dependencies

Install the necessary Ansible collections and additional Python dependencies:

```bash
ansible-galaxy collection install paloaltonetworks.panos
ansible-galaxy collection install community.general
```

## Inventory

Our Ansible inventory file (`inventory.yaml`) defines the target hosts and groups for our playbook. If needed, you can adjust the inventory to match your environment. 📝

> **Note:** When using a Python virtual environment, make sure to specify the Python interpreter path in the inventory file:
>
> ```yaml
> all:
>   hosts:
>     localhost:
>       ansible_connection: local
>       # ansible_python_interpreter: /path/to/venv/bin/python
> ```

## Playbook Structure

Our Ansible playbook (`playbook.yaml`) is structured as follows:

```yaml
---
- name: Pull Firewall Certificate
  hosts: localhost
  gather_facts: false
  tasks:
    - name: Export Certificate from PAN-OS
      import_role:
        name: panos

- name: Push Certificate to Server
  hosts: all
  gather_facts: true
  tasks:
    - name: Push for RHEL workstations
      block:
        - name: RHEL desktops
          import_role:
            name: rhel
          when: ansible_facts['os_family'] == 'RedHat'

        - name: Windows desktops
          import_role:
            name: windows
          when: ansible_facts['os_family'] == 'Windows'

      rescue:
        - name: Handle task errors
          debug:
            msg: "An error occurred while executing the block."

      when: inventory_hostname == target_server
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

Feel free to explore the playbook and customize it according to your specific requirements. Happy automating! 😄
