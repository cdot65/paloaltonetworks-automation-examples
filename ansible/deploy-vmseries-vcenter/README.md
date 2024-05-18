# Ansible Project 📚

This README provides an overview of our Ansible project and guides you through the setup and execution process. 🚀

## Table of Contents

- [Ansible Project 📚](#ansible-project-)
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

Our Ansible project aims to automate the deployment of a VM series firewall using VMware. By leveraging Ansible's powerful automation capabilities along with the `community.vmware` and `paloaltonetworks.panos` collections, we can streamline the process and ensure consistent and reproducible results across VMware environments. 🎯

## Prerequisites

Before getting started, ensure that you have the following prerequisites installed on your local machine:

- Python (version 3.X.X) 🐍
- pip (Python package manager) 📦
- Ansible (version X.X.X)
- Ansible Collections:
  - `paloaltonetworks.panos`
  - `community.vmware`
- Additional Python Dependencies:
  - `xmltodict`
  - `pyvmomi`
  - `pan-os-python`
  - `requests`

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
ansible-galaxy collection install community.vmware

pip install xmltodict pyvmomi pan-os-python requests
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
>       ansible_python_interpreter: /path/to/venv/bin/python
> ```

## Playbook Structure

Our Ansible playbook (`playbook.yaml`) is structured as follows:

```yaml
---
# ---------------------------------------------------------------------------
# Deploy VM series firewall
# ---------------------------------------------------------------------------
- name: Deploy VM series firewall
  hosts: localhost
  connection: local
  gather_facts: False
  become: False
  collections:
    - paloaltonetworks.panos
  tasks:
    - name: Create VM series
      community.vmware.vmware_guest:
        # Define connection parameters
        hostname: "{{ vcenter_hostname }}"
        username: "{{ vcenter_username }}"
        password: "{{ vcenter_password }}"
        validate_certs: False

        # Define vCenter parameters
        datacenter: "{{ datacenter }}"
        state: present
        folder: "{{ folder }}"
        esxi_hostname: "{{ esxi_host }}"

        # Define VM specifics
        template: "{{ template }}"
        name: "{{ vm_name }}"
        wait_for_ip_address: True
      delegate_to: localhost
      register: vmseries_details

    - name: Print VM series details
      debug:
        var: vmseries_details
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
