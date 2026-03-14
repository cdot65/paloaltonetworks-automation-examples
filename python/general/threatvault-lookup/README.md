# ThreatVault File Hash Lookup

## Overview

A Python script that computes SHA-256 hashes of files in a local directory and queries the Palo Alto Networks ThreatVault API to retrieve associated threat intelligence data. ThreatVault is the threat database behind PAN-OS WildFire, Threat Prevention, and URL Filtering. The tool uses the `requests` library for API calls and Dynaconf for configuration management with YAML settings files and a separate secrets file for the API key. Results are printed as formatted JSON to stdout.

## Prerequisites

- Python 3.8+
- A Palo Alto Networks ThreatVault API key

## Quickstart

1. **Clone the repository:**

   ```bash
   git clone https://github.com/cdot65/paloaltonetworks-automation-examples.git
   cd paloaltonetworks-automation-examples/python/general/threatvault-lookup
   ```

2. **Create and activate a virtual environment:**

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

   > **Tip -- What is a virtual environment?** A virtual environment is an isolated Python installation that keeps project dependencies separate from your system Python. This prevents version conflicts between projects.

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure your API key:**

   ```bash
   cp .secrets.yaml.example .secrets.yaml
   ```

   Edit `.secrets.yaml` with your ThreatVault API key.

5. **Place files to analyze in the `files/` directory, then run:**

   ```bash
   python app.py
   ```

## Configuration

**`settings.yaml`** -- API endpoint configuration:

```yaml
---
baseurl: "api.threatvault.paloaltonetworks.com/service"
```

**`.secrets.yaml`** -- API key (do not commit):

```yaml
---
apikey: "your-threatvault-api-key-here"
```

| Variable | Required | Description |
|---|---|---|
| `apikey` | Yes | ThreatVault API key (set in `.secrets.yaml` or `DYNACONF_APIKEY` env var) |
| `baseurl` | No | ThreatVault API base URL (default: `api.threatvault.paloaltonetworks.com/service`) |

Environment variables can override any setting with the `DYNACONF_` prefix:

```bash
DYNACONF_APIKEY="your-key" python app.py
```

**Security note:** Never commit `.secrets.yaml` with real API keys to version control.

## Usage

**Basic run:**

Place one or more files in the `files/` directory, then:

```bash
python app.py
```

**Override API key via environment variable:**

```bash
DYNACONF_APIKEY="your-key" python app.py
```

### Expected Output

When files are present in the `files/` directory and the API key is valid:

```json
{
  "success": true,
  "link": {
    "next": null,
    "previous": null
  },
  "count": 1,
  "data": [
    {
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "filetype": "PE",
      "verdict": "malware",
      "family": "WildFire.Malware",
      "create_time": "2024-01-15T14:30:22Z",
      "signatures": [
        {
          "name": "generic.ml",
          "severity": "high"
        }
      ]
    }
  ]
}
```

If no files are found:

```
No files found in the 'files' directory.
```

If the API call fails:

```
Error occurred during API request: 401 Client Error: Unauthorized
Failed to retrieve threat data from ThreatVault.
```

## Project Structure

```
threatvault-lookup/
  app.py                    # Main script: SHA-256 hash computation and ThreatVault API calls
  config.py                 # Dynaconf settings loader (reads settings.yaml and .secrets.yaml)
  settings.yaml             # Base URL configuration
  .secrets.yaml.example     # API key template (copy to .secrets.yaml)
  requirements.txt          # Dependencies (dynaconf, requests)
  files/                    # Drop files here for hash lookup (contains .gitkeep)
```

## Troubleshooting

| Issue | Cause | Solution |
|---|---|---|
| `Error: API endpoint not found. Status code: 404` | Incorrect base URL | Verify `baseurl` in `settings.yaml` matches the ThreatVault API |
| `Error occurred during API request: 401 Unauthorized` | Invalid or missing API key | Set `apikey` in `.secrets.yaml` or export `DYNACONF_APIKEY` |
| `ModuleNotFoundError: No module named 'dynaconf'` | Dependencies not installed | Run `pip install -r requirements.txt` |
| SSL certificate verify failed | Corporate proxy or outdated CA certs | Update system CA certificates or set `verify=False` in requests |
| Connection timeout | Network issues or API downtime | Check network connectivity to `api.threatvault.paloaltonetworks.com` |
| `No files found in the 'files' directory` | Empty `files/` directory | Place files to analyze in the `files/` directory |
| `Error: Directory 'files' not found` | Missing `files/` directory | Create it with `mkdir files` |
