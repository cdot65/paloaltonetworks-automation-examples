# PAN-OS NAT64 Global Counter Fetcher

## Overview

This script queries a PAN-OS firewall's global counters via the XML API and filters for entries matching specified name patterns such as `nat64` or `nptv6`. It is useful for monitoring NAT64 translation activity and troubleshooting IPv6 transition deployments. The script issues the `show counter global` operational command with the `all` filter, parses the XML response using dynamic XPath expressions, and returns matching counter entries with their name, value, rate, and severity. It uses `httpx` for HTTP communication and `lxml` for XML parsing.

## Prerequisites

- Python 3.10+
- Network access to a PAN-OS firewall with the XML API enabled
- A valid API key for the target firewall

## Quickstart

1. Clone the repository and navigate to the project directory:

    ```bash
    cd python/panos/nat64-counters
    ```

2. Create and activate a Python virtual environment:

    ```bash
    python3 -m venv .venv && source .venv/bin/activate
    ```

    > **What is a virtual environment?** A virtual environment is an isolated Python installation that keeps project dependencies separate from your system Python and other projects. This prevents version conflicts and ensures reproducibility.

3. Install dependencies using Poetry:

    ```bash
    poetry install
    ```

    Or install directly:

    ```bash
    pip install httpx lxml
    ```

4. Create a `.env` file with your firewall connection details.

5. Run the script:

    ```bash
    python main.py
    ```

## Configuration

Create a `.env` file in the project root:

```dotenv
FIREWALL=firewall.example.com
API_KEY=your-api-key-here
```

Alternatively, set the `FIREWALL` and `API_KEY` variables directly in `main.py`.

| Variable | Required | Description |
|---|---|---|
| `FIREWALL` | Yes | Firewall IP address or FQDN |
| `API_KEY` | Yes | PAN-OS API key for X-PAN-KEY authentication |

**Security note:** Never commit your `.env` file with real API keys to version control.

## Usage

Run the script directly:

```bash
python main.py
```

Use as a library:

```python
from main import fetch_counters

counters = fetch_counters("firewall.example.com", "your-api-key", patterns=("nat64",))
for c in counters:
    print(f"{c['name']} value={c['value']} rate={c['rate']}")
```

Filter for multiple counter patterns at once:

```python
counters = fetch_counters("fw.example.com", "MY_API_KEY", patterns=("nat64", "nptv6"))
```

### Function Parameters

| Parameter | Default | Description |
|---|---|---|
| `firewall_host` | (required) | FQDN or IP of the PAN-OS firewall |
| `api_key` | (required) | API key for X-PAN-KEY authentication |
| `patterns` | `("nat64",)` | Tuple of substrings to match in counter names (case-sensitive) |
| `verify_ssl` | `False` | Set to `True` if the firewall has a trusted certificate |
| `timeout` | `60.0` | HTTP request timeout in seconds |

### Expected Output

```
flow_nat64_icmp_6to4_no_xlat        value=0     rate=0    severity=drop
flow_nat64_icmp_4to6_no_xlat        value=0     rate=0    severity=drop
flow_nat64_tcp_session_created      value=142   rate=3    severity=info
flow_nat64_udp_session_created      value=87    rate=1    severity=info
flow_nptv6_prefix_xlat_success      value=2034  rate=12   severity=info
```

Each line shows the counter name (left-aligned, 35 chars), its current value, rate per second, and severity level. Only counters whose names contain any of the specified patterns are displayed.

## Troubleshooting

| Issue | Possible Cause | Solution |
|---|---|---|
| Connection refused | Firewall unreachable or wrong hostname | Verify `FIREWALL` in `.env` and network connectivity |
| Invalid API key | Wrong or expired API key | Regenerate the API key on the firewall and update `.env` |
| `ModuleNotFoundError: No module named 'httpx'` | Dependencies not installed | Run `poetry install` or `pip install httpx lxml` |
| SSL certificate verification error | Self-signed cert on firewall | `verify_ssl` defaults to `False`; ensure no proxy overrides it |
| Timeout fetching counters | Large counter table or slow firewall | Increase the `timeout` parameter (default: 60s) |
| No counters returned | Pattern does not match any counter names | Counter name matching is case-sensitive; check exact counter names on the firewall |
