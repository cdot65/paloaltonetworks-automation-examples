"""
PAN-OS client module for interacting with Panorama.

This module provides a high-level interface for interacting with Palo Alto Networks
Panorama appliances. It encapsulates common operations like connecting to Panorama,
managing address objects, and handling commits.
"""

from typing import Any, Dict, List, Optional, cast

from utils import logger

from models import AddressObject, LoopbackInterface, TunnelInterface
from panos.errors import PanDeviceError, PanXapiError
from panos.network import LoopbackInterface as PanosLoopbackInterface
from panos.network import TunnelInterface as PanosTunnelInterface
from panos.objects import AddressObject as PanAddressObject
from panos.panorama import DeviceGroup, Panorama, PanoramaCommit, PanoramaCommitAll, Template, TemplateStack


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

        # Refresh templates
        templates = Template.refreshall(panorama)
        logger.info("Found %d templates on Panorama", len(templates))

        # Refresh template stacks
        template_stacks = TemplateStack.refreshall(panorama)
        logger.info("Found %d template stacks on Panorama", len(template_stacks))

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

    def get_or_create_template(self, name: str) -> Optional[Template]:
        """
        Get an existing template or create a new one.

        Args:
            name (str): Name of the template.

        Returns:
            Optional[Template]: The template instance if successful, None otherwise.

        Raises:
            PanDeviceError: If template creation fails.
        """
        try:
            # Check if template exists
            existing = self.panorama.find(name, Template)
            if existing:
                logger.info("Found existing template: %s", name)
                return existing

            # Create new template
            logger.info("Creating template: %s", name)
            template = Template(name=name)
            try:
                self.panorama.add(template)
                template.create()
                return template
            except PanXapiError as e:
                logger.error("Failed to create template: %s", e)
                return None

        except PanDeviceError as e:
            logger.error("Failed to get/create template: %s", e)
            return None

    def get_or_create_template_stack(self, name: str) -> Optional[TemplateStack]:
        """
        Get an existing template stack or create a new one.

        Args:
            name (str): Name of the template stack.

        Returns:
            Optional[TemplateStack]: The template stack instance if successful, None otherwise.

        Raises:
            PanDeviceError: If template stack creation fails.
        """
        try:
            # Check if template stack exists
            existing = self.panorama.find(name, TemplateStack)
            if existing:
                logger.info("Found existing template stack: %s", name)
                return existing

            # Create new template stack
            logger.info("Creating template stack: %s", name)
            template_stack = TemplateStack(name=name)
            try:
                self.panorama.add(template_stack)
                template_stack.create()
                return template_stack
            except PanXapiError as e:
                logger.error("Failed to create template stack: %s", e)
                return None

        except PanDeviceError as e:
            logger.error("Failed to get/create template stack: %s", e)
            return None

    def create_tunnel_interface(self, template: Template, tunnel_interface: TunnelInterface) -> bool:
        """
        Create a new tunnel interface in the specified template.

        Args:
            template (Template): The template to create the interface in.
            tunnel_interface (TunnelInterface): The tunnel interface configuration.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            # Format the tunnel interface name correctly as tunnel.X (where X is the subinterface number)
            interface_name = f"{tunnel_interface.name}.{tunnel_interface.subinterface}"

            # Create the tunnel interface
            base_tunnel = PanosTunnelInterface(name=interface_name)

            # Handle IP address - if it's a list, use the first item
            if isinstance(tunnel_interface.ip, list) and tunnel_interface.ip:
                ip_value = tunnel_interface.ip[0]
                if isinstance(ip_value, str):
                    ip_address = ip_value
                else:
                    ip_address = str(ip_value)
            # If it's a special value (starting with $), use it as-is
            elif isinstance(tunnel_interface.ip, str) and tunnel_interface.ip.startswith("$"):
                # For special values, we need to use them as is
                # In PAN-OS this would typically be a pre-defined variable
                ip_address = tunnel_interface.ip
            else:
                # For standard IP addresses, use it directly
                ip_address = cast(str, tunnel_interface.ip)

            base_tunnel.ip = ip_address
            base_tunnel.comment = tunnel_interface.comment
            template.add(base_tunnel)

            try:
                # Create the tunnel interface
                base_tunnel.create()
                logger.info(
                    "Created tunnel interface: %s with IP %s",
                    interface_name,
                    tunnel_interface.ip,
                )

                return True

            except PanXapiError as e:
                if "already exists" not in str(e):
                    logger.error("Failed to create/update configuration: %s", e)
                    return False
                logger.info("Object already exists, continuing with configuration")
                return True

        except (PanDeviceError, PanXapiError) as e:
            logger.error("Failed to create tunnel interface: %s", e)
            return False

    def create_loopback_interface(self, template_stack: TemplateStack, loopback_interface: LoopbackInterface) -> bool:
        """
        Create a new loopback interface in the specified template stack.

        Args:
            template_stack (TemplateStack): The template stack to create the interface in.
            loopback_interface (LoopbackInterface): The loopback interface configuration.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            # Create the loopback interface
            loopback = PanosLoopbackInterface(name=loopback_interface.name)

            # Handle IP address - if it's a list, use the first item
            if isinstance(loopback_interface.ip, list) and loopback_interface.ip:
                ip_value = loopback_interface.ip[0]
                if isinstance(ip_value, str):
                    ip_address = ip_value
                else:
                    ip_address = str(ip_value)
            # If it's a special value (starting with $), use it as-is
            elif isinstance(loopback_interface.ip, str) and loopback_interface.ip.startswith("$"):
                # For special values, we need to use them as is
                # In PAN-OS this would typically be a pre-defined variable
                ip_address = loopback_interface.ip
            else:
                # For standard IP addresses, use it directly
                ip_address = cast(str, loopback_interface.ip)

            # Set the properties based on our model
            loopback.ip = ip_address
            loopback.comment = loopback_interface.comment

            if loopback_interface.ipv6_enabled:
                loopback.ipv6_enabled = True

            if loopback_interface.management_profile:
                loopback.management_profile = loopback_interface.management_profile

            if loopback_interface.mtu:
                loopback.mtu = loopback_interface.mtu

            if loopback_interface.adjust_tcp_mss:
                loopback.adjust_tcp_mss = True

            if loopback_interface.netflow_profile:
                loopback.netflow_profile = loopback_interface.netflow_profile

            if loopback_interface.ipv4_mss_adjust:
                loopback.ipv4_mss_adjust = loopback_interface.ipv4_mss_adjust

            if loopback_interface.ipv6_mss_adjust:
                loopback.ipv6_mss_adjust = loopback_interface.ipv6_mss_adjust

            # Add the loopback interface to the template stack
            template_stack.add(loopback)

            try:
                # Create the loopback interface
                loopback.create()
                logger.info(
                    "Created loopback interface: %s with IP %s",
                    loopback_interface.name,
                    loopback_interface.ip,
                )

                return True

            except PanXapiError as e:
                if "already exists" not in str(e):
                    logger.error("Failed to create/update configuration: %s", e)
                    return False
                logger.info("Object already exists, continuing with configuration")
                return True

        except (PanDeviceError, PanXapiError) as e:
            logger.error("Failed to create loopback interface: %s", e)
            return False

    def create_address_object(self, device_group: DeviceGroup, address_object: AddressObject) -> bool:
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
                description="Commit configuration changes",
                exclude_device_and_network=False,
                exclude_shared_objects=False,
            )
            self.panorama.commit(cmd=commit_panorama, sync=True)
            logger.info("Successfully committed changes to Panorama")
            return True
        except (PanDeviceError, PanXapiError) as e:
            logger.error("Failed to commit to Panorama: %s", e)
            return False

    def commit_all(
        self,
        templates: Optional[List[str]] = None,
        template_stacks: Optional[List[str]] = None,
    ) -> bool:
        """
        Push changes to all or specified templates or template stacks.

        Args:
            templates (Optional[List[str]]): List of template names.
                If None, not used in the commit.
            template_stacks (Optional[List[str]]): List of template stack names.
                If None, not used in the commit.

        Returns:
            bool: True if successful, False otherwise.
        """
        if not templates and not template_stacks:
            logger.warning("No templates or template stacks specified for commit-all")
            return False

        try:
            # Commit to templates if specified
            if templates:
                logger.info("Initiating commit-all to templates: %s", templates)

                for template_name in templates:
                    commit_all = PanoramaCommitAll(
                        style="template",
                        name=template_name,
                        description="Push configuration changes",
                        include_template=True,
                    )
                    self.panorama.commit(cmd=commit_all)
                    logger.info(
                        "Successfully initiated commit-all to template: %s",
                        template_name,
                    )

            # Commit to template stacks if specified
            if template_stacks:
                logger.info("Initiating commit-all to template stacks: %s", template_stacks)

                # PAN-OS API uses "template stack" style for template stacks
                for template_stack_name in template_stacks:
                    # Get templates associated with this template stack
                    try:
                        ts = self.panorama.find(template_stack_name, TemplateStack)
                        if ts and ts.templates:
                            for template_name in ts.templates:
                                logger.info(
                                    "Committing template associated with stack: %s -> %s",
                                    template_stack_name,
                                    template_name,
                                )
                                commit_all = PanoramaCommitAll(
                                    style="template stack",
                                    name=template_stack_name,
                                    description=(f"Push configuration changes for template stack {template_stack_name}"),
                                    include_template=True,
                                )
                                self.panorama.commit(cmd=commit_all)
                            logger.info(
                                "Successfully committed templates for stack: %s",
                                template_stack_name,
                            )
                        else:
                            logger.warning(
                                "Template stack %s not found or has no templates",
                                template_stack_name,
                            )
                    except (PanDeviceError, PanXapiError) as e:
                        logger.error(
                            "Failed to commit template stack %s: %s",
                            template_stack_name,
                            e,
                        )

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
                return job_result["result"] == "OK"
            except (PanDeviceError, PanXapiError) as e:
                logger.error("Failed to check job status: %s", e)
                return False

        return False
