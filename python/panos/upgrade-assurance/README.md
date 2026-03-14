# PAN-OS Upgrade Assurance Examples

## Overview

This project contains three standalone example scripts demonstrating the `panos-upgrade-assurance` library for running readiness checks, health checks, and pre/post-upgrade snapshot comparisons on Palo Alto Networks firewalls. The readiness checks script validates upgrade readiness by checking active support, NTP sync, candidate config, expired licenses, Panorama connectivity, content version, and free disk space. The health checks script verifies device health conditions such as root certificate status. The snapshots script captures network state (routes, ARP table, sessions, interfaces, IPSec tunnels, licenses, content version) before and after an upgrade window and produces a structured diff with configurable change thresholds.

## Prerequisites

- Python 3.11+
- Network access to a PAN-OS firewall with the API enabled
- Valid username and password for the target firewall

## Quickstart

1. Clone the repository and navigate to the project directory:

    ```bash
    cd python/panos/upgrade-assurance
    ```

2. Create and activate a Python virtual environment:

    ```bash
    python3 -m venv .venv && source .venv/bin/activate
    ```

    > **What is a virtual environment?** A virtual environment is an isolated Python installation that keeps project dependencies separate from your system Python and other projects. This prevents version conflicts and ensures reproducibility.

3. Install dependencies:

    ```bash
    pip install panos-upgrade-assurance
    ```

4. Update firewall credentials in each script's example function (hostname, username, password).

5. Run a script:

    ```bash
    python readiness_checks_example.py
    ```

## Configuration

Firewall credentials are set directly in each script's example function. Before running, update the following values:

```python
hostname = "your-firewall.example.com"
username = "admin"
password = "your-password-here"
```

| Variable | Required | Description |
|---|---|---|
| `hostname` | Yes | Firewall IP address or FQDN |
| `username` | Yes | Admin username for API authentication |
| `password` | Yes | Admin password for API authentication |

**Security note:** The example scripts contain placeholder credentials. Replace them with your actual values but do not commit real credentials to version control. Consider refactoring to use environment variables or a `.env` file for production use.

## Usage

### Readiness Checks

Validates that a firewall is ready for upgrade:

```bash
python readiness_checks_example.py
```

### Health Checks

Runs device health checks:

```bash
python healthcheck_example.py
```

### Snapshot Comparison

Takes pre- and post-upgrade snapshots and compares them:

```bash
python snapshots_example.py
```

### Expected Output

Readiness checks:

```
active_support: Passed
candidate_config: Passed
expired_licenses: Passed
jobs: Passed
ntp_sync: Passed
panorama: Failed
  Reason: Device is not connected to Panorama
content_version: Passed
free_disk_space: Passed
```

Health checks:

```
device_root_certificate_issue: Passed
```

Snapshot comparison:

```
Taking pre-upgrade snapshot...
Taking post-upgrade snapshot...

ROUTES comparison:
  No significant changes detected.

ARP_TABLE comparison:
  Changes detected:
    Missing entries: ['10.0.0.1']
    Added entries: ['10.0.0.5']

CONTENT_VERSION comparison:
  No significant changes detected.

SESSION_STATS comparison:
  Changes detected:
    Count change percentage: 5.2%
    Count change threshold: 10%
```

Each check reports Passed or Failed. Failed checks include a reason. Snapshot comparisons report missing, added, and changed entries with configurable thresholds.

## Project Structure

```
upgrade-assurance/
├── readiness_checks_example.py   # Validates upgrade readiness (support, licenses, NTP, disk space)
├── healthcheck_example.py        # Runs device health checks (e.g., root certificate issues)
├── snapshots_example.py          # Captures and compares network state snapshots with thresholds
└── poetry.lock                   # Locked dependency versions
```

## Troubleshooting

| Issue | Possible Cause | Solution |
|---|---|---|
| Connection refused | Firewall unreachable or wrong hostname | Verify hostname and network connectivity |
| Invalid credentials | Wrong username or password | Check the credentials in the script's example function |
| `ModuleNotFoundError: No module named 'panos_upgrade_assurance'` | Library not installed | Run `pip install panos-upgrade-assurance` |
| SSL certificate verification failed | Self-signed cert on firewall | The library handles this by default; check for proxy interference |
| Timeout connecting to firewall | Slow network or firewall under load | Verify firewall management interface is responsive |
| Panorama check fails | Firewall not connected to Panorama | This is expected if the firewall is standalone; not an error in the script |
| Snapshot comparison shows unexpected changes | Normal operational drift between snapshots | Adjust `count_change_threshold` in the comparison config to set acceptable variance |
