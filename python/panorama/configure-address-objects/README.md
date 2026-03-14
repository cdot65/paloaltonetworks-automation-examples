# Configure Panorama Address Objects

## Overview

A CLI tool that creates IP-netmask address objects on Palo Alto Networks Panorama using the pan-os-python SDK. Address objects are defined in YAML configuration files organized by device group, validated with Pydantic, and pushed to Panorama via the XML API. The tool supports automatic commit to Panorama and push to device groups. All output is logged to the console (and optionally to a file) through a singleton logger.

## Prerequisites

- Python 3.11+
- Poetry
- Access to a Palo Alto Networks Panorama appliance
- A Panorama API key

## Quickstart

1. Clone the repository:

   ```bash
   git clone https://github.com/cdot65/paloaltonetworks-automation-examples.git
   cd paloaltonetworks-automation-examples/python/panorama/configure-address-objects
   ```

2. Create and activate a virtual environment:

   ```bash
   python3 -m venv .venv && source .venv/bin/activate
   ```

   > **What is a virtual environment?** A virtual environment is an isolated Python installation that keeps project dependencies separate from your system Python, preventing version conflicts between projects.

3. Install dependencies:

   ```bash
   poetry install
   ```

4. Configure credentials:

   ```bash
   cp .env.example .env
   # Edit .env with your Panorama hostname and API key
   ```

5. Run the tool:

   ```bash
   python app.py --config config/address_objects.yaml
   ```

## Configuration

Copy `.env.example` to `.env` and populate with your values:

```env
PANORAMA_LOG_LEVEL=info
PANORAMA_HOSTNAME=panorama.example.com
PANORAMA_API_KEY=your-api-key-here
PANORAMA_COMMIT=true
```

| Variable | Required | Description |
|---|---|---|
| `PANORAMA_HOSTNAME` | Yes | Panorama FQDN or IP address |
| `PANORAMA_API_KEY` | Yes | API key for authentication |
| `PANORAMA_COMMIT` | No | Set to `true` to commit and push changes after creation |
| `PANORAMA_LOG_LEVEL` | No | Logging level (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`) |
| `PANORAMA_LOG_FILE` | No | Path to a log output file |

**Security note:** Never commit your `.env` file containing real credentials to version control. The `.env.example` file contains only placeholder values.

The YAML config file defines address objects per device group:

```yaml
address_objects:
  - device_group: "LAB_DG"
    entries:
      - name: "webserver01"
        value: "10.0.1.10/32"
        description: "Web server"
        tags:
          - "automation"
```

## Usage

Create address objects from configuration:

```bash
python app.py --config config/address_objects.yaml
```

Create address objects and commit changes:

```bash
PANORAMA_COMMIT=true python app.py --config config/address_objects.yaml
```

| Flag | Description |
|---|---|
| `--config` | **(required)** Path to YAML configuration file |

### Expected Output

```
2025-03-14 10:00:01 - panorama - INFO - Parsed arguments: config=config/address_objects.yaml
2025-03-14 10:00:02 - panorama - INFO - Found 4 device groups on Panorama
2025-03-14 10:00:02 - panorama - INFO - Loaded configuration from config/address_objects.yaml
2025-03-14 10:00:02 - panorama - INFO - Found existing device group: LAB_DG
2025-03-14 10:00:03 - panorama - INFO - Created address object: test101
2025-03-14 10:00:03 - panorama - INFO - Created address object: test101
2025-03-14 10:00:03 - panorama - INFO - Found existing device group: WOODLANDS_DG
2025-03-14 10:00:04 - panorama - INFO - Created address object: test102
2025-03-14 10:00:05 - panorama - INFO - Initiating commit to Panorama...
2025-03-14 10:00:10 - panorama - INFO - Successfully committed changes to Panorama
2025-03-14 10:00:10 - panorama - INFO - Initiating commit-all to device group: LAB_DG
2025-03-14 10:00:15 - panorama - INFO - Successfully initiated commit-all to device group: LAB_DG
2025-03-14 10:00:15 - panorama - INFO - Successfully pushed changes to device groups
```

Each log line follows the format `timestamp - panorama - LEVEL - message`. The tool reports device group lookups, address object creation results, and commit status.

## Project Structure

```
configure-address-objects/
├── app.py                          # CLI entry point, argument parsing, main logic
├── models.py                       # Pydantic models (AddressObject, Config)
├── panos_client.py                 # Panorama client wrapping pan-os-python SDK
├── utils.py                        # Singleton logger and IP validation utilities
├── config/
│   └── address_objects.yaml        # Sample YAML configuration
├── tests/
│   ├── test_panos_client.py        # Client unit tests
│   └── test_utils.py               # Utility unit tests
├── .env.example                    # Environment variable template
├── pyproject.toml                  # Poetry dependencies and tool config
└── Makefile                        # format, lint, type, test commands
```

## Troubleshooting

| Problem | Solution |
|---|---|
| Connection refused | Verify `PANORAMA_HOSTNAME` is correct and Panorama is reachable on port 443 |
| Invalid credentials / 403 | Regenerate your API key in Panorama and update `.env` |
| ModuleNotFoundError | Run `poetry install` to install all dependencies |
| SSL certificate verification error | Ensure your Panorama certificate is trusted, or set SSL verification in pan-os-python |
| Timeout during commit | Large configs take time; increase timeout or check Panorama job queue |
| `Invalid YAML format: root must be a dictionary` | Ensure your YAML file has `address_objects:` as the top-level key |
| `PANORAMA_HOSTNAME and PANORAMA_API_KEY must be set` | Verify `.env` file exists and both variables are populated |
