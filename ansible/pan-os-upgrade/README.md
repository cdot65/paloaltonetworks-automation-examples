# PAN-OS Upgrade 📚

This README provides an overview of our Ansible project and guides you through the setup and execution process. 🚀

## Table of Contents

- [PAN-OS Upgrade 📚](#pan-os-upgrade-)
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

Our Ansible project aims to automate the configuration and deployment of upgrading a firewall when connected to Panorama. By leveraging Ansible's powerful automation capabilities, we can streamline the process and ensure consistent and reproducible results across multiple environments. 🎯

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
        panorama:
          ansible_host: 192.168.255.210
```

> **Note:** When using a Python virtual environment, make sure to specify the Python interpreter path in the inventory file:
>
> ```yaml
> all:
>   hosts:
>     localhost:
>       ansible_connection: local
>       ansible_python_interpreter: your_virtualenvironment/path/to/bin/python
> ```

## Playbook Structure

Our Ansible playbook (`playbook.yml`) is structured as follows:

```yaml
- name: Upgrade a firewall
  hosts: panorama
  connection: local
  gather_facts: false
  become: false

  vars:
    serial_number: "007054012345670"
    software_version: "11.0.2-h1"

  tasks:
    - name: Install Software
      paloaltonetworks.panos.panos_software:
        provider:
          ip_address: "{{ ansible_host }}"
          username: "{{ panorama_credentials.username }}"
          password: "{{ panorama_credentials.password }}"
          serial_number: "{{ serial_number }}"
        version: "{{ software_version }}"
        download: true
        install: true
        restart: true
```

The playbook consists of one or more plays, each targeting specific hosts or groups. Variables can be defined at the playbook level or within individual plays. Tasks are the core components of the playbook, representing the actions to be performed on the target hosts. 🎭

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
