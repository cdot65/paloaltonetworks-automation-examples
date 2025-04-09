# Create Address Object 📚

This repository contains a Python script designed to automate configuration tasks on Palo Alto Networks Panorama.
Specifically, it provides an example of how to create address objects in a device group using the `pan-os-python` SDK.
🚀

## Table of Contents

- [Create Address Object 📚](#create-address-object-)
  - [Overview](#overview)
  - [Prerequisites](#prerequisites)
  - [Dependencies](#dependencies)
  - [Setup](#setup)
  - [Configuration](#configuration)
  - [Usage](#usage)
  - [Contributing](#contributing)
  - [License](#license)

## Overview

The script automates the creation of address objects in Palo Alto Networks Panorama device groups. It uses the `pan-os-python`
SDK to programmatically create address objects, commit changes to Panorama, and push configurations to device groups. This automation enhances efficiency and reduces the potential for human error in managing firewall configurations. 🎯

## Prerequisites

Before you begin, ensure you have:

- **Python 3.7+** 🐍
- **Poetry** (Python dependency management) 📦
- Access to a **Panorama** instance (hostname and API key) 🔐

## Dependencies

The project uses Poetry for dependency management. Key dependencies include:

- `pan-os-python`: Official Palo Alto Networks Python SDK for PAN-OS
- `python-dotenv`: For environment variable management
- `pyyaml`: For YAML configuration parsing

## Setup

1. **Clone the Repository:**
   ```bash
   git clone <repository-url>
   cd pan-os-configure-address-object
   ```

2. **Install Dependencies:**
   ```bash
   poetry install
   ```

3. **Configure Environment:**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` with your Panorama details.

## Configuration

### Environment Variables

Required environment variables in `.env`:
- `PANORAMA_HOSTNAME`: Panorama hostname or IP
- `PANORAMA_API_KEY`: API key for authentication
- `PANORAMA_COMMIT`: Set to "true" to commit changes (default: false)

### YAML Configuration

Address objects are defined in YAML files. Example structure:
```yaml
address_objects:
  - device_group: LAB_DG
    name: test101
    value: 10.0.1.1
    description: Test address object
    tags:
      - test
      - lab
```

## Usage

1. **Create Configuration:**
   Create a YAML file with your address object definitions.

2. **Run the Script:**
   ```bash
   poetry run python app.py --config config/address_objects.yaml
   ```

The script will:
1. Connect to Panorama
2. Create address objects in specified device groups
3. Commit changes to Panorama
4. Push changes to device groups

### Logging

Set `PANORAMA_LOG_LEVEL` environment variable to control logging (DEBUG, INFO, WARNING, ERROR).

## Contributing

Contributions are welcome! Please feel free to submit pull requests.

## License

This project is licensed under the MIT License.