"""
PAN-OS client module for interacting with Panorama.

This module provides a high-level interface for interacting with Palo Alto Networks
Panorama appliances. It encapsulates common operations like connecting to Panorama,
managing address objects, and handling commits.
"""

from typing import Any, Dict, List, Optional

from models import AddressObject
from panos.errors import PanDeviceError, PanXapiError
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
        Connect to Panorama and return a PanosClient instance.

        Args:
            hostname: The hostname or IP address of the Panorama instance
            api_key: The API key for authentication

        Returns:
            PanosClient: A connected PanosClient instance

        Raises:
            PanDeviceError: If connection fails
        """
        panorama = Panorama(hostname=hostname, api_key=api_key)
        panorama.refresh_system_info()

        # Refresh device groups to ensure we have the current state
        device_groups = DeviceGroup.refreshall(panorama)
        logger.info("Found %d device groups on Panorama", len(device_groups))

        return cls(panorama)

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
            existing = self.panorama.find(name, DeviceGroup)
            if existing:
                logger.info("Found existing device group: %s", name)
                return existing

            # Create new device group
            logger.info("Creating device group: %s", name)
            device_group = DeviceGroup(name=name)
            try:
                self.panorama.add(device_group)
                device_group.create()
                return device_group
            except PanXapiError as e:
                logger.error("Failed to create device group: %s", e)
                return None

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
            bool: True if successful, False otherwise.
        """
        try:
            # Convert to PAN-OS address object
            pan_addr_obj = PanAddressObject(
                name=address_object.name,
                value=str(address_object.value),
                type="ip-netmask",
                description=address_object.description,
                tag=address_object.tags,
            )

            # Add to device group and create
            device_group.add(pan_addr_obj)
            pan_addr_obj.create()
            logger.info("Created address object: %s", address_object.name)
            return True

        except (PanDeviceError, PanXapiError) as e:
            logger.error("Failed to create address object: %s", e)
            return False

    def commit_to_panorama(self) -> bool:
        """
        Commit changes to Panorama.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            logger.info("Initiating commit to Panorama...")
            commit_panorama = PanoramaCommit(
                description="Commit address object changes",
                exclude_device_and_network=False,
                exclude_shared_objects=False,
            )
            self.panorama.commit(cmd=commit_panorama)
            logger.info("Successfully committed changes to Panorama")
            return True
        except (PanDeviceError, PanXapiError) as e:
            logger.error("Failed to commit to Panorama: %s", e)
            return False

    def commit_all(self, device_groups: Optional[List[str]] = None) -> bool:
        """
        Push changes to all or specified device groups.

        Args:
            device_groups (Optional[List[str]]): List of device group names.
                If None, commits to all device groups.

        Returns:
            bool: True if successful, False otherwise.
        """
        if not device_groups:
            logger.warning("No device groups specified for commit-all")
            return False

        try:
            for dg in device_groups:
                logger.info("Initiating commit-all to device group: %s", dg)
                commit_all = PanoramaCommitAll(
                    style="device group",
                    name=dg,
                    description="Push address object changes",
                    include_template=True,
                )
                self.panorama.commit(cmd=commit_all)
                logger.info("Successfully initiated commit-all to device group: %s", dg)
            return True
        except (PanDeviceError, PanXapiError) as e:
            logger.error("Failed to commit-all: %s", e)
            return False

    def _check_commit_result(self, result: Dict[str, Any]) -> bool:
        """
        Check if a commit was successful.

        Args:
            result (Dict[str, Any]): Commit result from PAN-OS.

        Returns:
            bool: True if successful, False otherwise.
        """
        if isinstance(result, str):
            return result.lower() == "ok"

        if isinstance(result, int):
            logger.info("Commit job ID: %d", result)
            try:
                # Wait for the job to complete and get the final result
                logger.debug("Checking job status...")
                job_result = self.panorama.syncjob(result, sync=True)
                logger.debug("Raw job result: %s", job_result)

                # Handle different job result formats
                if isinstance(job_result, dict):
                    status = job_result.get("status")
                    logger.debug("Job status: %s", status)
                    if status == "FIN":
                        # Check the details for success
                        details = job_result.get("details", {})
                        logger.debug("Job details: %s", details)
                        if details.get("status") == "PASS":
                            logger.info("Commit completed successfully")
                            return True
                        else:
                            logger.error("Commit failed: %s", details.get("status"))
                            return False
                    else:
                        logger.error("Job did not finish successfully: %s", status)
                        return False
                else:
                    logger.error("Job result is not a dictionary: %s", type(job_result))
                return False
            except (PanDeviceError, PanXapiError) as e:
                logger.error("Failed to check job status: %s", e)
                return False

        if not isinstance(result, dict):
            logger.error("Invalid commit result type: %s", type(result))
            return False

        job_result = result.get("result")
        if not job_result:
            logger.error("No result in commit response")
            return False

        if isinstance(job_result, str):
            return job_result.lower() == "ok"

        return False
