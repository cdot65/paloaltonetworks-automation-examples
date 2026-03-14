# Palo Alto Networks Create DHCP Reservation (builtin.uri module) 📚

This README provides an overview of our Ansible project and guides you through the setup and execution process. 🚀

## Table of Contents

- [Palo Alto Networks Create DHCP Reservation (builtin.uri module) 📚](#palo-alto-networks-create-dhcp-reservation-builtinuri-module-)
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

Our Ansible project aims to automate the DHCP reservation configurations within a Palo Alto Networks Panorama by directly interacting with the API using Ansible's `ansible.builtin.uri` module. This approach allows for a highly flexible and customizable interaction with the API. 🎯

This project provides an alternative way of accomplishing goals without relying on specific Ansible modules. Instead, we use the native `ansible.builtin.uri` module to send direct requests to the API.

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
#------------------------------------------------------------------------
# CREATE DHCP RESERVATIONS WITHIN PANORAMA
#------------------------------------------------------------------------
- hosts: panorama
  connection: local
  gather_facts: False
  become: False
  vars:
    interface: "ethernet1/2"
    template: "BaseTemplate"
  collections:
    - ansible.utils

  tasks:
    - name: Login to a form based webpage, then use the returned cookie to access the app in later tasks
      ansible.builtin.uri:
        url: https://panorama/api
        method: POST
        body_format: form-urlencoded
        body:
          - [key, "{{ panorama_api_key}}"]
          - [type, config]
          - [action, set]
          - [
              xpath,
              "/config/devices/entry[@name='localhost.localdomain']/template/entry[@name='{{ template }}']/config/devices/entry[@name='localhost.localdomain']/network/dhcp/interface/entry[@name='{{ interface }}']/server/reserved",
            ]
          - [
              element,
              "<entry name='{{ item.ip_address }}'><mac>{{ item.mac }}</mac><description>{{ item.description }}</description></entry>",
            ]
        status_code: 200
        validate_certs: no
      loop:
        - {
            ip_address: "192.168.101.20",
            mac: "00:50:56:11:20:44",
            description: "server20",
          }
        - {
            ip_address: "192.168.101.21",
            mac: "00:50:56:11:21:44",
            description: "server21",
          }
        - {
            ip_address: "192.168.101.22",
            mac: "00:50:56:11:22:44",
            description: "server22",
          }
        - {
            ip_address: "192.168.101.23",
            mac: "00:50:56:11:23:44",
            description: "server23",
          }
```

The playbook consists of tasks that target the Panorama host group. Instead of using specific Ansible modules, we use Ansible's `ansible.builtin.uri` module to send direct API requests. This method provides more flexibility and direct control over the API interactions. 🎭

## Execution Workflow

To execute our Ansible playbook, follow these steps:

1. Ensure that you have activated the Python virtual environment.
2. Run the following command:

   ```bash
   ansible-playbook -i inventory.yaml playbook.yaml
   ```

   This command specifies the inventory file (`inventory.yaml`) and the playbook file (`playbook.yaml`) to be executed.

3. Ansible will connect to the Panorama host and execute the tasks defined in the playbook by sending direct API requests. 🚀

### Screenshots

Here are some screenshots showcasing the execution of our Ansible playbook:

![Screenshot 1](screenshots/screenshot1.png)
![Screenshot 2](screenshots/screenshot2.png)

Feel free to explore the playbook and customize it according to your specific requirements. Happy automating! 😄
