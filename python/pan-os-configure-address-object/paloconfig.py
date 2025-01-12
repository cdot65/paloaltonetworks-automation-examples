from typing import Dict, Any, List, Optional

from panos.errors import PanDeviceError, PanObjectMissing, PanDeviceXapiError
from panos.objects import (
    Tag,
    AddressObject,
    AddressGroup,
    ApplicationContainer,
    ApplicationObject,
    ApplicationTag,
    ServiceObject,
    ServiceGroup,
)
from panos.panorama import Panorama, DeviceGroup, PanoramaCommitAll, PanoramaCommit

from utils import logger


class PaloConfig:
    def __init__(
        self,
        panorama: Panorama,
    ):
        """
        Initialize a new instance with a Panorama object.

        This method sets up the instance with a reference to a Panorama object,
        which likely represents a Palo Alto Networks Panorama management system.

        Attributes:
            panorama (Panorama): An instance of the Panorama class representing
                                 the Panorama management system.
        """
        self.panorama: Panorama = panorama

    @staticmethod
    def _create_and_log_objects(
        device_group: DeviceGroup,
        object_type,
        object_name: str,
    ) -> None:
        """
        Create and log objects of a specified type within a device group.

        Finds objects of the given type in the device group, creates similar objects,
        and logs the results. If no objects are found, a warning is logged.

        Attributes:
            device_group (DeviceGroup): The device group to search for objects.
            object_type: The type of object to create and log.
            object_name (str): The name of the object type for logging purposes.

        Error:
            None explicitly raised, but logging warnings may occur.

        Return:
            None
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
        Perform a commit operation on Panorama using PanoramaCommit.

        Args:
            description (str, optional): The commit message
            admins (list, optional): List of admins whose changes are to be committed
            device_groups (list, optional): List of device groups to save changes for

        Raises:
            PanDeviceError: If the commit operation fails
        """
        try:
            commit_panorama = PanoramaCommit(
                description=description,
                admins=admins,
                device_groups=device_groups,
            )
            self.panorama.commit(cmd=commit_panorama)  # type: ignore[<lint-error-code>]
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
        Perform a commit-all operation on Panorama using PanoramaCommitAll.

        Args:
            style (str): The type of commit-all to perform (e.g., "device group", "template", etc.)
            name (str): The name of the location to push the config to
            description (str, optional): The commit message
            admins (list[str], optional): The list of admins to push the config to
            include_template (bool, optional): Include template changes (for device group commits)
            force_template_values (bool, optional): Force template values
            devices (list, optional): Specific devices to commit to

        Raises:
            PanDeviceError: If the commit operation fails
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
            self.panorama.commit(cmd=commit_all)  # type: ignore[<lint-error-code>]
            logger.info(f"Successfully committed changes to {style}: {name}")
        except PanDeviceError as e:
            logger.error(f"Failed to commit changes to {style} {name}: {e}")
            raise

    def create_device_group(
        self,
        name: str,
    ) -> Optional[DeviceGroup]:
        """
        Creates a device group in Panorama and attaches it to the Panorama object.

        Attempts to create a DeviceGroup with the given name and add it to the Panorama object.
        Logs the result of the operation.

        Attributes:
            name (str): The name of the device group to be created.

        Error:
            PanDeviceError: If the device group creation fails.

        Return:
            DeviceGroup or None: The created DeviceGroup object if successful, None otherwise.
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
    def application_objects(
        application_object_configuration: List[Dict[str, Any]],
        device_group: DeviceGroup,
    ) -> None:
        if not application_object_configuration:
            logger.warning(
                f"No application object configuration found for {device_group.name} device group"
            )
            return

        try:
            for app_obj_config in application_object_configuration:
                app_obj = ApplicationObject(
                    name=app_obj_config["name"],
                    category=app_obj_config["category"],
                    subcategory=app_obj_config["subcategory"],
                    technology=app_obj_config["technology"],
                    risk=app_obj_config["risk"],
                    default_type=app_obj_config["default_type"],
                    default_port=app_obj_config["default_port"],
                    # Add other optional parameters as needed
                    description=app_obj_config.get("description", ""),
                    default_ip_protocol=app_obj_config.get("default_ip_protocol"),
                    default_icmp_type=app_obj_config.get("default_icmp_type"),
                    default_icmp_code=app_obj_config.get("default_icmp_code"),
                    parent_app=app_obj_config.get("parent_app"),
                    timeout=app_obj_config.get("timeout"),
                    tcp_timeout=app_obj_config.get("tcp_timeout"),
                    udp_timeout=app_obj_config.get("udp_timeout"),
                    tcp_half_closed_timeout=app_obj_config.get(
                        "tcp_half_closed_timeout"
                    ),
                    tcp_time_wait_timeout=app_obj_config.get("tcp_time_wait_timeout"),
                    evasive_behavior=app_obj_config.get("evasive_behavior"),
                    consume_big_bandwidth=app_obj_config.get("consume_big_bandwidth"),
                    used_by_malware=app_obj_config.get("used_by_malware"),
                    able_to_transfer_file=app_obj_config.get("able_to_transfer_file"),
                    has_known_vulnerability=app_obj_config.get(
                        "has_known_vulnerability"
                    ),
                    tunnel_other_application=app_obj_config.get(
                        "tunnel_other_application"
                    ),
                    tunnel_applications=app_obj_config.get("tunnel_applications"),
                    prone_to_misuse=app_obj_config.get("prone_to_misuse"),
                    pervasive_use=app_obj_config.get("pervasive_use"),
                    file_type_ident=app_obj_config.get("file_type_ident"),
                    virus_ident=app_obj_config.get("virus_ident"),
                    data_ident=app_obj_config.get("data_ident"),
                )
                device_group.add(app_obj)

            application_objects = device_group.findall(ApplicationObject)
            if application_objects:
                application_objects[0].create_similar()
                logger.info(
                    f"Created and added {len(application_objects)} application objects to the {device_group.name} device "
                    f"group using bulk operation"
                )
            else:
                logger.warning(
                    f"No application objects found to create in {device_group.name} device group"
                )
        except PanObjectMissing as e:
            logger.error(
                f"Error creating application objects in {device_group.name}: {e}"
            )
        except PanDeviceXapiError as e:
            logger.error(
                f"API error while creating application objects in {device_group.name}: {e}"
            )
        except Exception as e:
            logger.error(
                f"Unexpected error creating application objects in {device_group.name}: {e}"
            )

    @staticmethod
    def application_tags(
        application_tag_configuration: List[Dict[str, Any]],
        device_group: DeviceGroup,
    ) -> None:
        if not application_tag_configuration:
            logger.warning(
                f"No application tag configuration found for {device_group.name} device group"
            )
            return

        try:
            for app_tag_config in application_tag_configuration:
                app_tag = ApplicationTag(
                    name=app_tag_config["name"],
                    tags=app_tag_config["tags"],
                )
                device_group.add(app_tag)

            application_tags = device_group.findall(ApplicationTag)
            if application_tags:
                application_tags[0].create_similar()
                logger.info(
                    f"Created and added {len(application_tags)} application tags to the {device_group.name} device "
                    f"group using bulk operation"
                )
            else:
                logger.warning(
                    f"No application tags found to create in {device_group.name} device group"
                )
        except PanObjectMissing as e:
            logger.error(f"Error creating application tags in {device_group.name}: {e}")
        except PanDeviceXapiError as e:
            logger.error(
                f"API error while creating application tags in {device_group.name}: {e}"
            )
        except Exception as e:
            logger.error(
                f"Unexpected error creating application tags in {device_group.name}: {e}"
            )

    @staticmethod
    def address_objects(
        address_object_configuration: List[Dict[str, Any]],
        device_group: DeviceGroup,
    ) -> None:
        """
        Creates and adds address objects to a device group.

        Iterates through address object configurations, creates AddressObject instances,
        and adds them to the specified device group. Performs bulk creation if possible.

        Attributes:
            address_object_configuration (List[Dict[str, Any]]): List of address object configurations.
            device_group (DeviceGroup): The device group to add address objects to.

        Errors:
            PanObjectMissing: Error creating address objects.
            PanDeviceXapiError: API error while creating address objects.
            Exception: Unexpected error during address object creation.

        Return:
            None
        """

        if not address_object_configuration:
            logger.warning(
                f"No address object configuration found for {device_group.name} device group"
            )
            return

        try:
            for addr_obj_config in address_object_configuration:
                addr_obj = AddressObject(
                    name=addr_obj_config["name"],
                    value=addr_obj_config["value"],
                    type=addr_obj_config["type"],
                    description=addr_obj_config.get("description", ""),
                    tag=addr_obj_config.get("tag", []),
                )
                device_group.add(addr_obj)

            address_objects = device_group.findall(AddressObject)
            if address_objects:
                address_objects[0].create_similar()
                logger.info(
                    f"Created and added {len(address_objects)} address objects to the {device_group.name} device "
                    f"group using bulk operation"
                )
            else:
                logger.warning(
                    f"No address objects found to create in {device_group.name} device group"
                )
        except PanObjectMissing as e:
            logger.error(f"Error creating address objects in {device_group.name}: {e}")
        except PanDeviceXapiError as e:
            logger.error(
                f"API error while creating address objects in {device_group.name}: {e}"
            )
        except Exception as e:
            logger.error(
                f"Unexpected error creating address objects in {device_group.name}: {e}"
            )

    @staticmethod
    def address_groups(
        address_groups_configuration: List[Dict[str, Any]],
        device_group: DeviceGroup,
    ) -> None:
        """
        Creates and adds address groups to a device group based on the given configuration.

        Iterates through the address groups configuration, creates AddressGroup objects,
        and adds them to the specified device group. Uses bulk operation for efficiency.

        Attributes:
            address_groups_configuration (List[Dict[str, Any]]): List of address group configurations.
            device_group (DeviceGroup): The device group to add address groups to.

        Errors:
            PanObjectMissing: Error when creating address groups.
            PanDeviceXapiError: API error while creating address groups.
            Exception: Unexpected error during address group creation.

        Return:
            None
        """

        if not address_groups_configuration:
            logger.warning(
                f"No address group configuration found for {device_group.name} device group"
            )
            return

        try:
            for group_config in address_groups_configuration:
                addr_group = AddressGroup(
                    name=group_config["name"],
                    static_value=group_config.get("static_value", []),
                    description=group_config.get("description", ""),
                )
                device_group.add(addr_group)

            address_groups = device_group.findall(AddressGroup)
            if address_groups:
                address_groups[0].create_similar()
                logger.info(
                    f"Created and added {len(address_groups)} address groups to the {device_group.name} device group "
                    f"using bulk operation"
                )
            else:
                logger.warning(
                    f"No address groups found to create in {device_group.name} device group"
                )
        except PanObjectMissing as e:
            logger.error(f"Error creating address groups in {device_group.name}: {e}")
        except PanDeviceXapiError as e:
            logger.error(
                f"API error while creating address groups in {device_group.name}: {e}"
            )
        except Exception as e:
            logger.error(
                f"Unexpected error creating address groups in {device_group.name}: {e}"
            )

    @staticmethod
    def application_containers(
        application_container_configuration: List[Dict[str, Any]],
        device_group: DeviceGroup,
    ) -> None:
        """
        Create and add ApplicationContainer objects to a specified device group.

        Iterates through the provided configuration to create ApplicationContainer objects
        and adds them to the given device group. Handles bulk creation and logs the process.

        Attributes:
            application_container_configuration (List[Dict[str, Any]]): List of container configs.
            device_group (DeviceGroup): Target device group for container addition.

        Error:
            PanObjectMissing: When required objects are missing.
            PanDeviceXapiError: When API errors occur during container creation.

        Return:
            None
        """

        if not application_container_configuration:
            logger.warning(
                f"No application container configuration found for {device_group.name} device group"
            )
            return

        try:
            for container_config in application_container_configuration:
                app_container = ApplicationContainer(
                    name=container_config["name"],
                    applications=container_config.get("applications", []),
                )
                device_group.add(app_container)

            app_containers = device_group.findall(ApplicationContainer)
            if app_containers:
                app_containers[0].create_similar()
                logger.info(
                    f"Created and added {len(app_containers)} application containers to the {device_group.name} "
                    f"device group using bulk operation"
                )
            else:
                logger.warning(
                    f"No application containers found to create in {device_group.name} device group"
                )
        except PanObjectMissing as e:
            logger.error(
                f"Error creating application containers in {device_group.name}: {e}"
            )
        except PanDeviceXapiError as e:
            logger.error(
                f"API error while creating application containers in {device_group.name}: {e}"
            )
        except Exception as e:
            logger.error(
                f"Unexpected error creating application containers in {device_group.name}: {e}"
            )

    @staticmethod
    def service_objects(
        service_object_configuration: List[Dict[str, Any]], device_group: DeviceGroup
    ) -> None:
        """
        Create and add service objects to a device group.

        Processes a list of service object configurations, creates ServiceObject instances,
        and adds them to the specified device group. Uses bulk operation for efficiency.

        Attributes:
            service_object_configuration (List[Dict[str, Any]]): List of service object configurations.
            device_group (DeviceGroup): The device group to add service objects to.

        Error:
            PanObjectMissing: Error creating service objects.
            PanDeviceXapiError: API error while creating service objects.
            Exception: Unexpected error during service object creation.

        Return:
            None
        """
        if not service_object_configuration:
            logger.warning(
                f"No service object configuration found for {device_group.name} device group"
            )
            return

        try:
            for service_obj_config in service_object_configuration:
                service_obj = ServiceObject(
                    name=service_obj_config["name"],
                    protocol=service_obj_config["protocol"],
                    destination_port=service_obj_config["destination_port"],
                    description=service_obj_config.get("description", ""),
                    tag=service_obj_config.get("tag", []),
                    source_port=service_obj_config.get("source_port"),
                    enable_override_timeout=service_obj_config.get(
                        "enable_override_timeout", "no"
                    ),
                    override_timeout=service_obj_config.get("override_timeout"),
                    override_half_close_timeout=service_obj_config.get(
                        "override_half_close_timeout"
                    ),
                    override_time_wait_timeout=service_obj_config.get(
                        "override_time_wait_timeout"
                    ),
                )
                device_group.add(service_obj)

            service_objects = device_group.findall(ServiceObject)
            if service_objects:
                service_objects[0].create_similar()
                logger.info(
                    f"Created and added {len(service_objects)} service objects to the {device_group.name} device "
                    f"group using bulk operation"
                )
            else:
                logger.warning(
                    f"No service objects found to create in {device_group.name} device group"
                )
        except PanObjectMissing as e:
            logger.error(f"Error creating service objects in {device_group.name}: {e}")
        except PanDeviceXapiError as e:
            logger.error(
                f"API error while creating service objects in {device_group.name}: {e}"
            )
        except Exception as e:
            logger.error(
                f"Unexpected error creating service objects in {device_group.name}: {e}"
            )

    @staticmethod
    def service_groups(
        service_group_configuration: List[Dict[str, Any]],
        device_group: DeviceGroup,
    ) -> None:
        if not service_group_configuration:
            logger.warning(
                f"No service group configuration found for {device_group.name} device group"
            )
            return

        try:
            for service_group_config in service_group_configuration:
                service_group = ServiceGroup(
                    name=service_group_config["name"],
                    value=service_group_config["value"],
                    tag=service_group_config.get("tag", []),
                )
                device_group.add(service_group)

            service_groups = device_group.findall(ServiceGroup)
            if service_groups:
                service_groups[0].create_similar()
                logger.info(
                    f"Created and added {len(service_groups)} service groups to the {device_group.name} device "
                    f"group using bulk operation"
                )
            else:
                logger.warning(
                    f"No service groups found to create in {device_group.name} device group"
                )
        except PanObjectMissing as e:
            logger.error(f"Error creating service groups in {device_group.name}: {e}")
        except PanDeviceXapiError as e:
            logger.error(
                f"API error while creating service groups in {device_group.name}: {e}"
            )
        except Exception as e:
            logger.error(
                f"Unexpected error creating service groups in {device_group.name}: {e}"
            )

    def bulk_create_resources(
        self,
        device_group: DeviceGroup,
    ) -> None:
        """
        Bulk create resources for a given device group.

        Creates tags, address objects, and address groups for the specified device group.
        Logs the process and handles potential errors during creation.

        Attributes:
            device_group (DeviceGroup): The device group for which resources are created.

        Error:
            PanDeviceError: Raised for errors during bulk creation of objects.
            Exception: Raised for unexpected errors during the process.

        Return:
            None
        """

        logger.info(
            f"Starting bulk creation of objects for {device_group.name} device group"
        )
        try:
            # # Bulk create tags
            # self._create_and_log_objects(
            #     device_group,
            #     Tag,
            #     "tags",
            # )
            # Bulk create address objects
            self._create_and_log_objects(
                device_group,
                AddressObject,
                "address objects",
            )
            # # Bulk create address groups
            # self._create_and_log_objects(
            #     device_group,
            #     AddressGroup,
            #     "address groups",
            # )

            # # Bulk create application containers
            # self._create_and_log_objects(
            #     device_group,
            #     ApplicationContainer,
            #     "application containers",
            # )

            # # Bulk create service objects
            # self._create_and_log_objects(
            #     device_group,
            #     ServiceObject,
            #     "service objects",
            # )

            # # Bulk create service groups
            # self._create_and_log_objects(
            #     device_group,
            #     ServiceGroup,
            #     "service groups",
            # )

            # # Bulk create application tags
            # self._create_and_log_objects(
            #     device_group,
            #     ApplicationTag,
            #     "application tags",
            # )

            # # Bulk create application objects
            # self._create_and_log_objects(
            #     device_group,
            #     ApplicationObject,
            #     "application objects",
            # )

            logger.info(
                f"Completed bulk creation of objects for {device_group.name} device group"
            )
        except PanDeviceError as e:
            logger.error(
                f"Error during bulk creation of objects in {device_group.name}: {e}"
            )
        except Exception as e:
            logger.error(
                f"Unexpected error during bulk creation of objects in {device_group.name}: {e}"
            )

    @staticmethod
    def tags(
        tag_configuration: List[Dict[str, Any]],
        device_group: DeviceGroup,
    ) -> None:
        """
        Create and add tags to a device group based on a given configuration.

        Iterates through the tag configuration, creates Tag objects, and adds them to the specified
        device group. Uses bulk operation for efficiency. Logs the process and handles exceptions.

        Attributes:
            tag_configuration (List[Dict[str, Any]]): List of dictionaries containing tag details.
            device_group (DeviceGroup): The device group to which tags will be added.

        Errors:
            PanObjectMissing: When there's an error creating tags.
            PanDeviceXapiError: When there's an API error while creating tags.
            Exception: For unexpected errors during tag creation.

        Return:
            None
        """

        if not tag_configuration:
            logger.warning(
                f"No tag configuration found for {device_group.name} device group"
            )
            return

        try:
            for each in tag_configuration:
                tag = Tag(
                    name=each["name"],
                    color=each["color"],
                    comments=each.get("comments", ""),
                )
                device_group.add(tag)

            tags = device_group.findall(Tag)
            if tags:
                tags[0].create_similar()
                logger.info(
                    f"Created and added {len(tags)} tags to the {device_group.name} device group using bulk operation"
                )
            else:
                logger.warning(
                    f"No tags found to create in {device_group.name} device group"
                )
        except PanObjectMissing as e:
            logger.error(f"Error creating tags in {device_group.name}: {e}")
        except PanDeviceXapiError as e:
            logger.error(f"API error while creating tags in {device_group.name}: {e}")
        except Exception as e:
            logger.error(f"Unexpected error creating tags in {device_group.name}: {e}")
