This README provides an overview of our PAN-OS Out-of-Sync Firewalls Report Generator and guides you through the setup and execution process. 🚀

## Table of Contents

- [PAN-OS Out-of-Sync Firewalls Report Generator 📊](#pan-os-out-of-sync-firewalls-report-generator-)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Prerequisites](#prerequisites)
  - [Setup](#setup)
    - [Creating a Python Virtual Environment](#creating-a-python-virtual-environment)
    - [Installing Dependencies](#installing-dependencies)
    - [Configuring Environment Variables](#configuring-environment-variables)
  - [Script Structure](#script-structure)
  - [Execution Workflow](#execution-workflow)
    - [Command-line Arguments](#command-line-arguments)
    - [Example Usage](#example-usage)

## Overview

Our PAN-OS Out-of-Sync Firewalls Report Generator is designed to connect to a Panorama appliance, retrieve lists of device groups and templates, and generate a PDF report showing which ones are in sync (in green) and which are out of sync (in red). This tool is essential for maintaining a well-managed Palo Alto Networks infrastructure. 🎯

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

To install the required Python packages within your virtual environment, execute:

```bash
pip install -r requirements.txt
```

### Configuring Environment Variables

Our script uses `dynaconf` for configuration management. Create or update the following files in your project directory:

Create a file named `.secrets.yaml`:

```yaml
---
hostname: "your-panorama.example.com"
api_key: "your-api-key"
```

## Script Structure

Our Python script (`app.py`) is structured as follows:

```python
"""Check the synchronization status of device groups and templates in Panorama and generate a PDF report.

This script connects to a Panorama appliance, retrieves lists of device groups and templates,
and generates a PDF report showing which ones are in sync (in green) and which are out of sync (in red).

(c) 2024 Your Name
"""

# Imports and global variables

# Function definitions (get_panorama_data, parse_sync_status, generate_pdf_report, etc.)

def main():
    # Main execution logic
    # 1. Parse command-line arguments
    # 2. Retrieve device groups and templates data
    # 3. Generate PDF report

if __name__ == "__main__":
    main()
```

The script is designed to:

1. Load environment variables for Panorama credentials using `dynaconf`.
2. Retrieve device groups and templates data from Panorama.
3. Parse the data to determine sync status.
4. Generate a PDF report with color-coded sync status.
5. Log activities and errors for debugging purposes.

## Execution Workflow

To execute our Python script, follow these steps:

1. Ensure that you have activated the Python virtual environment.
2. Run the following command:

   ```bash
   python app.py
   ```

### Command-line Arguments

The script supports the following command-line arguments:

- `-d` or `--debug`: Enable debug logging
- `-o` or `--output`: Specify the output PDF file name (default: panorama_sync_report.pdf)

### Example Usage

To generate a report with the default output name:

```bash
python app.py
```

To specify a custom output file name and enable debug logging:

```bash
python app.py -o my_custom_report.pdf --debug
```

Feel free to explore the script and customize it according to your specific requirements. Happy reporting! 😄