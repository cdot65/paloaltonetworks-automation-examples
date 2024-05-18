# Palo Alto Networks Create XML Configuration and Load 📚

This README provides an overview of our Ansible project and guides you through the setup and execution process. 🚀

## Table of Contents

- [Palo Alto Networks Create XML Configuration and Load 📚](#palo-alto-networks-create-xml-configuration-and-load-)
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

## Overview

Our Ansible project aims to automate the generation and loading of a full XML configuration for a Palo Alto Networks firewall using Jinja2 templates. By leveraging Ansible's powerful automation capabilities, we can streamline the process and ensure consistent and reproducible results across multiple environments. 🎯

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

Here is a snippet of the inventory file:

```yaml
all:
  children:
    firewalls:
      hosts:
        dal-vfw-01:
```

> **Note:** When using a Python virtual environment, make sure to specify the Python interpreter path in the inventory file if needed.

## Playbook Structure

Our Ansible playbook (`playbook.yaml`) is structured as follows:

```yaml
---
#------------------------------------------------------------------------
# Build a full XML configuration with Jinja2, push to firewall, and load.
#------------------------------------------------------------------------
- hosts: all
  connection: local
  any_errors_fatal: "{{ any_errors_fatal | default(true) }}"
  gather_facts: False
  tasks:
    # create local directories to hold configuration files.
    - ansible.builtin.import_role:
        name: directories

    # use Jinja2 to template out a firewall configuration, piece by piece.
    - ansible.builtin.import_role:
        name: build_config

    # assemble a full configuration from the parts created in previous step.
    - ansible.builtin.import_role:
        name: assemble

    # upload our full configuration to the firewall through the REST API.
    - name: Upload our generated configuration file
      ansible.builtin.shell: |
        curl 'https://{{ ansible_host }}/api/?type=import&category=configuration' \
        --header 'X-PAN-KEY: {{ api_token }}' \
        --form 'file=@"{{ completed_config_file }}"' -k

    # load our generated configuration into the candidate configuration.
    - name: Load our generated configuration into the candidate configuration
      ansible.builtin.shell: |
        curl 'https://{{ ansible_host }}/api/?type=op&cmd=<load><config><from>{{ ansible_host }}_ansible.xml</from></config></load>' \
        --header 'X-PAN-KEY: {{ api_token }}' -k
```

The playbook imports tasks from the roles directory and applies them sequentially:

1. The `directories` role creates local directories to hold configuration files.
2. The `build_config` role uses Jinja2 templates to generate the firewall configuration, piece by piece.
3. The `assemble` role assembles a full configuration from the parts created in the previous step.
4. The playbook uploads the full configuration to the firewall through the REST API.
5. The playbook loads the generated configuration into the candidate configuration on the firewall.

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
