# Netbox Execution Environment 📚

This README provides an overview of our container image project and guides you through the setup and execution process. 🚀

## Table of Contents

- [Netbox Execution Environment 📚](#netbox-execution-environment-)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Prerequisites](#prerequisites)
  - [Setup](#setup)
    - [Installing Podman](#installing-podman)
    - [Installing Ansible-Builder](#installing-ansible-builder)
      - [Creating a Python Virtual Environment](#creating-a-python-virtual-environment)
      - [Installing Ansible Builder](#installing-ansible-builder-1)
  - [Container Image File Structure](#container-image-file-structure)
    - [Galaxy Requirements](#galaxy-requirements)
  - [Execution Workflow](#execution-workflow)
    - [Using the CLI](#using-the-cli)
  - [Screenshots](#screenshots)

## Overview

Our container image project aims to automate the creation of an Execution Environment for interacting with Netbox. By leveraging the powerful CLI commands from Podman, we can streamline the process and ensure consistent and reproducible results across multiple environments. 🎯

If you would like further assistance throughout the build process, we have also included a `tasks.py` file that provides additional CLI shortcuts. This is optional and requires a Python environment, but many find that this makes their lives significantly easier than memorizing long and (sometimes) complex CLI commands.

## Prerequisites

Before getting started, ensure that you have the following prerequisites installed on your local machine:

- Podman installed

## Setup

### Installing Podman

- Installing Podman on [Linux, macOS, or Windows](https://podman-desktop.io/downloads)

### Installing Ansible-Builder

#### Creating a Python Virtual Environment

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

#### Installing Ansible Builder

With the virtual environment activated, install Ansible Builder using pip:

```bash
pip install ansible-builder
```

## Container Image File Structure

Our container image (`Dockerfile`) is dynamically built based on the contents within the `execution-environment.yml` file:

```yaml
---
version: 3

images:
  base_image:
    name: quay.io/fedora/fedora:latest

dependencies:
  ansible_core:
    package_pip: ansible-core
  ansible_runner:
    package_pip: ansible-runner
  system:
    - openssh-clients
    - sshpass
  python:
    - pytz
    - pynetbox
  galaxy: requirements.yml
```

### Galaxy Requirements

```yaml
---
collections:
  - name: netbox.netbox
    type: galaxy
    version: 3.18.0
```

## Execution Workflow

To execute our container image build, follow these steps:

### Using the CLI

1. Navigate to the project directory.
2. Run the following command to build the container image with a tag:

   ```bash
   ansible-builder build --tag ghcr.io/cdot65/execution-environment-netbox:latest
   ```

## Screenshots

Here are some screenshots showcasing the execution:

![Screenshot 1](screenshots/screenshot1.png)
![Screenshot 2](screenshots/screenshot2.png)

Feel free to explore the execution environment and customize it according to your specific requirements. Happy automating! 😄
