# PAN-OS Security Policy Configuration via Panorama

## Overview

This project configures security policies and associated objects on Palo Alto Networks Panorama using the `pan-os-python` SDK. It reads hierarchical YAML configuration files for device groups, tags, address objects, services, and security rules, then pushes them to Panorama and commits to device groups. Configuration is managed through Dynaconf with deep merging across multiple YAML files organized by category. A `PaloConfig` class wraps common Panorama operations including device group creation, bulk security rule creation via `create_similar()`, and commit/commit-all workflows.

## Prerequisites

- Python 3.10+
- Network access to a Panorama instance with API enabled
- Valid admin credentials or API key for Panorama

## Quickstart

1. Clone the repository and navigate to the project directory:

    ```bash
    cd python/panos/configure-security-policies
    ```

2. Create and activate a Python virtual environment:

    ```bash
    python3 -m venv .venv && source .venv/bin/activate
    ```

    > **What is a virtual environment?** A virtual environment is an isolated Python installation that keeps project dependencies separate from your system Python and other projects. This prevents version conflicts and ensures reproducibility.

3. Install dependencies:

    ```bash
    poetry install
    ```

    Or without Poetry:

    ```bash
    pip install pan-os-python dynaconf lxml
    ```

4. Create `.secrets.yaml` from `.secrets.example.yaml` and populate with Panorama credentials.

5. Edit YAML files under `config/` to define your desired configuration.

6. Run the script:

    ```bash
    python app.py
    ```

## Configuration

Create `.secrets.yaml` from `.secrets.example.yaml`:

```yaml
panos_config:
  panorama:
    api_key: "your-api-key-here"
```

The base Panorama URL is set in `config/base.yaml`:

```yaml
panos_config:
  panorama:
    base_url: "panorama.example.com"
```

YAML config files are organized under `config/`:

```
config/
  base.yaml                 # Panorama connection settings
  device_groups/*.yaml      # Device group definitions
  objects/*.yaml            # Address objects, services, tags
  network/*.yaml            # Interfaces, zones, virtual routers
  policy/*.yaml             # Security rules, NAT rules
  device/*.yaml             # HA settings, system settings
```

| Variable | Required | Description |
|---|---|---|
| `panos_config.panorama.base_url` | Yes | Panorama hostname or IP (in `config/base.yaml`) |
| `panos_config.panorama.api_key` | Yes | Panorama API key (in `.secrets.yaml`) |

All YAML files matching the patterns in `config.py` are deep-merged at load time. Add or edit files in any subdirectory to extend the configuration.

**Security note:** Never commit `.secrets.yaml` with real credentials to version control.

## Usage

Apply configuration to Panorama and push to device groups:

```bash
python app.py
```

Override settings via environment variable:

```bash
DYNACONF_LOG_LEVEL=DEBUG python app.py
```

### Expected Output

```
2024-01-15 10:30:00 [INFO] Base directory: /path/to/configure-security-policies
2024-01-15 10:30:00 [INFO] Config files to be loaded:
2024-01-15 10:30:00 [INFO]   config/base.yaml
2024-01-15 10:30:00 [INFO]   .secrets.yaml
2024-01-15 10:30:01 [INFO] Successfully connected to Panorama with credentials
2024-01-15 10:30:01 [INFO] Successfully attached Magnolia device group object to Panorama object
2024-01-15 10:30:02 [INFO] Created and added tags to the Magnolia device group
2024-01-15 10:30:03 [INFO] Successfully committed changes to Panorama
2024-01-15 10:30:10 [INFO] Configuration pushed to device group: Magnolia
```

The script commits changes to Panorama synchronously, then pushes to the specified device group. Additional object types (address groups, zones, security rules) are present in the codebase but currently commented out for incremental rollout.

## Project Structure

```
configure-security-policies/
├── app.py              # Main entry point: connects to Panorama, creates objects, commits
├── paloconfig.py       # PaloConfig class: device groups, security rules, commit operations
├── config.py           # Dynaconf configuration loader with deep merge across config/**/*.yaml
├── utils.py            # Singleton logger class
├── .secrets.example.yaml # Template for Panorama credentials
├── pyproject.toml      # Poetry dependencies (pan-os-python, dynaconf, lxml)
└── config/             # Hierarchical YAML configuration
    ├── base.yaml       # Panorama connection settings
    ├── device_groups/  # Device group definitions
    ├── objects/        # Address objects, services, tags
    ├── network/        # Interfaces, zones, virtual routers
    ├── policy/         # Security rules, NAT rules
    └── device/         # HA settings, system settings
```

## Troubleshooting

| Issue | Possible Cause | Solution |
|---|---|---|
| Connection refused | Panorama unreachable or wrong hostname | Verify `base_url` in `config/base.yaml` and network connectivity |
| Invalid credentials | Wrong API key | Regenerate API key on Panorama and update `.secrets.yaml` |
| `ModuleNotFoundError: No module named 'panos'` | Dependencies not installed | Run `poetry install` or `pip install pan-os-python` |
| SSL certificate verification failed | Self-signed cert on Panorama | pan-os-python disables verification by default; check for proxy interference |
| Timeout during commit | Large configuration or slow Panorama | Commits are synchronous (`sync=True`); increase timeout or check Panorama load |
| No tags found for device group | Missing YAML config for the device group | Add tag definitions to the appropriate `config/objects/*.yaml` file |
| YAML parsing error | Malformed YAML in config files | Validate YAML syntax; `config.py` logs and skips invalid files |
