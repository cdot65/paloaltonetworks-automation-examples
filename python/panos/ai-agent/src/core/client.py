"""PAN-OS Firewall client management.

Singleton pattern for reusable firewall connection across tools and subgraphs.
"""

import logging
from typing import Optional

from panos.errors import PanDeviceError
from panos.firewall import Firewall
from src.core.config import get_settings

logger = logging.getLogger(__name__)

# Global singleton
_firewall_client: Optional[Firewall] = None


def get_firewall_client() -> Firewall:
    """Get or create PAN-OS firewall client singleton.

    Initializes connection using credentials from environment variables.
    Uses username/password authentication by default.

    Returns:
        Firewall: Connected pan-os-python Firewall instance

    Raises:
        PanDeviceError: If connection fails
    """
    global _firewall_client

    if _firewall_client is None:
        settings = get_settings()

        logger.info(f"Initializing PAN-OS connection to {settings.panos_hostname}")

        # Create firewall instance
        _firewall_client = Firewall(
            hostname=settings.panos_hostname,
            api_username=settings.panos_username,
            api_password=settings.panos_password,
        )

        # Test connection
        try:
            # Trigger API call to validate credentials
            _firewall_client.refresh_system_info()
            logger.info(
                f"Connected to PAN-OS {_firewall_client.version} "
                f"(serial: {_firewall_client.serial})"
            )
        except PanDeviceError as e:
            logger.error(f"Failed to connect to PAN-OS firewall: {e}")
            _firewall_client = None
            raise

    return _firewall_client


def reset_firewall_client() -> None:
    """Reset firewall client singleton.

    Useful for testing or reconnecting with different credentials.
    """
    global _firewall_client
    _firewall_client = None
    logger.info("Firewall client reset")


def test_connection() -> tuple[bool, str]:
    """Test PAN-OS firewall connection.

    Returns:
        Tuple of (success: bool, message: str)
    """
    try:
        fw = get_firewall_client()
        message = f"✅ Connected to PAN-OS {fw.version} (serial: {fw.serial})"
        return True, message
    except Exception as e:
        message = f"❌ Connection failed: {type(e).__name__}: {e}"
        return False, message
