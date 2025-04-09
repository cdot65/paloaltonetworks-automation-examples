"""
PAN-OS client module for interacting with Panorama.

This module provides a high-level interface for interacting with Palo Alto Networks
Panorama appliances. It encapsulates common operations like connecting to Panorama,
managing address objects, and handling commits.
"""

from typing import Any, Dict, List, Optional

from models import AddressObject
from panos.errors import PanDeviceError
from panos.objects import AddressObject as PanAddressObject
from panos.panorama import DeviceGroup, Panorama, PanoramaCommit, PanoramaCommitAll
from utils import logger


class PanosClient:
    """Client for interacting with PAN-OS devices through Panorama.

    This class provides methods for managing PAN-OS configurations through Panorama,
    including address object management and commit operations.

    Attributes:
        panorama (Panorama): The connected Panorama instance.
    """

    def __init__(self, panorama: Panorama):
        """
        Initialize the PAN-OS client.

        Args:
            panorama (Panorama): A connected Panorama instance.
        """
        self.panorama = panorama

    @classmethod
    def connect(cls, hostname: str, api_key: str) -> "PanosClient":
        """
        Create a new PanosClient instance and connect to Panorama.

        Args:
            hostname (str): Hostname or IP address of the Panorama appliance.
            api_key (str): API key for authentication.

        Returns:
            PanosClient: A new client instance connected to Panorama.

        Raises:
            PanDeviceError: If connection fails.
        """
        try:
            # Create and connect to Panorama
            panorama = Panorama(hostname=hostname, api_key=api_key)
            panorama.refresh_system_info()
            logger.info("Successfully connected to Panorama: %s", hostname)
            return cls(panorama)
        except PanDeviceError as e:
            logger.error("Failed to connect to Panorama: %s", e)
            raise

    def get_or_create_device_group(self, name: str) -> Optional[DeviceGroup]:
        """
        Get an existing device group or create a new one.

        Args:
            name (str): Name of the device group.

        Returns:
            Optional[DeviceGroup]: The device group instance if successful, None otherwise.

        Raises:
            PanDeviceError: If device group creation fails.
        """
        try:
            # Check if device group exists
            device_group = DeviceGroup(name=name)
            device_group.create_refresh()

            # Add to Panorama if it doesn't exist
            if device_group.id is None:
                logger.info("Creating device group: %s", name)
                self.panorama.add(device_group)
                device_group.create()
            else:
                logger.info("Found existing device group: %s", name)

            return device_group
        except PanDeviceError as e:
            logger.error("Failed to get/create device group: %s", e)
            return None

    def create_address_object(
        self, device_group: DeviceGroup, address_object: AddressObject
    ) -> bool:
        """
        Create a new address object in the specified device group.

        Args:
            device_group (DeviceGroup): The device group to create the object in.
            address_object (AddressObject): The address object configuration.

        Returns:
            bool: True if creation was successful, False otherwise.
        """
        try:
            # Create PAN-OS address object
            pan_addr = PanAddressObject(
                name=address_object.name,
                value=str(address_object.value),
                type="ip-netmask",
                description=address_object.description,
                tag=address_object.tags,
            )

            # Add to device group and create
            device_group.add(pan_addr)
            pan_addr.create()
            logger.info("Created address object: %s", address_object.name)
            return True
        except PanDeviceError as e:
            logger.error("Failed to create address object: %s", e)
            return False

    def commit_to_panorama(
        self,
        description: Optional[str] = None,
        admins: Optional[List[str]] = None,
        device_groups: Optional[List[str]] = None,
    ) -> bool:
        """
        Commit changes to Panorama.

        Args:
            description (Optional[str]): Commit description.
            admins (Optional[List[str]]): List of admin names to commit changes for.
            device_groups (Optional[List[str]]): List of device groups to commit changes for.

        Returns:
            bool: True if commit was successful, False otherwise.
        """
        try:
            cmd = PanoramaCommit(
                description=description,
                admins=admins,
                device_groups=device_groups,
            )
            result: Dict[str, Any] = self.panorama.commit(cmd=cmd)
            logger.info("Commit to Panorama successful")
            return result.get("result") == "OK"
        except PanDeviceError as e:
            logger.error("Failed to commit to Panorama: %s", e)
            return False

    def commit_all(
        self,
        device_group_name: str,
        description: Optional[str] = None,
        admins: Optional[List[str]] = None,
        include_template: bool = True,
    ) -> bool:
        """
        Perform a commit-all operation to push changes to firewalls.

        Args:
            device_group_name (str): Name of the device group to commit.
            description (Optional[str]): Commit description.
            admins (Optional[List[str]]): List of admin names to commit changes for.
            include_template (bool): Whether to include template changes.

        Returns:
            bool: True if commit was successful, False otherwise.
        """
        try:
            cmd = PanoramaCommitAll(
                description=description,
                admins=admins,
                device_groups=[device_group_name],
                include_template=include_template,
            )
            result: Dict[str, Any] = self.panorama.commit_all(cmd=cmd)
            logger.info("Commit-all successful for device group: %s", device_group_name)
            return result.get("result") == "OK"
        except PanDeviceError as e:
            logger.error("Failed to commit-all: %s", e)
            return False
