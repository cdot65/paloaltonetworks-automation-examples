# PAN-OS Tunnel and Loopback Interface Automation

This project provides automation for creating and configuring tunnel and loopback interfaces on Palo Alto Networks firewalls using Panorama management platform.

## Project Overview

This automation solution follows a clean separation of concerns:

1. **Configuration Models** - Define the structure and validation of interface configurations
2. **PAN-OS Client** - Handles all interactions with the Panorama API
3. **Main Application** - Orchestrates the workflow and processes configuration files

## Project Structure

- `app.py` - Main application entry point and orchestration
- `models.py` - Pydantic models for data validation and configuration
- `panos_client.py` - Client for interacting with PAN-OS API
- `config/` - YAML configuration files
  - `tunnel_interfaces.yaml` - Tunnel interface configurations (via Templates)
  - `loopback_interfaces.yaml` - Loopback interface configurations (via Template Stacks)

## Order of Operations

### Main Application Flow (app.py)

The main application performs the following steps:

1. Parse command-line arguments to get the configuration file path
2. Load and validate the configuration using Pydantic models
3. Connect to Panorama using environment variables
4. Process the configuration:
   - For tunnel interfaces: Create interfaces via Templates
   - For loopback interfaces: Create interfaces via Template Stacks
5. Commit changes to Panorama
6. Push changes to devices via a commit-all operation

### Data Modeling (models.py)

The models.py file defines several Pydantic models:

- `AddressObject` - Structure for network address objects
- `TunnelInterface` - Structure for tunnel interfaces with validation
- `LoopbackInterface` - Structure for loopback interfaces with validation
- `Config` - Main configuration model for YAML files

These models ensure all configuration data is properly validated before being used.

### PAN-OS API Interactions (panos_client.py)

The PanosClient class provides these key functions:

1. `connect()` - Establishes connection to Panorama
2. `get_or_create_template()` - Retrieves or creates a Template
3. `get_or_create_template_stack()` - Retrieves or creates a Template Stack
4. `create_tunnel_interface()` - Creates tunnel interfaces in Templates
5. `create_loopback_interface()` - Creates loopback interfaces in Template Stacks
6. `commit_to_panorama()` - Commits changes to Panorama
7. `commit_all()` - Pushes changes to devices

### Commit Process

The commit process is handled in two phases:

1. **Panorama Commit** - First commits all changes to Panorama
2. **Template/Template Stack Commit** - Then pushes changes to devices

For Template Stacks, the system:
1. Identifies which templates are associated with each template stack
2. Uses PanoramaCommitAll with "template stack" style to push changes
3. Handles both template and template stack commits in a single operation

## Requirements

- Python 3.10+
- PAN-OS Python SDK
- Panorama with API access

## Usage

```bash
# Configure tunnel interfaces using Templates
poetry run python app.py --config config/tunnel_interfaces.yaml

# Configure loopback interfaces using Template Stacks
poetry run python app.py --config config/loopback_interfaces.yaml
```

## Environment Variables

The following environment variables are required:

- `PANORAMA_HOSTNAME`: Hostname or IP address of your Panorama instance
- `PANORAMA_API_KEY`: API key for authentication
- `PANORAMA_COMMIT`: Set to "true" to commit changes (optional)
