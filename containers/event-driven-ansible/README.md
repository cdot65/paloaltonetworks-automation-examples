# Event-Driven Ansible Project 📚

This README provides an overview of our Event-Driven Ansible project and guides you through the setup, container build, execution process, and the configuration of log forwarding from Palo Alto Networks. 🚀

## Table of Contents

- [Event-Driven Ansible Project 📚](#event-driven-ansible-project-)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Prerequisites](#prerequisites)
  - [Setup](#setup)
    - [Installing a Container Runtime Engine](#installing-a-container-runtime-engine)
    - [Installing Invoke \[Optional\]](#installing-invoke-optional)
      - [Creating a Python Virtual Environment](#creating-a-python-virtual-environment)
      - [Installing Invoke](#installing-invoke)
  - [Container Image File Structure](#container-image-file-structure)
  - [Execution Workflow](#execution-workflow)
    - [Using the CLI](#using-the-cli)
    - [Using Invoke](#using-invoke)
    - [Screenshots](#screenshots)

## Overview

Our container image project aims to automate the configuration and deployment of Event-Driven Ansible using a rulebook that reacts to specific conditions and executes playbooks accordingly. By leveraging the powerful CLI commands from either Docker or Podman, we can ensure consistent and reproducible results across multiple environments. 🎯

If you would like further assistance throughout the build process, we have also included a `tasks.py` file that provides additional CLI shortcuts. This is optional and requires a Python environment, but many find that this makes their lives significantly easier than memorizing long and (sometimes) complex CLI commands.

## Prerequisites

Before getting started, ensure that you have the following prerequisites installed on your local machine:

- Docker or Podman installed
- [Optional: for using Invoke] Python (version 3.11+) 🐍
- [Optional: for using Invoke] pip (Python package manager) 📦

## Setup

### Installing a Container Runtime Engine

- Installing Docker on [Linux](https://docs.docker.com/desktop/install/linux-install/), [macOS](https://docs.docker.com/desktop/install/mac-install/), or [Windows](https://docs.docker.com/desktop/install/windows-install/)
- Installing Podman on [Linux, macOS, or Windows](https://podman-desktop.io/downloads)

### Installing Invoke [Optional]

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

#### Installing Invoke

With the virtual environment activated, install Invoke using pip:

```bash
pip install invoke
```

## Container Image File Structure

Our container image (`Dockerfile`) is structured as follows:

```Dockerfile
# Use Fedora Base Image
FROM fedora:latest

# Update package index and install OpenJDK, Python, Pip, GCC, and Python development headers
RUN dnf update -y
RUN dnf install -y java-17-openjdk python3.12 python3-pip maven gcc python3.12-devel
RUN dnf groupinstall -y "Development Tools"
RUN dnf install -y redhat-rpm-config libffi-devel openssl-devel
RUN dnf clean all

# Set JAVA_HOME environment variable
ENV JAVA_HOME=/usr/lib/jvm/jre-17-openjdk

# Install Ansible, ansible-rulebook (with no binary jpy), and ansible-runner
RUN pip3 install ansible ansible-runner aiohttp==3.9.0b0
RUN pip3 install ansible-rulebook --no-binary jpy

# Install any dependencies and Ansible Collection
RUN pip3 install pan-os-python xmltodict
RUN ansible-galaxy collection install paloaltonetworks.panos

# Set working directory
WORKDIR /ansible/eda
```

This Dockerfile is structured to update the base Fedora image, install necessary development tools, set environment variables, and finally, install the necessary Ansible components and Python packages. Sequentially, it ensures that we have a standardized environment for deploying Event-Driven Ansible.

## Execution Workflow

### Using the CLI

1. Build the container image:

   ```bash
   docker build -t event-driven-ansible-node:0.0.1 .
   ```

2. Run the container:

   ```bash
   docker run --rm -d -p 5000:5000 --name ansible-eda \
     -v $(pwd)/collections:/usr/share/ansible/collections \
     -v $(pwd)/roles:/usr/share/ansible/roles \
     -v $(pwd)/plugins:/usr/share/ansible/plugins \
     -v $(pwd):/ansible/eda \
     event-driven-ansible-node:0.0.1 \
     ansible-rulebook --rulebook=rulebooks/rulebook.yaml \
     -i inventory/inventory.yaml --verbose
   ```

3. Tail the logs:

   ```bash
   docker logs -f ansible-eda
   ```

4. Stop the container:

   ```bash
   docker stop ansible-eda
   ```

### Using Invoke

1. **Ensure the `invoke` library is installed**:

   ```bash
   pip install invoke
   ```

2. **Build the container image**:

   ```bash
   inv build
   ```

3. **Run the container**:

   ```bash
   inv up
   ```

4. **Monitor the logs**:

   ```bash
   inv logs
   ```

5. **Stop and remove the container**:

   ```bash
   inv down
   ```

### Screenshots

Here are some screenshots showcasing the execution of our Ansible project:

![Screenshot 1](screenshots/screenshot1.png)
![Screenshot 2](screenshots/screenshot2.png)

Feel free to explore the playbook and customize it according to your specific requirements. Happy automating! 😄
