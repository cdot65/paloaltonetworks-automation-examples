# Ansible Hello World Project 👋

This README provides an overview of our Ansible Hello World project and guides you through the setup and execution process. 🚀

## Table of Contents

- [Ansible Hello World Project 👋](#ansible-hello-world-project-)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Prerequisites](#prerequisites)
  - [Setup](#setup)
    - [Creating a Python Virtual Environment](#creating-a-python-virtual-environment)
    - [Installing Ansible](#installing-ansible)
  - [Inventory](#inventory)
  - [Playbook Structure](#playbook-structure)
  - [Execution Workflow](#execution-workflow)

## Overview

Our Ansible Hello World project aims to demonstrate the basic usage of Ansible by printing a simple "Hello World!" message. This project serves as a starting point for learning Ansible and understanding its fundamental concepts. 📚

## Prerequisites

Before getting started, ensure that you have the following prerequisites installed on your local machine:

- Python (version 3.11 or greater) 🐍
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

Our Ansible inventory file (`inventory.yaml`) defines the target hosts for our playbook. In this case, we are targeting `localhost` with a local connection. If needed, you can adjust the inventory to match your environment. 📝

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

Our Ansible playbook (`playbook.yaml`) is structured as follows:

```yaml
- name: Hello World Sample
  hosts: all
  become: false
  vars:
    message: "Hello World!"
  tasks:
    - name: Hello Message
      debug:
        msg: "{{ message }}"
      tags:
        - debug
  handlers:
    - name: Print done
      debug:
        msg: "Done"
      listen: "done"
```

The playbook consists of a single play targeting all hosts defined in the inventory. It sets a variable `message` with the value "Hello World!". The playbook includes a single task that prints the `message` variable using the `debug` module. Additionally, it defines a handler that prints "Done" when triggered. 🎭

## Execution Workflow

To execute our Ansible playbook, follow these steps:

1. Ensure that you have activated the Python virtual environment.
2. Run the following command:

   ```bash
   ansible-playbook playbook.yaml
   ```

   This command executes the playbook file (`playbook.yaml`) using the default inventory file specified in the `ansible.cfg` configuration file.

3. Ansible will connect to the target hosts (in this case, `localhost`) and execute the tasks defined in the playbook. 🚀

Feel free to explore the playbook and customize it according to your specific requirements. Happy automating! 😄
