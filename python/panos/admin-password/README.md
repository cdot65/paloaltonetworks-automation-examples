# PAN-OS Admin Password Rotation

## Overview

This script rotates the administrator password on a Palo Alto Networks PAN-OS firewall using the `pan-os-python` SDK. It can generate a cryptographically secure 16-character random password or accept a user-provided one via the `--new-password` flag. The script authenticates to the firewall with the current credentials, updates the admin password through the PAN-OS API, and prints the new password to stdout. Credentials are loaded from environment variables or a `.env` file via `python-dotenv`.

## Prerequisites

- Python 3.11+
- Network access to the PAN-OS firewall management interface
- Valid admin credentials for the target firewall

## Quickstart

1. Clone the repository and navigate to the project directory:

    ```bash
    cd python/panos/admin-password
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

4. Copy `.env.example` to `.env` and populate with your values:

    ```bash
    cp .env.example .env
    ```

5. Run the script:

    ```bash
    python rotate_admin_password.py
    ```

## Configuration

Create a `.env` file in the project root (see `.env.example`):

```dotenv
PANOS_HOSTNAME=your-firewall-hostname.example.com
PANOS_USERNAME=admin
PANOS_PASSWORD=your-current-admin-password
```

| Variable | Required | Description |
|---|---|---|
| `PANOS_HOSTNAME` | Yes | Firewall IP address or FQDN |
| `PANOS_USERNAME` | Yes | Admin username to authenticate and rotate |
| `PANOS_PASSWORD` | Yes | Current password for the admin user |

**Security note:** Never commit your `.env` file to version control. The `.gitignore` file already excludes it.

## Usage

Auto-generate a new password (interactive confirmation prompt):

```bash
python rotate_admin_password.py
```

Supply a specific new password:

```bash
python rotate_admin_password.py --new-password "YourNewSecureP@ss!"
```

Enable debug output with stack traces:

```bash
python rotate_admin_password.py --debug
```

### CLI Flags

| Flag | Description |
|---|---|
| `--new-password` | Provide a specific new password (min 12 characters); if omitted, a random one is generated |
| `--debug` | Enable debug output including exception stack traces |

### Expected Output

When generating a new password:

```
2024-01-15 10:30:00 - rotate_password - INFO - Starting PAN-OS Admin Password Rotation Tool
2024-01-15 10:30:00 - rotate_password - INFO - Establishing connection to PAN-OS firewall...
2024-01-15 10:30:01 - rotate_password - INFO - Successfully connected to firewall
2024-01-15 10:30:01 - rotate_password - INFO - Generated new password (length: 16)
2024-01-15 10:30:01 - rotate_password - WARNING - SAVE THIS PASSWORD BEFORE PROCEEDING!

==================================================
NEW PASSWORD GENERATED
==================================================
Password: aB3$xY7!mN9@pQ2&
==================================================
Please save this password securely!
==================================================

Have you saved the password? Type 'yes' to continue: yes
2024-01-15 10:30:10 - rotate_password - INFO - Rotating password for admin 'admin'...
2024-01-15 10:30:10 - rotate_password - INFO - Changing administrator password...
2024-01-15 10:30:11 - rotate_password - INFO - Password rotation succeeded.
```

The script requires typing `yes` to confirm before applying the change. It exits with code 0 on success, 1 on configuration errors, and 2 on PAN-OS API failures.

## Troubleshooting

| Issue | Possible Cause | Solution |
|---|---|---|
| Connection refused | Firewall unreachable or wrong hostname | Verify `PANOS_HOSTNAME` and network connectivity |
| Invalid Credential error | Wrong current password | Check `PANOS_PASSWORD` in `.env` matches the current admin password |
| `ModuleNotFoundError: No module named 'panos'` | Dependencies not installed | Run `pip install -r requirements.txt` in the virtual environment |
| SSL certificate verification failed | Self-signed cert on firewall | pan-os-python disables verification by default; check for proxy interference |
| Timeout connecting to firewall | Slow network or firewall under load | Verify firewall management interface is responsive |
| Password too short error | Provided password under 12 characters | Use `--new-password` with at least 12 characters |
