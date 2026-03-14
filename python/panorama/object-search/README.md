# Panorama Address Object Search

## Overview

A CLI tool that searches for address objects across all device groups in Palo Alto Networks Panorama and maps their membership in address groups, including nested group relationships. It uses the pan-os-python SDK to retrieve configuration from both Shared and per-device-group scopes, Dynaconf for settings management, and renders results as formatted tables using pandas and tabulate. Output is printed to the console and logged to `search.log`.

## Prerequisites

- Python 3.11+
- pip
- Access to a Palo Alto Networks Panorama appliance
- Panorama credentials (username and password)

## Quickstart

1. Clone the repository:

   ```bash
   git clone https://github.com/cdot65/paloaltonetworks-automation-examples.git
   cd paloaltonetworks-automation-examples/python/panorama/object-search
   ```

2. Create and activate a virtual environment:

   ```bash
   python3 -m venv .venv && source .venv/bin/activate
   ```

   > **What is a virtual environment?** A virtual environment is an isolated Python installation that keeps project dependencies separate from your system Python, preventing version conflicts between projects.

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure credentials by creating a `.secrets.yaml` file:

   ```yaml
   hostname: "panorama.example.com"
   username: "your-username"
   password: "your-password"
   ```

5. Configure search prefixes in `settings.yaml`:

   ```yaml
   prefixes:
     - 10.0.0.1/32
     - 172.16.0.2
   ```

6. Run the tool:

   ```bash
   python app.py
   ```

## Configuration

Create a `.secrets.yaml` file with Panorama credentials:

```yaml
hostname: "panorama.example.com"
username: "your-username"
password: "your-password"
```

Create or edit `settings.yaml` with IP prefixes to search:

```yaml
prefixes:
  - 10.0.0.1/32
  - 172.16.0.2
```

| Variable | Required | Description |
|---|---|---|
| `hostname` | Yes | Panorama FQDN or IP address (in `.secrets.yaml`) |
| `username` | Yes | Panorama admin username (in `.secrets.yaml`) |
| `password` | Yes | Panorama admin password (in `.secrets.yaml`) |
| `prefixes` | No | List of IP prefixes to search (in `settings.yaml`; can be overridden via `--prefix`) |

Both files are loaded by Dynaconf. You can also set values via environment variables with the `DYNACONF_` prefix (e.g., `DYNACONF_HOSTNAME`).

**Security note:** Never commit `.secrets.yaml` to version control. Add it to your `.gitignore`.

## Usage

Search using prefixes from `settings.yaml`:

```bash
python app.py
```

Search for specific prefixes via CLI:

```bash
python app.py --prefix "10.0.0.1/32,172.16.0.2"
```

Enable debug logging:

```bash
python app.py --debug
```

| Flag | Description |
|---|---|
| `-p`, `--prefix` | Comma-separated list of IP prefixes to search (overrides `settings.yaml`) |
| `-d`, `--debug` | Enable debug-level logging |

### Expected Output

```
Searching for instances of 172.16.0.2
╒════╤══════════╤══════════════════════╤═══════════════════╤══════════════════════════════════════════╕
│    │ 0        │ 1                    │ 2                 │ 3                                        │
╞════╪══════════╪══════════════════════╪═══════════════════╪══════════════════════════════════════════╡
│  0 │ Shared   │ Internal-Servers     │ Server subnet     │ ['webserver01', 'dbserver01', 'app01']   │
├────┼──────────┼──────────────────────┼───────────────────┼──────────────────────────────────────────┤
│  1 │ LAB_DG   │ Lab-Address-Group    │                   │ ['Internal-Servers', 'DMZ-Servers']      │
╘════╧══════════╧══════════════════════╧═══════════════════╧══════════════════════════════════════════╛

Searching for instances of 1.1.1.1/32
2025-03-14 10:00:05 - WARNING - No match was found for 1.1.1.1/32
```

Columns in the table represent: index, source scope (Shared or device group name), address group name, description, and member list. If the address object is found but not in any group, a debug message is logged. If no match is found at all, a warning is logged.

## Project Structure

```
object-search/
├── app.py              # Main script: config retrieval, matching, and table display
├── config.py           # Dynaconf settings loader
├── settings.yaml       # Default search prefixes
├── .secrets.yaml       # Panorama credentials (do not commit)
├── requirements.txt    # Python dependencies
└── screenshots/        # Example output screenshots
```

## Troubleshooting

| Problem | Solution |
|---|---|
| Connection refused | Verify `hostname` in `.secrets.yaml` is correct and Panorama is reachable on port 443 |
| Invalid credentials / 403 | Verify `username` and `password` in `.secrets.yaml` are correct |
| ModuleNotFoundError | Run `pip install -r requirements.txt` to install all dependencies |
| SSL certificate verification error | Ensure your Panorama certificate is trusted by your Python environment |
| Timeout retrieving config | Large Panorama configs take time; ensure network connectivity is stable |
| `No match was found for <prefix>` | The IP prefix does not exist as an address object value on Panorama |
| `AttributeError: settings has no attribute` | Ensure both `settings.yaml` and `.secrets.yaml` exist and are valid YAML |
