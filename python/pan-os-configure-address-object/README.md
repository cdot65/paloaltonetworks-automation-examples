# Create Address Object 📚

This repository contains a Python script designed to automate configuration tasks on Palo Alto Networks Panorama.
Specifically, it provides an example of how to create address objects in a device group using the `pan-os-python` SDK.
🚀

## Table of Contents

- [Palo Alto Networks Panorama Automation 📚](#palo-alto-networks-panorama-automation-)
    - [Overview](#overview)
    - [Prerequisites](#prerequisites)
    - [Dependencies](#dependencies)
    - [Setup](#setup)
        - [Creating a Python Virtual Environment](#creating-a-python-virtual-environment)
        - [Installing Dependencies](#installing-dependencies)
    - [Script Structure](#script-structure)
    - [Usage](#usage)
        - [Command-Line Arguments](#command-line-arguments)
        - [Example: Creating an Address Object](#example-creating-an-address-object)
    - [Execution Workflow](#execution-workflow)
    - [Logging](#logging)
    - [Error Handling](#error-handling)
    - [Contributing](#contributing)
    - [License](#license)

## Overview

The `app.py` script simplifies the process of managing configurations on Panorama. By leveraging the `pan-os-python`
SDK, the script allows you to programmatically create address objects, commit changes, and push configurations to
specific device groups. This automation enhances efficiency and reduces the potential for human error in managing
firewall configurations. 🎯

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- **Python 3.7+** 🐍
- **pip** (Python package manager) 📦
- Access credentials to your **Panorama** instance (hostname/IP, username, and password) 🔐

## Dependencies

The project relies on the following Python packages:

- `pan-os-python`: Official Palo Alto Networks Python SDK for PAN-OS
- `typing-extensions`: Backport of the standard library `typing` module
- Additional built-in modules: `argparse`, `logging`, `sys`

These dependencies are specified in the `requirements.txt` file.

## Setup

### Creating a Python Virtual Environment

It is recommended to run the script within a Python virtual environment to manage dependencies effectively.

1. **Navigate to the Project Directory:**

   ```bash
   cd /path/to/your/project
   ```

2. **Create a Virtual Environment:**

   ```bash
   python3 -m venv venv
   ```

3. **Activate the Virtual Environment:**

    - On **macOS/Linux:**

      ```bash
      source venv/bin/activate
      ```

    - On **Windows:**

      ```bash
      venv\Scripts\activate
      ```

### Installing Dependencies

With the virtual environment activated, install the required packages:

```bash
pip install -r requirements.txt
```

This command reads the `requirements.txt` file and installs the listed packages.

## Script Structure

The project consists of the following key files:

- **`app.py`**: The main script that parses arguments and orchestrates the configuration tasks.
- **`paloconfig.py`**: Contains the `PaloConfig` class that encapsulates methods for interacting with Panorama
  configurations.
- **`utils.py`**: Provides logging utilities via the `Logger` singleton class.

### `app.py`

The `app.py` script performs the following:

1. Parses command-line arguments.
2. Establishes a connection to Panorama.
3. Creates or retrieves a device group.
4. Prepares the address object configuration.
5. Adds the address object to the device group.
6. Commits changes to Panorama.
7. Pushes changes to the specified device group.

### `paloconfig.py`

Defines the `PaloConfig` class with methods to:

- Create device groups.
- Add address objects.
- Commit changes to Panorama.
- Push configurations to device groups.

### `utils.py`

Provides a `Logger` class for consistent logging across the application, allowing you to set the logging level and log
messages at various severity levels.

## Usage

### Command-Line Arguments

The script accepts several command-line arguments:

- `--hostname`: **(Required)** Panorama hostname or IP address.
- `--username`: **(Required)** Panorama username.
- `--password`: **(Required)** Panorama password.
- `--device-group`: **(Required)** Name of the device group.
- `--address-name`: **(Required)** Name of the address object to create.
- `--address-type`: **(Required)** Type of the address object (`ip-netmask`, `ip-range`, `fqdn`).
- `--address-value`: **(Required)** Value of the address object (e.g., IP address, FQDN).
- `--address-description`: Description for the address object.
- `--address-tags`: Tags to associate with the address object.
- `-l`, `--log-level`: Set the logging level (`debug`, `info`, `warning`, `error`, `critical`).

**Example:**

```bash
python app.py --hostname panorama.example.com \
              --username admin \
              --password secretpassword \
              --device-group ExampleDeviceGroup \
              --address-name WebServer \
              --address-type ip-netmask \
              --address-value 192.168.1.10 \
              --address-description "Corporate web server" \
              --address-tags Web Servers Production
```

### Example: Creating an Address Object

Here's how you can use the script to create an address object:

1. **Prepare the Command:**

   Replace the placeholders with your actual Panorama details and desired address object configuration.

   ```bash
   python app.py --hostname <PANORAMA_HOSTNAME> \
                 --username <USERNAME> \
                 --password <PASSWORD> \
                 --device-group <DEVICE_GROUP_NAME> \
                 --address-name <ADDRESS_OBJECT_NAME> \
                 --address-type <ADDRESS_OBJECT_TYPE> \
                 --address-value <ADDRESS_OBJECT_VALUE> \
                 --address-description "<ADDRESS_DESCRIPTION>" \
                 --address-tags <TAG1> <TAG2>
   ```

2. **Execute the Command:**

   Run the command in your terminal. The script will output logs indicating the progress.

3. **Verify the Results:**

    - **On Panorama:**
        - Log in to your Panorama web interface.
        - Navigate to **Objects** > **Addresses** under the specified device group.
        - Confirm that the new address object has been created.

    - **In the Terminal:**
        - The script will print `{"status": "completed"}` upon successful execution.

**Note:** Ensure that the user account you use has the necessary permissions to perform configuration changes and
commits on Panorama.

## Execution Workflow

1. **Script Invocation:**

   The script is invoked with the required command-line arguments.

2. **Argument Parsing:**

   Arguments are parsed using the `argparse` module.

3. **Logging Level Configuration:**

   The logging level is set based on the `--log-level` argument.

4. **Panorama Connection:**

   A connection to Panorama is established using the provided credentials.

5. **Device Group Handling:**

   The specified device group is created or retrieved.

6. **Address Object Creation:**

   An address object is configured and added to the device group.

7. **Commit Changes to Panorama:**

   Changes are committed to Panorama.

8. **Push Changes to Device Group:**

   The configuration changes are pushed to the specified device group.

9. **Completion:**

   The script outputs `{"status": "completed"}` and exits with a success code (`0`).

## Logging

The script provides informative logging at various steps:

- **INFO:**

    - Successful connections.
    - Successful configurations and commits.

- **WARNING:**

    - Missing configurations.
    - Non-critical issues that do not stop execution.

- **ERROR:**

    - Failed operations that may require attention.

- **CRITICAL:**

    - Severe errors that cause the script to exit.

You can control the verbosity using the `--log-level` argument.

**Example:**

```bash
python app.py --hostname panorama.example.com \
              --username admin \
              --password secretpassword \
              --device-group ExampleDeviceGroup \
              --address-name WebServer \
              --address-type ip-netmask \
              --address-value 192.168.1.10 \
              --address-description "Corporate web server" \
              --address-tags Web Servers Production \
              --log-level debug
```

## Error Handling

The script includes comprehensive error handling to catch exceptions and provide meaningful messages:

- **PanDeviceError:**

    - Issues related to PAN-OS device operations.

- **Exception:**

    - Catches any unexpected errors.

In case of an error, the script outputs `{"status": "errored"}` and exits with a failure code (`1`).

## Contributing

We welcome contributions to enhance the functionality of this script. Please follow these steps:

1. **Fork the Repository:**

   Click the **Fork** button at the top-right corner of this page.

2. **Clone the Forked Repository:**

   ```bash
   git clone https://github.com/your-username/your-forked-repo.git
   ```

3. **Create a Feature Branch:**

   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Make Changes and Commit:**

   ```bash
   git commit -am "Add your commit message"
   ```

5. **Push Changes to GitHub:**

   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request:**

   Open a pull request to merge your changes into the main repository.

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

Feel free to explore the script and adapt it to suit your automation needs. If you encounter any issues or have
suggestions for improvements, please open an issue or submit a pull request. Happy automating! 😄