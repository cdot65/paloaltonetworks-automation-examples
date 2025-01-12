# IP Tag Manager

A Python utility for managing IP address tags on PAN-OS devices using the pan-os-python SDK. This tool allows you to
register, unregister, list, and manage IP tags efficiently through a command-line interface.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
    - [Basic Commands](#basic-commands)
    - [Examples](#examples)
- [Configuration](#configuration)
- [Error Handling](#error-handling)
- [Contributing](#contributing)
- [License](#license)

## Features

- List all registered IP tags
- Register new IP-tag associations with optional timeout
- Unregister specific IP-tag combinations
- Clear all IP tags from the device
- Audit and synchronize IP-tag mappings
- Comprehensive error handling and logging
- Support for virtual systems (VSYS)

## Prerequisites

- Python 3.7 or higher
- Access to a PAN-OS device (firewall or Panorama)
- Network connectivity to the target device
- Valid credentials with appropriate permissions

## Installation

1. Clone the repository:

    ```bash
    git clone git@github.com:cdot65/paloaltonetworks-automation-examples.git
    cd paloaltonetworks-automation-examples/python/pan-os-dag
    ```

2. Create and activate a virtual environment:

   Make sure you have Python3.11 or higher

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: .\venv\Scripts\activate
    ```

3. Install required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Basic Commands

The script provides several commands for managing IP tags:

1. **List all registered IP tags**:

    ```bash
    python ip_tag_manager.py --host <firewall> --username <user> --password <pass> list
    ```

2. **Register tags for an IP**:

    ```bash
    python ip_tag_manager.py --host <firewall> --username <user> --password <pass> register <ip> <tags> [--timeout <seconds>]
    ```

3. **Unregister specific tags**:

    ```bash
    python ip_tag_manager.py --host <firewall> --username <user> --password <pass> unregister <ip> <tags>
    ```

4. **Clear all IP tags**:

    ```bash
    python ip_tag_manager.py --host <firewall> --username <user> --password <pass> clear
    ```

### Examples

1. Register multiple tags for a web server:

    ```bash
    python ip_tag_manager.py --host fw.example.com --username admin --password secret register 10.0.0.1 "linux,apache,webserver" --timeout 3600
    ```

2. List all registered IP tags:

    ```bash
    python ip_tag_manager.py --host fw.example.com --username admin --password secret list
    ```

   Example output:

    ```
    10.0.0.1: linux, apache, webserver
    10.0.0.2: windows, sql
    10.0.0.3: linux, mongodb
    ```

3. Remove specific tags from an IP:

    ```bash
    python ip_tag_manager.py --host fw.example.com --username admin --password secret unregister 10.0.0.1 "apache,webserver"
    ```

## Configuration

The script supports the following configuration options:

| Option     | Required | Default | Description                      |
|------------|----------|---------|----------------------------------|
| --host     | Yes      | -       | Firewall/Panorama hostname or IP |
| --username | Yes      | -       | Username for authentication      |
| --password | Yes      | -       | Password for authentication      |
| --vsys     | No       | vsys1   | Virtual system name              |
| --timeout  | No       | None    | Tag timeout in seconds           |

## Error Handling

The script includes comprehensive error handling and logging:

- Connection failures
- Authentication errors
- Invalid IP addresses or tags
- PAN-OS API errors
- Network connectivity issues

Logs are written to stdout with timestamps and appropriate log levels. Example:

```
2025-01-04 10:15:30 - INFO - Successfully connected to fw.example.com
2025-01-04 10:15:31 - INFO - Retrieved 3 registered IP addresses
2025-01-04 10:15:32 - ERROR - Failed to register tags for IP 10.0.0.1: Invalid IP address
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to
discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License

---

For more information about the pan-os-python SDK, visit
the [official documentation](https://pan-os-python.readthedocs.io/).

For questions or issues, please open a GitHub issue in this repository.