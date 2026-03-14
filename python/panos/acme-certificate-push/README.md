# ACME Certificate Deployment to PAN-OS Firewalls

## Overview

This script deploys ACME-issued TLS certificates (e.g., Let's Encrypt) to one or more Palo Alto Networks firewalls by wrapping the `acme.sh` CLI deploy hook for PAN-OS. It iterates over a comma-separated list of firewall hostnames passed as a command-line argument, setting the `PANOS_HOST` environment variable for each device before invoking the deploy hook. The script uses Python's `subprocess` module to call `acme.sh` and `urllib3` to suppress insecure-request warnings.

## Prerequisites

- Python 3.11+
- [acme.sh](https://github.com/acmesh-official/acme.sh) installed with a valid certificate already issued for the target domain
- PAN-OS firewalls with API access enabled
- Environment variables required by the acme.sh PAN-OS deploy hook (`PANOS_USER`, `PANOS_PASS` or `PANOS_KEY`) set in the shell

## Quickstart

1. Clone the repository and navigate to the project directory:

    ```bash
    cd python/panos/acme-certificate-push
    ```

2. Create and activate a Python virtual environment:

    ```bash
    python3 -m venv .venv && source .venv/bin/activate
    ```

    > **What is a virtual environment?** A virtual environment is an isolated Python installation that keeps project dependencies separate from your system Python and other projects. This prevents version conflicts and ensures reproducibility.

3. Install dependencies:

    ```bash
    pip install urllib3
    ```

4. Set the required acme.sh deploy hook environment variables:

    ```bash
    export PANOS_USER=admin
    export PANOS_PASS=your-password-here
    ```

5. Run the script:

    ```bash
    python app.py fw01.example.com
    ```

## Configuration

The script relies on environment variables for PAN-OS authentication (consumed by `acme.sh`, not by this script directly) and command-line arguments for targeting devices.

| Variable | Required | Description |
|---|---|---|
| `PANOS_USER` | Yes | PAN-OS admin username (used by acme.sh deploy hook) |
| `PANOS_PASS` | Yes* | PAN-OS admin password (used by acme.sh deploy hook) |
| `PANOS_KEY` | Yes* | PAN-OS API key (alternative to `PANOS_PASS`) |

*One of `PANOS_PASS` or `PANOS_KEY` is required.

**Security note:** Never hard-code credentials in scripts or commit them to version control. Export them in your shell session or use a secrets manager.

## Usage

Deploy to a single firewall:

```bash
python app.py fw01.example.com
```

Deploy to multiple firewalls:

```bash
python app.py fw01.example.com,fw02.example.com,fw03.example.com
```

Custom domain and acme.sh path:

```bash
python app.py fw01.example.com --domain example.com --acme-path /usr/local/bin/acme.sh
```

### CLI Arguments

| Argument | Default | Description |
|---|---|---|
| `devices` | (required) | Comma-separated list of firewall hostnames |
| `--domain` | `example.com` | Domain for the certificate |
| `--acme-path` | `/Users/cdot/.acme.sh/acme.sh` | Path to the acme.sh script |

### Expected Output

```
Setting PANOS_HOST to fw01.example.com
Successfully deployed certificate to fw01.example.com
[acme.sh deploy hook output...]

Setting PANOS_HOST to fw02.example.com
Successfully deployed certificate to fw02.example.com
[acme.sh deploy hook output...]
```

If deployment fails for a device, the error and stderr from acme.sh are printed:

```
Setting PANOS_HOST to fw03.example.com
Error deploying certificate to fw03.example.com: Command '...' returned non-zero exit status 1.
[acme.sh error output...]
```

## Troubleshooting

| Issue | Possible Cause | Solution |
|---|---|---|
| Connection refused | Firewall unreachable or wrong hostname | Verify hostname resolves and firewall management port is accessible |
| Invalid credentials | Wrong `PANOS_USER`/`PANOS_PASS` | Verify environment variables are exported correctly in the current shell |
| `ModuleNotFoundError: No module named 'urllib3'` | Dependencies not installed | Run `pip install urllib3` in the virtual environment |
| SSL certificate error from acme.sh | Self-signed cert on firewall | The `--insecure` flag is already passed to acme.sh by the script |
| `FileNotFoundError` for acme.sh | acme.sh not installed or wrong path | Install acme.sh or pass the correct path via `--acme-path` |
| Timeout during deployment | Slow network or large certificate chain | Check network connectivity to the firewall management interface |
