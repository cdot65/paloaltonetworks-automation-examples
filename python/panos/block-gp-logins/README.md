# GlobalProtect Failed Login Blocker

## Overview

This script queries a PAN-OS firewall for failed GlobalProtect authentication attempts, extracts the source public IPs, and registers them as Dynamic Address Group (DAG) tag entries via the User-ID API. This enables automated blocking of brute-force login sources through security policies that reference the DAG tag. It uses the PAN-OS XML API directly via `requests` for log queries and DAG registration, `lxml` for XML generation, and Dynaconf for configuration management.

## Prerequisites

- Python 3.10+
- PAN-OS firewall with GlobalProtect configured and a valid API key
- A Dynamic Address Group and security policy referencing the DAG tag already configured on the firewall

## Quickstart

1. Clone the repository and navigate to the project directory:

    ```bash
    cd python/panos/block-gp-logins
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
    pip install requests dynaconf lxml
    ```

4. Configure `settings.yaml` with firewall details and DAG tag name.

5. Run the script:

    ```bash
    python app.py
    ```

## Configuration

Edit `settings.yaml`:

```yaml
panos:
  hostname: "192.168.1.1"
  apikey: "your-api-key-here"
  trusted_users: ["trusteduser1", "trusteduser2"]
  dag_tag: "blocked-gp-attackers"
```

Optionally create `.secrets.yaml` if separating credentials (Dynaconf loads it after `settings.yaml`).

| Variable | Required | Description |
|---|---|---|
| `panos.hostname` | Yes | Firewall IP address or FQDN |
| `panos.apikey` | Yes | PAN-OS API key for authentication |
| `panos.trusted_users` | No | List of usernames to exclude from the query |
| `panos.dag_tag` | Yes | Tag name to register against offending IPs |

**Security note:** Never commit `settings.yaml` or `.secrets.yaml` with real API keys to version control.

## Usage

Run once:

```bash
python app.py
```

Schedule via cron for continuous protection (e.g., every 5 minutes):

```
*/5 * * * * cd /path/to/block-gp-logins && /path/to/.venv/bin/python app.py
```

### Expected Output

```
2024-01-15 10:30:00 [INFO] Job still processing...
2024-01-15 10:30:03 [INFO] Job still processing...
2024-01-15 10:30:06 [INFO] Job completed.
2024-01-15 10:30:07 [INFO] <response status="success"><result/></response>
```

The script creates a `dags.xml` file in the working directory containing the generated UID XML payload. The firewall API response is logged after DAG entries are registered.

## Project Structure

```
block-gp-logins/
├── app.py            # Main script: queries logs, extracts IPs, registers DAG tags
├── config.py         # Dynaconf settings loader
├── settings.yaml     # Firewall hostname, API key, trusted users, DAG tag
├── dags.xml          # Example/generated DAG XML payload
└── pyproject.toml    # Poetry dependencies (requests, dynaconf, lxml)
```

## Troubleshooting

| Issue | Possible Cause | Solution |
|---|---|---|
| Connection refused | Firewall unreachable or wrong hostname | Verify `panos.hostname` in `settings.yaml` and network connectivity |
| Invalid API key | Wrong or expired API key | Regenerate the API key on the firewall and update `settings.yaml` |
| `ModuleNotFoundError: No module named 'lxml'` | Dependencies not installed | Run `poetry install` or `pip install lxml` |
| SSL certificate verification error | Self-signed cert on firewall | The script does not set `verify=False`; add it to requests calls if needed |
| Timeout during log query | Large log volume or slow firewall | Increase the `timeout` parameter in the `create_job` function |
| No public IPs extracted | No failed logins in the last 100 log entries | Check GlobalProtect logs on the firewall directly to confirm activity |
| XML parsing error | Unexpected API response format | Enable debug logging and inspect the raw XML response |
