# Prisma Access Security Policy 📚

This README provides an overview of the `prisma-access-security-policy` Python project and guides you through the setup and execution process. 🚀

## Table of Contents

- [Prisma Access Security Policy 📚](#prisma-access-security-policy-)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Prerequisites](#prerequisites)
  - [Setup](#setup)
    - [Creating a Python Virtual Environment](#creating-a-python-virtual-environment)
    - [Installing Dependencies](#installing-dependencies)
  - [Script Structure](#script-structure)
  - [Execution Workflow](#execution-workflow)
    - [Screenshots](#screenshots)

## Overview

Our Python project aims to automate the configuration and deployment of a security policy using the Prisma Access API. By leveraging Python's powerful automation capabilities and the panapi SDK, we can streamline the process and ensure consistent and reproducible results across multiple environments. 🎯 Dynaconf is used for secrets management in this project.

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

### Installing Dependencies

To install the required Python packages within our virtual environment, run the following command:

```bash
pip install -r requirements.txt
```

## Script Structure

Our Python script (`app.py`) is structured as follows:

```python
# dynaconf to handle settings and secrets
from config import settings

# Palo Alto Networks Prisma imports
from panapi.config.security import SecurityRule
from panapi import PanApiSession

session = PanApiSession()

# authenticate to Prisma Access OAuth API
session.authenticate(
    client_id=settings.oauth.client_id,
    client_secret=settings.oauth.client_secret,
    scope=f"profile tsg_id:{settings.oauth.tsg} email",
    token_url=settings.oauth.token_url,
)

# Create a security rule object
security_rule = {
    "name": "DMZ Outbound",
    "action": "allow",
    "from": ["any"],
    "to": ["any"],
    "source": ["any"],
    "destination": ["any"],
    "source_user": ["any"],
    "category": ["any"],
    "application": ["any"],
    "service": ["application-default"],
    "log_setting": "Cortex Data Lake",
    "description": "Control outbound internet access for DMZ",
    "folder": "Prisma Accses",
    "position": "pre",
}

# Create the security rule
prisma_rule = SecurityRule(**security_rule)
prisma_rule.create(session)

```

The script begins by importing the Dynaconf settings module for handling secrets and preparing the Prisma Access SDK imports. After authenticating with the Prisma Access API using credentials defined in the `.secrets.yaml` file, it creates a security rule and deploys it using the PanApiSession instance.

## Execution Workflow

To execute our Python script, follow these steps:

1. Ensure that you have activated the Python virtual environment.
2. Update the `.secrets.yaml` file with your Prisma Access TSG service account credentials:

    ```yaml
    ---
    # secrets.yaml
    oauth:
      client_id: "your-client-id"
      client_secret: "your-client-secret"
      token_url: "your-token-url"
      tsg: "your-tsg-id"
    ```

3. Run the following command:

   ```bash
   python app.py
   ```

### Screenshots

Here are some screenshots showcasing the execution of our Python script:

![Screenshot 1](screenshots/screenshot1.png)
![Screenshot 2](screenshots/screenshot2.png)

Feel free to explore the script and customize it according to your specific requirements. Happy automating! 😄
