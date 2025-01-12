# Prisma Access Address Object and Group Automation 📚

This README provides an overview of our Python project and guides you through the setup and execution process. 🚀

## Table of Contents

- [Prisma Access Address Object and Group Automation 📚](#prisma-access-address-object-and-group-automation-)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Prerequisites](#prerequisites)
  - [Setup](#setup)
    - [Creating a Python Virtual Environment](#creating-a-python-virtual-environment)
    - [Installing Dependencies](#installing-dependencies)
  - [Script Structure](#script-structure)
    - [`address-group.py`](#address-grouppy)
    - [`address-object.py`](#address-objectpy)
  - [Execution Workflow](#execution-workflow)
    - [Screenshots](#screenshots)

## Overview

Our Python project aims to automate the configuration of address objects and address groups in Prisma Access using the panapi SDK and Dynaconf for secrets management. By leveraging Python's powerful automation capabilities, we can streamline the process and ensure consistent and reproducible results across multiple environments. 🎯

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

To install the required Python packages within our virtual environment, use the following command:

```bash
pip install -r requirements.txt
```

## Script Structure

Our Python scripts (`address-object.py` and `address-group.py`) are structured to interact with the Prisma Access API using the panapi SDK. Below, we provide an overview of each script.

### `address-group.py`

```python
# dynaconf to handle settings and secrets
from config import settings

# Palo Alto Networks Prisma imports
from panapi import PanApiSession
from panapi.config.objects import AddressGroup

# create an empty session
session = PanApiSession()

# authenticate to Prisma OAUTH API
session.authenticate(
    client_id=settings.oauth.client_id,
    client_secret=settings.oauth.client_secret,
    scope=f"profile tsg_id:{settings.oauth.tsg} email",
    token_url=settings.oauth.token_url,
)

# create an address object dictionary
address_group = {
    "folder": "Prisma Access",
    "name": "test",
    "description": "this is just a test",
    "static": ["panapi test"],
}

# pass the dictionary as arguments into a new AddressGroup object

prisma_address_group = AddressGroup(**address_group)

# create the address object
prisma_address_group.create(session)

# delete the address object
# prisma_address_group.delete(session)

```

### `address-object.py`

```python
# dynaconf to handle settings and secrets
from config import settings

# Palo Alto Networks Prisma imports
from panapi import PanApiSession
from panapi.config.objects import Address

# create an empty session
session = PanApiSession()

# authenticate to Prisma OAUTH API
session.authenticate(
    client_id=settings.oauth.client_id,
    client_secret=settings.oauth.client_secret,
    scope=f"profile tsg_id:{settings.tenant.mytentantid.tsg} email",
    token_url=settings.oauth.token_url,
)

# create an address object dictionary
address_object = {
    "folder": "Prisma Access",
    "name": "panapi test",
    "description": "this is just a test",
    "fqdn": "test.redtail.com",
}

# pass the dictionary as arguments into a new PrismaAddress object
prisma_address_object = Address(**address_object)

# create the address object
prisma_address_object.create(session)

# delete the address object
# prisma_address_object.delete(session)

```

## Execution Workflow

To execute our Python scripts, follow these steps:

1. Ensure that you have activated the Python virtual environment.
2. Update the `.secrets.yaml` with your own service account credentials for Prisma Access TSG.
3. Run one of the scripts using the following command:

   ```bash
   python address-object.py
   ```

   or

   ```bash
   python address-group.py
   ```

### Screenshots

Here are some screenshots showcasing the execution of our Python script:

![Screenshot 1](screenshots/screenshot1.png)
![Screenshot 2](screenshots/screenshot2.png)

Feel free to explore the script and customize it according to your specific requirements. Happy automating! 😄
