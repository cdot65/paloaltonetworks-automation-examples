# Palo Alto Networks Address Object 📚

This README provides an overview of our Ansible project and guides you through the setup and execution process. 🚀

## Table of Contents

- [Palo Alto Networks Address Object 📚](#palo-alto-networks-address-object-)
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

Our Ansible project aims to automate the configuration and deployment of a simple example of what it looks like to provision something simple: an address object on a Panorama appliance. By leveraging Ansible's powerful automation capabilities, we can streamline the process and ensure consistent and reproducible results across multiple environments. 🎯 This is a good starter playbook to pull apart and try to understand what's happening.

## Prerequisites

Before getting started, ensure that you have the following prerequisites installed on your local machine:

- Python (recommended version 3.11+) 🐍
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

```yaml
all:
  children:
    panorama:
      hosts:
        panorama.example.com:
```

## Playbook Structure

Our Ansible playbook (`playbook.yaml`) is structured as follows:

```yaml
---
#------------------------------------------------------------------------
# CHECK TO SEE IF PANORAMA WOULD ALLOW ME TO CREATE A SECURITY OBJECT
#------------------------------------------------------------------------
- hosts: panorama
  connection: local
  gather_facts: False
  become: False
  collections:
    - paloaltonetworks.panos
    - ansible.utils

  tasks:
    - name: "Validate that Panorama would allow us to create an object, check mode"
      panos_address_object:
        provider:
          ip_address: "{{ ansible_host }}"
          api_key: "{{ panorama_api_key }}"
        name: "Gaming-PC"
        address_type: "fqdn"
        value: "gaming.example.com"
        description: "Gaming PC"
      check_mode: yes
      register: result

    - name: "Print result to the console"
      debug:
        msg: "{{ result }}"
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
