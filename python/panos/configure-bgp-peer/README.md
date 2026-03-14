# PAN-OS BGP Peer Configuration

## Overview

This script configures BGP peering on a Palo Alto Networks firewall using the `pan-os-python` SDK. It creates a virtual router with BGP enabled, adds an eBGP peer group with soft-reset-with-stored-info, and configures one or more BGP peers with IPv4 address family from a YAML settings file. Configuration is managed through Dynaconf, which loads BGP parameters from `settings.yaml` and firewall credentials from `.secrets.yaml`.

## Prerequisites

- Python 3.11+
- Network access to a PAN-OS firewall with API enabled
- Valid admin credentials for the target firewall

## Quickstart

1. Clone the repository and navigate to the project directory:

    ```bash
    cd python/panos/configure-bgp-peer
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

4. Configure `settings.yaml` with BGP parameters and `.secrets.yaml` with firewall credentials.

5. Run the script:

    ```bash
    python app.py
    ```

## Configuration

Edit `settings.yaml` with your BGP parameters:

```yaml
vr_name: "default"
router_id: "172.16.255.1"
local_as: 65000
bgp_name: "MPLS"
neighbors:
  - name: "peer1"
    asn: 65001
    iface: "ethernet1/8"
    local_ip: "10.10.10.1/24"
    peer_ip: "10.10.10.2"
```

Create `.secrets.yaml` with firewall credentials:

```yaml
hostname: "192.168.1.1"
username: "admin"
password: "your-password-here"
```

| Variable | Required | Description |
|---|---|---|
| `hostname` | Yes | Firewall IP address or FQDN (in `.secrets.yaml`) |
| `username` | Yes | Admin username (in `.secrets.yaml`) |
| `password` | Yes | Admin password (in `.secrets.yaml`) |
| `vr_name` | Yes | Virtual router name |
| `router_id` | Yes | BGP router ID |
| `local_as` | Yes | Local AS number |
| `bgp_name` | Yes | BGP peer group name |
| `neighbors` | Yes | List of BGP peer definitions (name, asn, iface, local_ip, peer_ip) |

**Security note:** Never commit `.secrets.yaml` with real credentials to version control.

## Usage

```bash
python app.py
```

The script applies BGP configuration directly to the firewall's candidate configuration. It does not commit automatically; commit manually via the firewall UI or API after verifying the candidate config.

### Expected Output

The script does not produce console output on success. If a `PanDeviceError` occurs (wrong credentials, unreachable firewall, invalid configuration), a Python exception traceback is raised. After successful execution, verify in the PAN-OS UI under Network > Virtual Routers > BGP that the peer group and peers are configured.

## Troubleshooting

| Issue | Possible Cause | Solution |
|---|---|---|
| Connection refused | Firewall unreachable or wrong hostname | Verify `hostname` in `.secrets.yaml` and network connectivity |
| Invalid credentials | Wrong username or password | Check `username` and `password` in `.secrets.yaml` |
| `ModuleNotFoundError: No module named 'panos'` | Dependencies not installed | Run `pip install -r requirements.txt` in the virtual environment |
| SSL certificate verification failed | Self-signed cert on firewall | pan-os-python disables verification by default; check for proxy interference |
| Timeout connecting to firewall | Slow network or firewall under load | Verify firewall management interface is responsive |
| Virtual router not found | VR name mismatch | Ensure `vr_name` matches an existing virtual router on the firewall |
