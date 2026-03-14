# PAN-OS Static DNS Entry Configuration

## Overview

This script manages static DNS proxy entries on a Palo Alto Networks PAN-OS firewall via the XML API. It reads desired DNS entries from a YAML configuration file, fetches the current static entries from the firewall, and creates or updates only the entries that differ from the intended state. Entries already matching the desired configuration are skipped. Configuration is managed through Dynaconf, which loads settings from `settings.yaml` and credentials from `.secrets.yaml`. The script uses `requests` for HTTP communication with the PAN-OS XML API.

## Prerequisites

- Python 3.11+
- Network access to a PAN-OS firewall with the XML API enabled
- A valid API key for the target firewall
- A DNS proxy profile already configured on the firewall

## Quickstart

1. Clone the repository and navigate to the project directory:

    ```bash
    cd python/panos/configure-static-dns
    ```

2. Create and activate a Python virtual environment:

    ```bash
    python3 -m venv .venv && source .venv/bin/activate
    ```

    > **What is a virtual environment?** A virtual environment is an isolated Python installation that keeps project dependencies separate from your system Python and other projects. This prevents version conflicts and ensures reproducibility.

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Create `.secrets.yaml` with firewall credentials and edit `settings.yaml` with DNS entries.

5. Run the script:

    ```bash
    python app.py
    ```

## Configuration

Create `.secrets.yaml` with firewall credentials:

```yaml
panos:
  hostname: "firewall.example.com"
  apikey: "your-api-key-here"
```

Edit `settings.yaml` to define the DNS proxy domain and static entries:

```yaml
dns:
  domain: example.com
  entries:
    - name: host1
      ip: "192.168.1.10"
      domain_name: host1.example.com
    - name: host2
      ip: "192.168.1.11"
      domain_name: host2.example.com
```

| Variable | Required | Description |
|---|---|---|
| `panos.hostname` | Yes | Firewall IP address or FQDN (in `.secrets.yaml`) |
| `panos.apikey` | Yes | PAN-OS API key (in `.secrets.yaml`) |
| `dns.domain` | Yes | DNS proxy profile domain name (in `settings.yaml`) |
| `dns.entries` | Yes | List of static DNS entries with name, ip, and domain_name |

**Security note:** Never commit `.secrets.yaml` with real API keys to version control.

## Usage

```bash
python app.py
```

Changes are applied to the candidate configuration. Commit separately on the firewall to activate.

### Expected Output

```
Updated DNS Entries:
- name: Kirk
  ip: 192.168.255.11
  domain: kirk.example.com
- name: Spock
  ip: 192.168.255.12
  domain: spock.example.com

Skipped DNS Entries:
- name: Bones
  status: Entry is already in the intended state
- name: Picard
  status: Entry is already in the intended state
```

Updated entries show the name, IP, and domain that were pushed. Skipped entries indicate they already matched the desired state on the firewall.

## Project Structure

```
configure-static-dns/
├── app.py             # Main script: fetches, compares, and updates DNS entries
├── config.py          # Dynaconf settings loader
├── settings.yaml      # DNS domain and entry definitions
├── .secrets.yaml      # Firewall hostname and API key (do not commit real values)
├── requirements.txt   # Python dependencies (requests, dynaconf)
└── screenshots/       # Reference screenshots
```

## Troubleshooting

| Issue | Possible Cause | Solution |
|---|---|---|
| Connection refused | Firewall unreachable or wrong hostname | Verify `panos.hostname` in `.secrets.yaml` and network connectivity |
| Invalid API key | Wrong or expired API key | Regenerate the API key on the firewall and update `.secrets.yaml` |
| `ModuleNotFoundError: No module named 'requests'` | Dependencies not installed | Run `pip install -r requirements.txt` in the virtual environment |
| SSL certificate verification error | Self-signed cert on firewall | The script uses `verify=False` to skip SSL verification |
| Timeout connecting to firewall | Slow network or firewall under load | Check firewall management interface responsiveness |
| DNS proxy not found | Domain name mismatch | Ensure `dns.domain` matches an existing DNS proxy profile on the firewall |
| All entries skipped | All entries already match desired state | This is expected behavior; no changes needed |
