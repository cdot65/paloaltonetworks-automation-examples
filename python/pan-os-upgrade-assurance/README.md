# PAN-OS Upgrade Assurance Examples

This README provides an overview of our PAN-OS Upgrade Assurance Examples and guides you through the setup and execution process. 🚀

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Health Check Script Example](#health-check-script-example)
- [Readiness Checks Script Example](#readiness-checks-script-example)
- [Snapshot Example Script Structure](#snapshot-example-script-structure)

## Overview

Our PAN-OS Health Check Tool is designed to perform health checks on Palo Alto Networks firewalls using the `panos_upgrade_assurance` package. This tool allows you to run specific health checks and view the results, helping to ensure the proper functioning of your firewall. 🎯

## Prerequisites

Before getting started, ensure that you have the following prerequisites installed on your local machine:

- Python (version 3.6+) 🐍
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

To install the required Python packages within your virtual environment, execute:

```bash
pip install panos_upgrade_assurance
```

### Configuring Environment Variables

This script doesn't use environment variables directly. However, you may want to securely store your firewall credentials in environment variables or a configuration file for production use.

## Health Check Script Example

Our Python script (`healthcheck_example.py`) is structured as follows:

1. `run_health_checks`: This function initializes a FirewallProxy, creates a CheckFirewall instance, and runs the specified health checks.
2. `print_health_check_results`: This function prints the results of the health checks in a formatted manner.
3. `run_health_checks_example`: This function demonstrates how to use the other functions to perform health checks on a firewall.

### Execution Workflow

To execute our Python script, follow these steps:

1. Ensure that you have activated the Python virtual environment.
2. Run the following command:

    ```bash
    python healthcheck_example.py
    ```

### Command-line Arguments

The script currently doesn't support command-line arguments. All parameters are hardcoded in the `run_health_checks_example` function.

### Example Usage

The script will run the health checks defined in the `run_health_checks_example` function. Currently, it checks for the "device_root_certificate_issue".

Example output:

```
device_root_certificate_issue: Passed
```

or

```
device_root_certificate_issue: Failed
  Reason: [Reason for failure]
```

## Readiness Checks Script Example

Our Python script (`readiness_checks_example.py`) is structured as follows:

```python
from panos_upgrade_assurance.firewall_proxy import FirewallProxy
from panos_upgrade_assurance.check_firewall import CheckFirewall

def run_readiness_checks(hostname: str, username: str, password: str, checks_configuration: list) -> dict:
    # Implementation details...

def print_check_results(results: dict) -> None:
    # Implementation details...

def run_readiness_checks_example():
    # Implementation details...

if __name__ == "__main__":
    run_readiness_checks_example()
```

This script performs readiness checks on a firewall using the panos_upgrade_assurance library. Here's a breakdown of its structure:

1. `run_readiness_checks`: This function initializes a FirewallProxy, creates a CheckFirewall instance, and runs the specified readiness checks.
2. `print_check_results`: This function prints the results of the readiness checks in a formatted manner.
3. `run_readiness_checks_example`: This function demonstrates how to use the `run_readiness_checks` function with a sample configuration.

### Execution Workflow

To execute our Python script, follow these steps:

1. Ensure that you have activated the Python virtual environment.
2. Run the following command:

    ```bash
    python readiness_checks_example.py
    ```

## Snapshot Example Script Structure

Our Python script (`snapshot_compare_example.py`) is structured as follows:

1. Import necessary modules from `panos_upgrade_assurance`.
2. Define the `take_and_compare_snapshots` function to take pre- and post-upgrade snapshots and compare them.
3. Define helper functions `print_changes` and `print_results` to format and display the comparison results.
4. In the main execution block:
    - Define snapshot and comparison configurations.
    - Call `take_and_compare_snapshots` with firewall credentials and configurations.
    - Print the results using the helper functions.

### Execution Workflow

To execute our Python script, follow these steps:

1. Ensure that you have activated the Python virtual environment.
2. Run the following command:

    ```bash
    python snapshot_compare_example.py
    ```

This will:
1. Take a pre-upgrade snapshot of the specified firewall areas.
2. Simulate an upgrade (not actually performed in this example).
3. Take a post-upgrade snapshot.
4. Compare the snapshots based on the defined comparison configuration.
5. Print the results, showing any changes or issues detected.

Note: Remember to replace the firewall credentials in the script with your own before running.

Happy health checking! 😄