# Palo Alto Networks Get Interfaces 📚

This README provides an overview of our Ansible project and guides you through the setup and execution process. 🚀

## Table of Contents

- [Palo Alto Networks Get Interfaces 📚](#palo-alto-networks-get-interfaces-)
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

Our Ansible project aims to automate the retrieval of interface information from firewalls running PAN-OS. By leveraging Ansible's powerful automation capabilities and the Palo Alto Networks collection, we can streamline the process and ensure consistent and reproducible results across multiple environments. 🎯

## Prerequisites

Before getting started, ensure that you have the following prerequisites installed on your local machine:

- Python (version 3.11 or higher) 🐍
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

> **Note:** When using a Python virtual environment, make sure to specify the Python interpreter path in the `ansible.cfg` file. 

## Playbook Structure

Our Ansible playbook (`playbook.yml`) is structured as follows:

```yaml
---
- hosts: firewalls
  connection: local
  gather_facts: False
  become: False
  collections:
    - paloaltonetworks.panos
    - ansible.utils

  tasks:
    - name: "Run commmand 'show interfaces' on firewalls running PAN-OS."
      paloaltonetworks.panos.panos_op:
        provider:
          ip_address: "{{ ansible_host }}"
          username: "{{ panos_username }}"
          password: "{{ panos_password }}"
        cmd: "show interface all"
      register: result

    - name: "Convert to Python dictionary with xmltodict"
      set_fact:
        interfaces: "{{ result['stdout_xml'] | ansible.utils.from_xml('xmltodict') }}"

    - name: "Print interface output to the console"
      debug:
        msg: "{{ interfaces['response']['result']['hw']['entry'] }}"
```

The playbook consists of one play targeting the `firewalls` group. It includes tasks for running the 'show interfaces' command on the firewalls, converting the XML output to a Python dictionary, and printing the interface information to the console. 🎭

## Execution Workflow

To execute our Ansible playbook, follow these steps:

1. Ensure that you have activated the Python virtual environment.
2. Run the following command:

   ```bash
   ansible-playbook -i inventory.yaml playbook.yml
   ```

   This command specifies the inventory file (`inventory.yaml`) and the playbook file (`playbook.yml`) to be executed.

3. Ansible will connect to the target hosts and execute the tasks defined in the playbook. 🚀

### Screenshots

Here are some screenshots showcasing the execution of our Ansible playbook:

![Screenshot 1](screenshots/screenshot1.png)
![Screenshot 2](screenshots/screenshot2.png)

Feel free to explore the playbook and customize it according to your specific requirements. Happy automating! 😄
