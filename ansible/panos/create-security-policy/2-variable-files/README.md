# Palo Alto Networks Create Security Policy (variable files) 📚

This README provides an overview of our Ansible project and guides you through the setup and execution process. 🚀

## Table of Contents

- [Palo Alto Networks Create Security Policy (variable files) 📚](#palo-alto-networks-create-security-policy-variable-files-)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Prerequisites](#prerequisites)
  - [Setup](#setup)
    - [Creating a Python Virtual Environment](#creating-a-python-virtual-environment)
    - [Installing Ansible](#installing-ansible)
  - [Inventory](#inventory)
  - [Playbook Structure](#playbook-structure)
    - [Variables in `host_vars/panorama.yaml`](#variables-in-host_varspanoramayaml)
    - [Variables in `group_vars/panorama.yaml`](#variables-in-group_varspanoramayaml)
  - [Execution Workflow](#execution-workflow)
    - [Screenshots](#screenshots)

## Overview

Our Ansible project aims to automate the configuration and deployment of security policies on a Palo Alto Networks Panorama firewall. By leveraging Ansible's powerful automation capabilities, we can streamline the process and ensure consistent and reproducible results across multiple environments. 🎯

This project is an iteration on the previous and focuses on breaking up some of the variables into separate `host_vars` and `group_vars` directories. These files are discovered at runtime and automatically populate their variables into the playbook's execution upon a match from the inventory file.

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
> ```ini
> [defaults]
> interpreter_python = /path/to/venv/bin/python
> ```

Example `inventory.yaml`:

```yaml
all:
  children:
    panorama:
      hosts:
        panorama:
```

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

The playbook specifies tasks to be performed on the `panorama` group defined in the inventory. Variables used within the playbook are defined in separate `host_vars` and `group_vars` directories.

### Variables in `host_vars/panorama.yaml`

```yaml
# Variables related to the security rule
security_rule:
  rule_name: "Permit DMZ to WAN"
  description: "Allow Kubernetes hosts outbound access to the WAN"
  source_zone:
    - "DMZ"
  destination_zone:
    - "WAN"
  source_ip:
    - "any"
  source_user:
    - "any"
  destination_ip:
    - "any"
  category:
    - "any"
  application:
    - "any"
  service:
    - "application-default"
  hip_profiles:
    - "any"
  action: "allow"
  device_group: "shared"
```

### Variables in `group_vars/panorama.yaml`

```yaml
# group_vars/panorama.yaml

# Variables related to all Panorama API connections
panorama_credentials:
  username: "this-is-just-a-placeholder"
  password: "this-is-just-a-placeholder"
```

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
