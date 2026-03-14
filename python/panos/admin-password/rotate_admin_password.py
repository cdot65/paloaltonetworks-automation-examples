#!/usr/bin/env python3
"""Simple PAN-OS admin password rotation script.

Usage:
    1. Populate environment variables (directly or via a `.env` file):
       - PANOS_HOSTNAME  (e.g. fw01.example.com)
       - PANOS_USERNAME  (admin user to authenticate with)
       - PANOS_PASSWORD  (current password for the user)
    2. Run the script:
       $ python rotate_admin_password.py

The script prints the newly generated password to stdout on success and exits
non-zero on failure.
"""

from __future__ import annotations

import os
import secrets
import string
import sys
import argparse
import logging
from typing import Final

from dotenv import load_dotenv
from panos.device import Administrator
from panos.errors import PanDeviceError
from panos.firewall import Firewall

# ---------------------------------------------------------------------------
# Configuration helpers
# ---------------------------------------------------------------------------

PASSWORD_LENGTH: Final[int] = 16
CHARSET: Final[str] = (
    string.ascii_uppercase
    + string.ascii_lowercase
    + string.digits
    + "!@#$%^&*()_+-=[]{}|;:,.<>?"
)


def generate_password(length: int = PASSWORD_LENGTH) -> str:
    """Generate a cryptographically secure random password."""
    if length < 12:
        raise ValueError(
            "Password length must be at least 12 characters for basic security."
        )
    return "".join(secrets.choice(CHARSET) for _ in range(length))


# ---------------------------------------------------------------------------
# Main rotation logic
# ---------------------------------------------------------------------------


def rotate_password() -> None:
    """Rotate the admin password on a PAN-OS firewall using pan-os-python."""

    # Configure logging once at runtime
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )
    logger = logging.getLogger("rotate_password")

    logger.info("Starting PAN-OS Admin Password Rotation Tool")

    # Load variables from .env if present
    load_dotenv()

    hostname = os.getenv("PANOS_HOSTNAME")
    username = os.getenv("PANOS_USERNAME")
    current_password = os.getenv("PANOS_PASSWORD")

    if not hostname or not username or not current_password:
        logger.error(
            "Error: PANOS_HOSTNAME, PANOS_USERNAME, and PANOS_PASSWORD must be set as environment variables."
        )
        sys.exit(1)

    # -------------------------------------------------------------------
    # Determine new password: use CLI value or generate and confirm
    # -------------------------------------------------------------------

    parser = argparse.ArgumentParser(description="Rotate PAN-OS admin password")
    parser.add_argument(
        "--new-password",
        dest="cli_password",
        help="Provide a new password; if omitted, a random secure password is generated.",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug output including stack traces.",
    )
    args = parser.parse_args()

    show_trace = args.debug

    if args.cli_password:
        new_password: str | None = args.cli_password
        if len(new_password) < 12:
            logger.error("Provided password must be at least 12 characters.")
            sys.exit(1)
    else:
        new_password = None  # Will be generated after establishing connection

    logger.info("Establishing connection to PAN-OS firewall…")

    try:
        fw = Firewall(hostname, username, current_password)
        logger.info("Successfully connected to firewall")

        # Handle password generation/confirmation if needed
        if new_password is None:
            new_password = generate_password()
            logger.info("Generated new password (length: %d)", len(new_password))
            logger.warning("SAVE THIS PASSWORD BEFORE PROCEEDING!")

            # Stylized block for user visibility
            print("\n" + "=" * 50)
            print("NEW PASSWORD GENERATED")
            print("=" * 50)
            print(f"Password: {new_password}")
            print("=" * 50)
            print("Please save this password securely!")
            print("=" * 50 + "\n")

            confirm = (
                input("Have you saved the password? Type 'yes' to continue: ")
                .strip()
                .lower()
            )
            if confirm != "yes":
                logger.info("Aborting password rotation at user request.")
                sys.exit(0)

        logger.info("Rotating password for admin '%s'…", username)

        # Locate the administrator account and update its password
        admin_user = Administrator(name=username)
        fw.add(admin_user)
        try:
            admin_user.refresh()  # Retrieve existing admin details (noop if not present)
        except PanDeviceError:
            # If refresh fails, we proceed assuming the admin exists; failure will be caught on change_password.
            pass

        logger.info("Changing administrator password…")
        admin_user.change_password(new_password)

        logger.info("Password rotation succeeded.")
        sys.exit(0)

    except PanDeviceError as err:
        logger.error("Password rotation failed: %s", err)
        if "Invalid Credential" in str(err):
            logger.error(
                "The supplied current credentials are invalid. Check PANOS_PASSWORD in your .env."
            )
        else:
            logger.error("The password may have been partially changed.")
            logger.error(
                "Try updating your .env file with the new password shown above."
            )
        if show_trace:
            logger.exception("Exception details")
        sys.exit(2)


if __name__ == "__main__":
    rotate_password()
