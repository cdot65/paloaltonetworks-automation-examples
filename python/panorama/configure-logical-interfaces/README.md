# Configure Panorama Logical Interfaces

## Overview

A CLI tool that creates tunnel and loopback interfaces on Palo Alto Networks Panorama using the pan-os-python SDK. Tunnel interfaces are created within Panorama Templates and loopback interfaces within Template Stacks, both defined via YAML configuration files and validated with Pydantic models. IP addresses can be literal values or PAN-OS template variables (prefixed with `$`). After creation, changes can be automatically committed and pushed to managed firewalls.

## Prerequisites

- Python 3.11+
- Poetry
- Access to a Palo Alto Networks Panorama appliance
- A Panorama API key

## Quickstart

1. Clone the repository:

   ```bash
   git clone https://github.com/cdot65/paloaltonetworks-automation-examples.git
   cd paloaltonetworks-automation-examples/python/panorama/configure-logical-interfaces
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
   python app.py --config config/tunnel_interfaces.yaml
   ```

## Configuration

Copy `.env.example` to `.env` and populate with your values:

```env
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

**Security note:** Never commit your `.env` file containing real credentials to version control.

Tunnel interface YAML format (created under Templates):

```yaml
tunnel_interfaces:
  - template: "LAB_TEMPLATE"
    entries:
      - name: "tunnel"
        subinterface: "1"
        ip:
          - "$TUNNEL_IP"
        comment: "IPsec tunnel interface"
        security_zone: "UNTRUST"
```

Loopback interface YAML format (created under Template Stacks):

```yaml
loopback_interfaces:
  - template_stack: "DALLAS_STACK"
    entries:
      - name: "loopback.1"
        ip:
          - "192.168.5.1/32"
        comment: "Inside loopback interface"
```

## Usage

Create tunnel interfaces:

```bash
python app.py --config config/tunnel_interfaces.yaml
```

Create loopback interfaces:

```bash
python app.py --config config/loopback_interfaces.yaml
```

Create interfaces and commit:

```bash
PANORAMA_COMMIT=true python app.py --config config/tunnel_interfaces.yaml
```

| Flag | Description |
|---|---|
| `--config` | **(required)** Path to YAML configuration file |

### Expected Output

```
2025-03-14 10:00:01 - panorama - INFO - Parsed arguments: config=config/tunnel_interfaces.yaml
2025-03-14 10:00:02 - panorama - INFO - Found 4 device groups on Panorama
2025-03-14 10:00:02 - panorama - INFO - Found 3 templates on Panorama
2025-03-14 10:00:02 - panorama - INFO - Found 2 template stacks on Panorama
2025-03-14 10:00:02 - panorama - INFO - Loaded configuration from config/tunnel_interfaces.yaml
2025-03-14 10:00:03 - panorama - INFO - Found existing template: LAB_TEMPLATE
2025-03-14 10:00:03 - panorama - INFO - Created tunnel interface: tunnel.1 with IP ['$TUNNEL_IP']
2025-03-14 10:00:03 - panorama - INFO - Created tunnel interface: tunnel.1
2025-03-14 10:00:04 - panorama - INFO - Created tunnel interface: tunnel.2 with IP ['10.1.1.1/24']
2025-03-14 10:00:04 - panorama - INFO - Created tunnel interface: tunnel.2
2025-03-14 10:00:05 - panorama - INFO - Initiating commit to Panorama...
2025-03-14 10:00:10 - panorama - INFO - Successfully committed changes to Panorama
2025-03-14 10:00:10 - panorama - INFO - Successfully pushed changes to templates and template stacks
```

Each log line shows template/stack lookups, interface creation with IP assignment, and commit status. The tool creates the interface name by combining `name` and `subinterface` (e.g., `tunnel.1`).

## Project Structure

```
configure-logical-interfaces/
├── app.py                              # CLI entry point, argument parsing, main logic
├── models.py                           # Pydantic models (TunnelInterface, LoopbackInterface, Config)
├── panos_client.py                     # Panorama client with template/stack/interface management
├── config/
│   ├── tunnel_interfaces.yaml          # Sample tunnel interface configuration
│   └── loopback_interfaces.yaml        # Sample loopback interface configuration
├── .env.example                        # Environment variable template
├── pyproject.toml                      # Poetry dependencies and tool config
└── Makefile                            # format, lint, typecheck, test commands
```

## Troubleshooting

| Problem | Solution |
|---|---|
| Connection refused | Verify `PANORAMA_HOSTNAME` is correct and Panorama is reachable on port 443 |
| Invalid credentials / 403 | Regenerate your API key in Panorama and update `.env` |
| ModuleNotFoundError | Run `poetry install` to install all dependencies |
| SSL certificate verification error | Ensure your Panorama certificate is trusted, or configure SSL in pan-os-python |
| Timeout during commit | Large configs take time; check Panorama job queue for pending operations |
| `Object already exists` warning | The tool handles this gracefully and continues; the interface was previously created |
| `PANORAMA_HOSTNAME and PANORAMA_API_KEY must be set` | Verify `.env` file exists and both variables are populated |
