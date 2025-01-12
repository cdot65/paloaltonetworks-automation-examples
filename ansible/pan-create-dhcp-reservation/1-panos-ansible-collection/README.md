# Palo Alto Networks Create DHCP Reservation (Ansible Collection) 📚

This README provides an overview of our Ansible project and guides you through the setup and execution process. 🚀

## Table of Contents

- [Palo Alto Networks Create DHCP Reservation (Ansible Collection) 📚](#palo-alto-networks-create-dhcp-reservation-ansible-collection-)
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

Our Ansible project aims to automate the DHCP reservation configurations within a Palo Alto Networks Panorama. By leveraging Ansible's powerful automation capabilities, we can streamline the process and ensure consistent and reproducible results across multiple environments. 🎯

This project provides two unique ways of accomplishing goals. You can build configuration directly with the Ansible modules (as shown in the example provided), or you can bypass the modules and use the API directly (which will be showcased in the next project).

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
# CREATE DHCP RESERVATIONS WITHIN PANORAMA
- hosts: panorama
  connection: local
  gather_facts: False
  become: False
  collections:
    - paloaltonetworks.panos
    - ansible.utils

  tasks:
    - name: DHCP reservations
      paloaltonetworks.panos.panos_config_element:
        provider:
          ip_address: "{{ ansible_host }}"
          api_key: "{{ panorama_api_key }}"
        xpath: "/config/devices/entry[@name='localhost.localdomain']/template/entry[@name='{{ item.template }}']/config/devices/entry[@name='localhost.localdomain']/network/dhcp/interface/entry[@name='{{ item.interface }}']/server/reserved"
        element: |
          "<entry name='{{ item.ip_address }}'>
            <mac>{{ item.mac }}</mac>
            <description>{{ item.description }}</description>
          </entry>"
      loop: "{{ dhcp_reservations }}"
```

The playbook consists of one or more tasks that target the Panorama host group. Variables such as API keys and DHCP reservations are defined separately in group variable files (`group_vars/auth.yaml` and `group_vars/dhcp.yaml`). Tasks are the core components of the playbook, representing the actions to be performed on the target Panorama device. 🎭

## Execution Workflow

To execute our Ansible playbook, follow these steps:

1. Ensure that you have activated the Python virtual environment.
2. Run the following command:

   ```bash
   ansible-playbook -i inventory.yaml playbook.yaml
   ```

   This command specifies the inventory file (`inventory.yaml`) and the playbook file (`playbook.yaml`) to be executed.

3. Ansible will connect to the Panorama host and execute the tasks defined in the playbook. 🚀

### Screenshots

Here are some screenshots showcasing the execution of our Ansible playbook:

![Screenshot 1](screenshots/screenshot1.png)
![Screenshot 2](screenshots/screenshot2.png)

Feel free to explore the playbook and customize it according to your specific requirements. Happy automating! 😄
