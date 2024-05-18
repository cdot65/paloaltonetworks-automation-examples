# Palo Alto Networks Get Exported Rules as CSV 📚

This README provides an overview of our Ansible project and guides you through the setup and execution process. 🚀

## Table of Contents

- [Palo Alto Networks Get Exported Rules as CSV 📚](#palo-alto-networks-get-exported-rules-as-csv-)
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

Our Ansible project aims to automate the retrieval of security pre-rule base and post-rule base configurations from a Panorama instance. By leveraging Ansible's powerful automation capabilities, we can streamline the process and ensure consistent and reproducible results across multiple environments. 🎯

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

> **Note:** When using a Python virtual environment, make sure to specify the Python interpreter path in the inventory file:
>
> ```yaml
> all:
>   vars:
>     ansible_python_interpreter: "{{ ansible_playbook_python }}"
> ```

## Playbook Structure

Our Ansible playbook (`playbook.yaml`) is structured as follows:

```yaml
---
- name: Retrieve Panorama configuration
  hosts: panorama
  connection: local
  gather_facts: false
  collections:
    - paloaltonetworks.panos
    - community.general

  tasks:
    - name: Retrieve security pre-rule base
      panos_security_rule_facts:
        provider:
          ip_address: "{{ ansible_host }}"
          api_key: "{{ panorama_api_key }}"
        rulebase: "pre-rulebase"
        details: True
      register: pre_rule_base

    - name: Retrieve security post-rule base
      panos_security_rule_facts:
        provider:
          ip_address: "{{ ansible_host }}"
          api_key: "{{ panorama_api_key }}"
        rulebase: "post-rulebase"
        details: True
      register: post_rule_base

    - name: Parse data and write to CSV file with Jinja2
      template:
        src: "./templates/security_profile_group.j2"
        dest: "./test.csv"
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
