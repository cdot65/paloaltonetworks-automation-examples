from typing import Dict, Any, List, Optional

from panos.errors import PanDeviceError
from panos.panorama import Panorama, DeviceGroup, PanoramaCommitAll, PanoramaCommit
from panos.policies import PreRulebase, SecurityRule

from utils import logger


class PaloConfig:
    def __init__(
        self,
        panorama: Panorama,
    ):
        # Initialize the PaloConfig class with a Panorama object to interact with Panorama
        self.panorama: Panorama = panorama

    @staticmethod
    def _create_and_log_objects(
        device_group: DeviceGroup,
        object_type,
        object_name: str,
    ) -> None:
        # Find all objects of the given type in the device group
        objects = device_group.findall(object_type)
        if objects:
            # If objects are found, create similar ones in bulk
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
        try:
            # Create a PanoramaCommit object with the provided parameters
            commit_panorama = PanoramaCommit(
                description=description,
                admins=admins,
                device_groups=device_groups,
            )
            # Commit the changes to Panorama
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
        try:
            # Create a PanoramaCommitAll object to commit changes across multiple device groups or templates
            commit_all = PanoramaCommitAll(
                style=style,
                name=name,
                description=description,
                admins=admins,
                include_template=include_template,
                force_template_values=force_template_values,
                devices=devices,
            )
            # Commit the changes to all specified targets
            self.panorama.commit(cmd=commit_all)
            logger.info(f"Successfully committed changes to {style}: {name}")
        except PanDeviceError as e:
            logger.error(f"Failed to commit changes to {style} {name}: {e}")
            raise

    def create_device_group(
        self,
        name: str,
    ) -> Optional[DeviceGroup]:
        try:
            # Create a new DeviceGroup object with the specified name
            device_group = DeviceGroup(name)
            # Attach the device group to the Panorama object
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
        if not security_rule_configuration:
            # Log a warning if no security rule configuration is provided
            logger.warning(
                f"No security rule configuration found for {device_group.name} device group"
            )
            return

        try:
            # Create a PreRulebase object and add it to the device group
            pre_rulebase = PreRulebase()
            device_group.add(pre_rulebase)

            # Iterate through the provided security rule configurations
            for rule_config in security_rule_configuration:
                # Create a SecurityRule object with the given parameters
                security_rule = SecurityRule(
                    name=rule_config["name"],
                    fromzone=rule_config["fromzone"],
                    tozone=rule_config["tozone"],
                    source=rule_config["source"],
                    destination=rule_config["destination"],
                    application=rule_config["application"],
                    service=rule_config["service"],
                    action=rule_config["action"],
                    description=rule_config.get("description", ""),
                    tag=rule_config.get("tag", []),
                    disabled=rule_config.get("disabled", False),
                    log_setting=rule_config.get("log_setting"),
                    group=rule_config.get("group"),
                    category=rule_config.get("category"),
                )
                # Add the security rule to the PreRulebase
                pre_rulebase.add(security_rule)

            # Find all security rules in the PreRulebase and create similar ones in bulk if possible
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
