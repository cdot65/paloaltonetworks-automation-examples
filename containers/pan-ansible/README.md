# PAN-OS and Panorama Ansible Container Image Project 📚

This README provides an overview of our container image project and guides you through the setup and execution process. 🚀

## Table of Contents

- [PAN-OS and Panorama Ansible Container Image Project 📚](#pan-os-and-panorama-ansible-container-image-project-)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Prerequisites](#prerequisites)
  - [Setup](#setup)
    - [Installing a Container Runtime Engine](#installing-a-container-runtime-engine)
    - [Installing Invoke \[optional\]](#installing-invoke-optional)
      - [Creating a Python Virtual Environment](#creating-a-python-virtual-environment)
      - [Installing Invoke](#installing-invoke)
  - [Container Image File Structure](#container-image-file-structure)
  - [Execution Workflow](#execution-workflow)
    - [Using the CLI](#using-the-cli)
    - [Using Invoke](#using-invoke)
    - [Screenshots](#screenshots)

## Overview

Our container image project aims to automate the creation of a Docker container for PAN-OS and Panorama Ansible projects. By leveraging the powerful CLI commands from either Docker or Podman, we can streamline the process and ensure consistent and reproducible results across multiple environments. 🎯

If you would like further assistance throughout the build process, we have also included a `tasks.py` file that provides additional CLI shortcuts. This is optional and requires a Python environment, but many find that this makes their lives significantly easier than memorizing long and (sometimes) complex CLI commands.

## Prerequisites

Before getting started, ensure that you have the following prerequisites installed on your local machine:

- Docker or Podman installed
- [optional: for using Invoke] Python (version 3.11+) 🐍
- [optional: for using Invoke] pip (Python package manager) 📦

## Setup

### Installing a Container Runtime Engine

- Installing Docker on [Linux](https://docs.docker.com/desktop/install/linux-install/), [macOS](https://docs.docker.com/desktop/install/mac-install/), or [Windows](https://docs.docker.com/desktop/install/windows-install/)
- Installing Podman on [Linux, macOS, or Windows](https://podman-desktop.io/downloads)

### Installing Invoke [optional]

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
FROM python:3.11-slim

LABEL name="ghcr.io/cdot65/pan-ansible:latest" \
    maintainer="cremsburg.dev@gmail.com" \
    description="Docker container for PAN-OS and Panorama" \
    license="Apache 2.0" \
    url="https://github.com/cdot65/pan-ansible" \
    build-date="20230406"

RUN apt-get update
RUN apt-get install -y --no-install-recommends \
    sudo \
    git \
    curl \
    vim \
    less \
    zsh
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/*

RUN useradd -m ansible
RUN echo "ansible ALL=(ALL) NOPASSWD: ALL" >>/etc/sudoers

USER ansible

RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
SHELL ["/bin/zsh", "-c"]

RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /home/ansible
COPY pyproject.toml pyproject.toml

ENV POETRY_VIRTUALENVS_PATH="/home/ansible/venv"
ENV ANSIBLE_CONFIG /home/ansible/ansible.cfg

RUN echo 'export PATH="/home/ansible/.local/bin:$PATH"' >>~/.zshrc
RUN source ~/.zshrc
RUN /home/ansible/.local/bin/poetry install
RUN /home/ansible/.local/bin/poetry run ansible-galaxy collection install paloaltonetworks.panos
RUN echo 'source $POETRY_VIRTUALENVS_PATH/pan-ansible-*/bin/activate' >>~/.zshrc
```

The Dockerfile sets up a slim Python 3.11 environment, installs essential packages, creates an `ansible` user, and configures Oh My Zsh, Poetry for package management, and the Palo Alto Networks Ansible collection.

## Execution Workflow

To execute our container image build, follow these steps:

### Using the CLI

Build the container image with the following command:

```bash
docker build -t ghcr.io/cdot65/pan-ansible:0.1.0 .
```

### Using Invoke

Build the container image using Invoke:

```bash
invoke build
```

Start up the container using Invoke:

```bash
invoke up
```

Access the container shell to execute your Ansible playbooks:

```bash
invoke shell
```

To shut down the container, this will destroy the container:

```bash
invoke down
```

### Screenshots

Here are some screenshots showcasing the execution of our container image build and workflow:

![Screenshot 1](screenshots/screenshot1.png)
![Screenshot 2](screenshots/screenshot2.png)

Feel free to explore the project and customize it according to your specific requirements. Happy automating! 😄
