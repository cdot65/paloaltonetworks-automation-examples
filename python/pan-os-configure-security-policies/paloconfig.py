from typing import Dict, Any, List, Optional

from panos.errors import PanDeviceError
from panos.panorama import Panorama, DeviceGroup, PanoramaCommitAll, PanoramaCommit
from panos.policies import PreRulebase, SecurityRule

from utils import logger


class PaloConfig:
    """
    A class to manage the configuration of Palo Alto Networks Panorama.

    This class provides methods to interact with Panorama, including creating device groups,
    adding security rules, and committing changes to Panorama and device groups.

    Attributes:
        panorama (Panorama): The Panorama instance to interact with.
    """

    def __init__(
        self,
        panorama: Panorama,
    ):
        """
        Initialize the PaloConfig class with a Panorama object.

        Args:
            panorama (Panorama): The Panorama instance to interact with.
        """
        self.panorama: Panorama = panorama

    @staticmethod
    def _create_and_log_objects(
        device_group: DeviceGroup,
        object_type,
        object_name: str,
    ) -> None:
        """
        Find and create objects of a given type in a device group, and log the action.

        Args:
            device_group (DeviceGroup): The device group to search for objects.
            object_type: The type of objects to find and create.
            object_name (str): The name of the object type for logging purposes.

        Returns:
            None

        Logs:
            Information about the number of objects created or warnings if none found.
        """
        objects = device_group.findall(object_type)
        if objects:
            objects[0].create_similar()
            logger.info(f"Bulk created {len(objects)} {object_name}")
        else:
            logger.warning(
                f"No {object_name} found to create in {device_group.name} device group"
            )

    def commit_panorama(
        self,
        description=None,
        admins=None,
        device_groups=None,
    ):
        """
        Commit changes to Panorama with the given parameters.

        Args:
            description (str, optional): Description for the commit.
            admins (list[str], optional): List of admin usernames to include in the commit.
            device_groups (list[str], optional): List of device groups to include in the commit.

        Raises:
            PanDeviceError: If the commit operation fails.

        Returns:
            None

        Logs:
            Information about the success or failure of the commit operation.
        """
        try:
            commit_panorama = PanoramaCommit(
                description=description,
                admins=admins,
                device_groups=device_groups,
            )
            self.panorama.commit(cmd=commit_panorama)
            logger.info("Successfully committed changes to Panorama")
        except PanDeviceError as e:
            logger.error(f"Failed to commit changes to Panorama: {e}")
            raise

    def commit_all(
        self,
        style,
        name,
        description=None,
        admins=None,
        include_template=None,
        force_template_values=None,
        devices=None,
    ):
        """
        Commit changes across multiple device groups or templates.

        Args:
            style (str): The style of the commit (e.g., 'device group', 'template').
            name (str): The name of the device group or template.
            description (str, optional): Description for the commit.
            admins (list[str], optional): List of admin usernames to include in the commit.
            include_template (bool, optional): Whether to include templates in the commit.
            force_template_values (bool, optional): Force template values during commit.
            devices (list[str], optional): List of devices to include in the commit.

        Raises:
            PanDeviceError: If the commit-all operation fails.

        Returns:
            None

        Logs:
            Information about the success or failure of the commit-all operation.
        """
        try:
            commit_all = PanoramaCommitAll(
                style=style,
                name=name,
                description=description,
                admins=admins,
                include_template=include_template,
                force_template_values=force_template_values,
                devices=devices,
            )
            self.panorama.commit(cmd=commit_all)
            logger.info(f"Successfully committed changes to {style}: {name}")
        except PanDeviceError as e:
            logger.error(f"Failed to commit changes to {style} {name}: {e}")
            raise

    def create_device_group(
        self,
        name: str,
    ) -> Optional[DeviceGroup]:
        """
        Create a device group in Panorama.

        Args:
            name (str): The name of the device group to create.

        Returns:
            DeviceGroup: The created DeviceGroup object, or None if creation fails.

        Raises:
            PanDeviceError: If the device group creation fails.

        Logs:
            Information about the success or failure of the device group creation.
        """
        try:
            device_group = DeviceGroup(name)
            self.panorama.add(device_group)
            logger.info(
                f"Successfully attached {name} device group object to Panorama object"
            )
            return device_group
        except PanDeviceError as e:
            logger.error(f"Failed to create device group {name}: {e}")
            return None

    @staticmethod
    def security_rules(
        security_rule_configuration: List[Dict[str, Any]],
        device_group: DeviceGroup,
    ) -> None:
        """
        Configure security rules in a given device group.

        Args:
            security_rule_configuration (List[Dict[str, Any]]): List of security rule configurations.
            device_group (DeviceGroup): The device group to add the security rules to.

        Returns:
            None

        Logs:
            Information about the success or failure of adding security rules.

        Raises:
            PanDeviceError: If there is an error in creating security rules.
        """
        if not security_rule_configuration:
            logger.warning(
                f"No security rule configuration found for {device_group.name} device group"
            )
            return

        try:
            pre_rulebase = PreRulebase()
            device_group.add(pre_rulebase)

            for rule_config in security_rule_configuration:
                security_rule = SecurityRule(**rule_config)
                pre_rulebase.add(security_rule)

            security_rules = pre_rulebase.findall(SecurityRule)
            if security_rules:
                security_rules[0].create_similar()
                logger.info(
                    f"Created and added {len(security_rules)} security rules to the {device_group.name} device group using bulk operation"
                )
            else:
                logger.warning(
                    f"No security rules found to create in {device_group.name} device group"
                )
        except PanDeviceError as e:
            logger.error(f"Error creating security rules in {device_group.name}: {e}")
        except Exception as e:
            logger.error(
                f"Unexpected error creating security rules in {device_group.name}: {e}"
            )
