# Configure Panorama Settings (Full Stack)

## Overview

A comprehensive configuration-as-code tool that provisions entire Palo Alto Networks Panorama device group configurations from YAML files using the pan-os-python SDK and Dynaconf. It supports bulk creation of tags, address objects, address groups, service objects, service groups, application objects, and application tags across multiple device groups. All YAML files are deep-merged at startup into a unified configuration, enabling modular file organization by category.

## Prerequisites

- Python 3.11+
- Poetry
- Access to a Palo Alto Networks Panorama appliance
- A Panorama API key

## Quickstart

1. Clone the repository:

   ```bash
   git clone https://github.com/cdot65/paloaltonetworks-automation-examples.git
   cd paloaltonetworks-automation-examples/python/panorama/configure-settings
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

4. Configure credentials by creating a `.secrets.yaml` file:

   ```yaml
   panos_config:
     panorama:
       base_url: "panorama.example.com"
       api_key: "your-api-key-here"
   ```

5. Run the tool:

   ```bash
   python app.py
   ```

## Configuration

Create a `.secrets.yaml` file in the project root with Panorama credentials:

```yaml
panos_config:
  panorama:
    base_url: "panorama.example.com"
    api_key: "your-api-key-here"
```

| Variable | Required | Description |
|---|---|---|
| `panos_config.panorama.base_url` | Yes | Panorama FQDN or IP address |
| `panos_config.panorama.api_key` | Yes | API key for authentication |

**Security note:** Never commit `.secrets.yaml` to version control. Add it to your `.gitignore`.

All configuration lives under the `config/` directory, organized by category:

```
config/
  base.yaml                   # Panorama connection placeholder
  device_groups/              # Device group definitions (e.g., magnolia.yaml)
  objects/                    # Address objects/groups, services, tags, apps, EDLs
  network/                   # Interfaces, zones, virtual routers
  policy/                    # Security rules, NAT rules, PBF
  device/                    # System settings, HA configuration
```

All YAML files are deep-merged at startup. Each file follows a nested structure under `panos_config.device_groups.<name>`, allowing configuration to be split across as many files as needed. Environment variables with the `DYNACONF_` prefix can override any setting.

## Usage

Run the main configuration script:

```bash
python app.py
```

Run with debug logging:

```bash
python app.py --log-level debug
```

| Flag | Description |
|---|---|
| `-l`, `--log-level` | Set logging level: `debug`, `info`, `warning`, `error`, `critical` (default: `info`) |

### Expected Output

```
2025-03-14 10:00:01 - palo_alto_config - INFO - Successfully connected to Panorama with credentials
2025-03-14 10:00:02 - palo_alto_config - INFO - Successfully attached Magnolia device group object to Panorama object
2025-03-14 10:00:02 - palo_alto_config - INFO - Created and added 5 tags to the Magnolia device group using bulk operation
2025-03-14 10:00:03 - palo_alto_config - INFO - Created and added 12 address objects to the Magnolia device group using bulk operation
2025-03-14 10:00:03 - palo_alto_config - INFO - Created and added 3 address groups to the Magnolia device group using bulk operation
2025-03-14 10:00:04 - palo_alto_config - INFO - Created and added 8 service objects to the Magnolia device group using bulk operation
2025-03-14 10:00:04 - palo_alto_config - INFO - Created and added 2 service groups to the Magnolia device group using bulk operation
2025-03-14 10:00:05 - palo_alto_config - INFO - Created and added 4 application tags to the Magnolia device group using bulk operation
2025-03-14 10:00:05 - palo_alto_config - INFO - Created and added 3 application objects to the Magnolia device group using bulk operation
2025-03-14 10:00:06 - palo_alto_config - INFO - Completed bulk creation of objects for Magnolia device group
2025-03-14 10:00:07 - palo_alto_config - INFO - Successfully committed changes to Panorama
2025-03-14 10:00:10 - palo_alto_config - INFO - Successfully committed changes to device group: Magnolia
```

The tool iterates over each configured device group, creating and bulk-pushing all object types. After all groups are configured, it commits to Panorama and pushes to each device group.

## Project Structure

```
configure-settings/
├── app.py                              # CLI entry point, device group iteration, commit logic
├── paloconfig.py                       # PaloConfig class: device group and bulk object management
├── config.py                           # YAML loading, deep-merge, Dynaconf initialization
├── utils.py                            # Singleton logger
├── config/
│   ├── base.yaml                       # Panorama connection placeholder
│   ├── device_groups/                  # Device group definitions
│   │   ├── magnolia.yaml               # Magnolia device group
│   │   └── other_device_groups.yaml    # Additional device groups
│   ├── objects/                        # Object configurations (15+ YAML files)
│   ├── network/                        # Interfaces, zones, virtual routers
│   ├── policy/                         # Security rules, NAT rules, PBF
│   └── device/                         # System settings, HA configuration
├── .secrets.yaml                       # Credentials (do not commit)
└── pyproject.toml                      # Poetry dependencies and build config
```

## Troubleshooting

| Problem | Solution |
|---|---|
| Connection refused | Verify `base_url` in `.secrets.yaml` is correct and Panorama is reachable on port 443 |
| Invalid credentials / 403 | Regenerate your API key in Panorama and update `.secrets.yaml` |
| ModuleNotFoundError | Run `poetry install` to install all dependencies |
| SSL certificate verification error | Ensure your Panorama certificate is trusted, or configure SSL in pan-os-python |
| Timeout during commit | Large configs take time; check Panorama job queue for pending operations |
| `Failed to initialize Dynaconf settings` | Verify all YAML files in `config/` are valid YAML syntax |
| `No tag configuration found for <DG>` | The device group YAML is empty; add object definitions under the appropriate keys |
| `API error while creating address objects` | Check that object names are unique and conform to PAN-OS naming rules (1-63 chars, alphanumeric, `_`, `-`, `.`) |
