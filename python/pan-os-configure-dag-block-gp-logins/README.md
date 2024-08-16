# Block Failed GlobalProtect Logins with Python 📚

This README provides an overview of our Python project and guides you through the setup and execution process. 🚀

## Table of Contents

- [Block Failed GlobalProtect Logins with Python 📚](#block-failed-globalprotect-logins-with-python-)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Prerequisites](#prerequisites)
  - [Dependencies](#dependencies)
  - [Setup](#setup)
    - [Creating a Python Virtual Environment](#creating-a-python-virtual-environment)
    - [Installing Dependencies](#installing-dependencies)
  - [Script Structure](#script-structure)
  - [Execution Workflow](#execution-workflow)
    - [Screenshots](#screenshots)

## Overview

The `block-gp-baddies` Python project aims to automate the process of updating Dynamic Address Groups (DAGs) in PAN-OS firewalls. It queries the firewall logs for failed login attempts, extracts public IP addresses, generates an XML file with these IPs, and updates the firewall's address groups accordingly. By leveraging Python's powerful automation capabilities, we can streamline the process and ensure consistent and reproducible results across multiple environments. 🎯

## Prerequisites

Before getting started, ensure that you have the following prerequisites installed on your local machine:

- Python (version 3.11+) 🐍
- pip (Python package manager) 📦

## Dependencies

- `requests`: For making HTTP requests to the PAN-OS API.
- `dynaconf`: For dynamic configuration management.
- `lxml`: For XML file generation and handling.
- Development dependencies like `black`, `flake8`, `ipdb`, and `ipython` for code formatting, linting, and debugging.

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

Install packages within our virtual environment by running:

   ```bash
   pip install lxml requests dynaconf
   ```

Or you can use the `pyproject.toml` setup with the command:

   ```bash
   poetry install
   ```

## Script Structure

Our Python script (`app.py`) is structured as follows:

```python
import logging
import requests
import sys
import time
import xml.etree.ElementTree as ET

from config import settings
from lxml import etree

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def create_job() -> str:
    # Job creation logic here

def check_job_status(job_id: str) -> str:
    # Job status checking logic here

def get_job_results(job_id: str) -> bytes:
    # Job results retrieval logic here

def extract_public_ips(root: ET.Element) -> set:
    # Public IP extraction logic here

def generate_xml_file(public_ips: set, filename="dags.xml") -> str:
    # XML file generation logic here

def send_xml_to_firewall(xml_filename: str) -> str:
    # XML file sending logic here

def main():
    # Main workflow function here

if __name__ == "__main__":
    main()
```

The script performs the following high-level steps:

1. Create a job on the firewall to fetch the last 100 GlobalProtect logs with authentication failures.
2. Check the status of the job until it is complete.
3. Retrieve and parse the job results.
4. Extract the public IPs from the job results.
5. Generate an XML file of DAG entries to add to the firewall.
6. Send the generated XML file to the firewall.

## Execution Workflow

To execute our Python script, follow these steps:

1. Ensure that you have activated the Python virtual environment.
2. Update the `settings.yaml` file with your PAN-OS firewall details and other configurations.
3. Run the following command:

   ```bash
   python app.py
   ```

### Screenshots

Here are some screenshots showcasing the execution of our Python script:

![Screenshot 1](screenshots/screenshot1.png)
![Screenshot 2](screenshots/screenshot2.png)

Feel free to explore the script and customize it according to your specific requirements. Happy automating! 😄
