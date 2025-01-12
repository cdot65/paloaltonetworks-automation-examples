#!/usr/bin/env python3

"""
IP Tag Manager - A script to manage IP address tags on PAN-OS devices
using the pan-os-python SDK.
"""

import argparse
import logging
import sys
from typing import Dict, List, Optional

from panos.base import PanDevice
from panos.errors import PanDeviceError
from panos.panorama import Panorama

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class IPTagManager:
    """Manages IP address tags on PAN-OS devices."""

    def __init__(
        self,
        hostname: str,
        username: str,
        password: str,
        vsys: str = None,
    ):
        """Initialize the IP Tag Manager.

        Args:
            hostname: Firewall/Panorama hostname or IP
            username: Username for authentication
            password: Password for authentication
            vsys: Virtual system (default: vsys1)
        """
        self.hostname = hostname
        self.username = username
        self.password = password
        self.vsys = vsys
        self.device = None

    def connect(self) -> None:
        """Establish connection to the device."""
        try:
            self.device = PanDevice.create_from_device(
                self.hostname,
                self.username,
                self.password,
            )

            if type(self.device) == Panorama:
                print("Connected to a Panorama appliance.")
            else:
                print("Connected to a firewall appliance. Setting vsys...")
                self.device.vsys = self.vsys
            logger.info(f"Successfully connected to {self.hostname}")
        except PanDeviceError as e:
            logger.error(f"Failed to connect to device: {e}")
            sys.exit(1)

    def get_all_registered_ips(self) -> Dict[str, List[str]]:
        """Retrieve all registered IP addresses and their tags.

        Returns:
            Dict mapping IP addresses to lists of tags
        """
        try:
            registered_ips = self.device.userid.get_registered_ip()
            logger.info(f"Retrieved {len(registered_ips)} registered IP addresses")
            return registered_ips
        except PanDeviceError as e:
            logger.error(f"Failed to get registered IPs: {e}")
            return {}

    def register_ip_tags(
        self,
        ip: str,
        tags: List[str],
        timeout: Optional[int] = None,
    ) -> None:
        """Register tags for an IP address.

        Args:
            ip: IP address to tag
            tags: List of tags to apply
            timeout: Optional timeout in seconds
        """
        try:
            self.device.userid.register(
                ip,
                tags,
                timeout,
            )
            logger.info(f"Successfully registered tags {tags} for IP {ip}")
        except PanDeviceError as e:
            logger.error(f"Failed to register tags for IP {ip}: {e}")

    def unregister_ip_tags(
        self,
        ip: str,
        tags: List[str],
    ) -> None:
        """Remove tags from an IP address.

        Args:
            ip: IP address to untag
            tags: List of tags to remove
        """
        try:
            self.device.userid.unregister(
                ip,
                tags,
            )
            logger.info(f"Successfully unregistered tags {tags} for IP {ip}")
        except PanDeviceError as e:
            logger.error(f"Failed to unregister tags for IP {ip}: {e}")

    def clear_all_ip_tags(self) -> None:
        """Remove all IP tags from the device."""
        try:
            self.device.userid.clear_registered_ip()
            logger.info("Successfully cleared all IP tags")
        except PanDeviceError as e:
            logger.error(f"Failed to clear IP tags: {e}")

    def audit_ip_tags(
        self,
        ip_tags_map: Dict[str, List[str]],
        timeout: Optional[int] = None,
    ) -> None:
        """Synchronize IP tags to match the provided mapping.

        Args:
            ip_tags_map: Dict mapping IP addresses to desired tags
            timeout: Optional timeout in seconds
        """
        try:
            self.device.userid.audit_registered_ip(
                ip_tags_map,
                timeout,
            )
            logger.info("Successfully audited IP tags")
        except PanDeviceError as e:
            logger.error(f"Failed to audit IP tags: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Manage IP tags on PAN-OS devices",
    )
    parser.add_argument(
        "--host",
        required=True,
        help="Firewall/Panorama hostname or IP",
    )
    parser.add_argument(
        "--username",
        required=True,
        help="Username for authentication",
    )
    parser.add_argument(
        "--password",
        required=True,
        help="Password for authentication",
    )
    parser.add_argument(
        "--vsys",
        default="vsys1",
        help="Virtual system (default: vsys1)",
    )

    # Add subparsers for different operations
    subparsers = parser.add_subparsers(
        dest="command",
        help="Command to execute",
    )

    # List command
    subparsers.add_parser(
        "list",
        help="List all registered IP tags",
    )

    # Register command
    register_parser = subparsers.add_parser(
        "register",
        help="Register tags for an IP",
    )
    register_parser.add_argument(
        "ip",
        help="IP address to tag",
    )
    register_parser.add_argument(
        "tags",
        help="Comma-separated list of tags",
    )
    register_parser.add_argument(
        "--timeout",
        type=int,
        help="Tag timeout in seconds",
    )

    # Unregister command
    unregister_parser = subparsers.add_parser(
        "unregister",
        help="Remove tags from an IP",
    )
    unregister_parser.add_argument(
        "ip",
        help="IP address to untag",
    )
    unregister_parser.add_argument(
        "tags",
        help="Comma-separated list of tags to remove",
    )

    # Clear command
    subparsers.add_parser(
        "clear",
        help="Clear all IP tags",
    )

    args = parser.parse_args()

    # Initialize and connect to device
    manager = IPTagManager(
        args.host,
        args.username,
        args.password,
        args.vsys,
    )
    manager.connect()

    # Execute requested command
    if args.command == "list":
        registered_ips = manager.get_all_registered_ips()
        for ip, tags in registered_ips.items():
            print(f"{ip}: {', '.join(tags)}")

    elif args.command == "register":
        tags = [tag.strip() for tag in args.tags.split(",")]
        manager.register_ip_tags(args.ip, tags, args.timeout)

    elif args.command == "unregister":
        tags = [tag.strip() for tag in args.tags.split(",")]
        manager.unregister_ip_tags(args.ip, tags)

    elif args.command == "clear":
        manager.clear_all_ip_tags()


if __name__ == "__main__":
    main()
