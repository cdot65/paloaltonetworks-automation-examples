# PAN-OS Configuration Global Search

## Overview

This script searches the merged XML configuration of a live PAN-OS firewall for specified keywords. For each match it reports the XPath location, enclosing entry name, and the full object configuration rendered as YAML. It retrieves the merged (running + candidate) configuration using the `show config merged` operational command, then walks the entire XML tree looking for text nodes and attribute values containing any of the configured keywords. Results are displayed in a summary table via `tabulate` followed by detailed per-match YAML output. Configuration is managed through Dynaconf, and the script uses `lxml` for XML parsing and `xmltodict` for XML-to-YAML conversion. Content-preview application descriptions are excluded from results to reduce noise.

## Prerequisites

- Python 3.11+
- Network access to a PAN-OS firewall with the XML API enabled
- A valid API key for the target firewall

## Quickstart

1. Clone the repository and navigate to the project directory:

    ```bash
    cd python/panos/global-search
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

4. Create `.secrets.yaml` with firewall credentials and edit `settings.yaml` with search keywords.

5. Run the script:

    ```bash
    python app.py
    ```

## Configuration

Create `.secrets.yaml` with firewall credentials:

```yaml
hostname: "firewall.example.com"
api_key: "your-api-key-here"
```

Edit `settings.yaml` to define search keywords:

```yaml
keywords:
  - "Cloudflare DNS"
  - "10.0.0.1"
```

| Variable | Required | Description |
|---|---|---|
| `hostname` | Yes | Firewall IP address or FQDN (in `.secrets.yaml`) |
| `api_key` | Yes | PAN-OS API key (in `.secrets.yaml`) |
| `keywords` | Yes | List of search terms to look for in the configuration (in `settings.yaml`) |

**Security note:** Never commit `.secrets.yaml` with real API keys to version control.

## Usage

Run a basic search:

```bash
python app.py
```

Run with debug logging:

```bash
python app.py --debug
```

### CLI Flags

| Flag | Short | Description |
|---|---|---|
| `--debug` | `-d` | Enable debug-level logging to console and `search.log` |

### Expected Output

```
+------+----------------+------------------+-------------------------------------------+
|  No. | Matched Word   | Entry Name       | XPath                                     |
+------+----------------+------------------+-------------------------------------------+
|    1 | Cloudflare DNS | dns-primary      | /config[1]/devices[1]/entry[1]/network... |
|    2 | Cloudflare DNS | dns-secondary    | /config[1]/devices[1]/entry[1]/network... |
+------+----------------+------------------+-------------------------------------------+

Found 2 matches.

Detailed Results:
================================================================================

Result 1:
Matched Word: Cloudflare DNS
XPath: /config[1]/devices[1]/entry[1]/network[1]/dns-proxy[1]...
Entry Name: dns-primary
Full YAML Configuration:
entry:
  '@name': dns-primary
  address:
    member: 1.1.1.1
  domain: example.com

--------------------------------------------------------------------------------
```

A `search.log` file is created in the working directory with timestamped log entries. When `--debug` is used, additional detail about each element inspected is included.

## Project Structure

```
global-search/
├── app.py             # Main script: retrieves config and searches for keywords
├── config.py          # Dynaconf settings loader
├── settings.yaml      # Keywords to search for
├── .secrets.yaml      # Firewall hostname and API key (do not commit real values)
├── requirements.txt   # Python dependencies (requests, lxml, tabulate, xmltodict, dynaconf)
└── screenshots/       # Reference screenshots
```

## Troubleshooting

| Issue | Possible Cause | Solution |
|---|---|---|
| Connection refused | Firewall unreachable or wrong hostname | Verify `hostname` in `.secrets.yaml` and network connectivity |
| Invalid API key | Wrong or expired API key | Regenerate the API key on the firewall and update `.secrets.yaml` |
| `ModuleNotFoundError: No module named 'lxml'` | Dependencies not installed | Run `pip install -r requirements.txt` in the virtual environment |
| SSL certificate verification error | Self-signed cert on firewall | The script uses `verify=False` to skip SSL verification |
| Timeout retrieving configuration | Large configuration or slow firewall | Check firewall responsiveness; consider increasing request timeout |
| No matches found | Keywords do not appear in the configuration | Verify keywords in `settings.yaml`; try broader search terms |
| XML parsing error | Unexpected API response format | Enable `--debug` and inspect the raw response in `search.log` |
