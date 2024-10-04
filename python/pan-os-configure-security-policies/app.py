# standard library imports
import argparse
import json
import sys

# pan-os-python SDK imports
from panos.errors import PanDeviceError, PanObjectMissing, PanDeviceXapiError
from panos.panorama import Panorama, PanoramaCommitAll

# local imports
from paloconfig import PaloConfig
from utils import set_log_level, logger


def parse_arguments():
    """
    Parse command-line arguments for configuring Palo Alto Networks Panorama.

    Sets up an argument parser with options for log level and returns parsed arguments.

    Attributes:
        -l, --log-level (str): Set the logging level (choices: debug, info, warning, error, critical; default: info)

    Return:
        argparse.Namespace: Parsed command-line arguments
    """
    parser = argparse.ArgumentParser(description="Configure Palo Alto Networks Panorama")
    parser.add_argument("-l", "--log-level", choices=["debug", "info", "warning", "error", "critical"], default="info", help="Set the logging level", type=lambda x: x.lower())
    parser.add_argument("--hostname", required=True, help="Panorama hostname or IP address")
    parser.add_argument("--username", required=True, help="Panorama username")
    parser.add_argument("--password", required=True, help="Panorama password")
    parser.add_argument("--device-group", required=True, help="Device group name")
    parser.add_argument("--address-name", required=True, help="Address object name")
    parser.add_argument("--address-type", required=True, help="Address object type")
    parser.add_argument("--address-value", required=True, help="Address object value")
    parser.add_argument("--address-description", default="", help="Address object description")
    parser.add_argument("--address-tags", nargs='*', default=[], help="Address object tags")
    return parser.parse_args()


def connect_to_panorama(
    hostname: str,
    username: str,
    password: str
) -> Panorama:
    """
    Establishes a connection to a Panorama device.

    Attempts to connect to a Panorama device using the provided hostname and API key.
    Refreshes system info upon successful connection.

    Attributes:
        hostname (str): The hostname or IP address of the Panorama device.
        username (str): The username for authentication.
        password (str): The username for authentication.

    Error:
        PanDeviceError: Raised if connection to Panorama fails.

    Return:
        Panorama: A connected Panorama object.
    """
    try:
        pan = Panorama(
            hostname=hostname,
            api_username=username,
            api_password=password,
        )
        pan.refresh_system_info()
        logger.info("Successfully connected to Panorama with credentials")
        return pan
    except PanDeviceError as e:
        logger.error(f"Failed to connect to Panorama: {e}")
        raise


def build_and_apply_config(
    panorama_config: PaloConfig,
    dg_name: str,
    dg_config: dict,
):
    """
    Build and apply a Palo Alto Networks Panorama configuration by device group.

    Creates a device group and configures various security configuration within it,
    including tags, address objects, and address groups. Handles exceptions that may
    occur during the configuration process.

    Attributes:
        panorama_config (PaloConfig): Configuration object for Palo Alto firewall.
        dg_name (str): Name of the device group to be created.
        dg_config (dict): Configuration dictionary for the device group.

    Error:
        PanObjectMissing: When a required object is missing.
        PanDeviceXapiError: When an API error occurs.
        Exception: For any unexpected errors during processing.
    """
    try:
        device_group = panorama_config.create_device_group(dg_name)

        # # Configure tags
        # panorama_config.tags(
        #     dg_config.get("objects", {}).get("tags", []),
        #     device_group,
        # )

        # # Configure address objects
        panorama_config.address_objects(
            dg_config.get("objects", {}).get("address_objects", []),
            device_group,
        )

        # # Configure address groups
        # panorama_config.address_groups(
        #     dg_config.get("objects", {}).get("address_groups", []),
        #     device_group,
        # )

        # # Configure application containers
        # panorama_config.application_containers(
        #     dg_config.get("objects", {}).get("application_container", []),
        #     device_group,
        # )

        # # Configure service objects
        # panorama_config.service_objects(
        #     dg_config.get("objects", {}).get("service_objects", []),
        #     device_group,
        # )

        # # Configure service groups
        # panorama_config.service_groups(
        #     dg_config.get("objects", {}).get("service_groups", []),
        #     device_group,
        # )

        # # Configure application objects
        # panorama_config.application_objects(
        #     dg_config.get("objects", {}).get("application_objects", []),
        #     device_group,
        # )

        # # Configure application tags
        # panorama_config.application_tags(
        #     dg_config.get("objects", {}).get("application_tags", []),
        #     device_group,
        # )

        # Perform bulk creation of objects
        panorama_config.bulk_create_resources(device_group)

    except PanObjectMissing as e:
        logger.error(f"Error processing device group {dg_name}: {e}")
    except PanDeviceXapiError as e:
        logger.error(f"API error while processing device group {dg_name}: {e}")
    except Exception as e:
        logger.error(f"Unexpected error processing device group {dg_name}: {e}")


def commit_changes(pan: Panorama):
    """
    Commit changes to Panorama and log the result.

    Attempts to commit changes to the Panorama device synchronously and logs the outcome.
    If successful, an info message is logged. If unsuccessful, an error is logged and an exception is raised.

    Args:
        pan (Panorama): The Panorama object to commit changes to.

    Raises:
        PanDeviceError: If the commit operation fails.
    """
    try:
        pan.commit(sync=True)
        logger.info("Successfully committed changes to Panorama")
    except PanDeviceError as e:
        logger.error(f"Failed to commit changes to Panorama: {e}")
        raise


def push_device_group(
    pan: Panorama,
    dg_name: str,
):
    """
    Push configuration to a specified device group in Panorama.

    Attempts to commit all changes to the specified device group using the Panorama object.
    Logs the result of the operation, whether successful or failed.

    Attributes:
        pan (Panorama): The Panorama object to use for the commit operation.
        dg_name (str): The name of the device group to push the configuration to.

    Error:
        PanDeviceError: Raised if the commit operation fails.
    """
    try:
        pan.commit_all(
            sync=True,
            devicegroup=dg_name,
        )
        logger.info(f"Configuration pushed to device group: {dg_name}")
    except PanDeviceError as e:
        logger.error(f"Failed to push configuration to device group {dg_name}: {e}")


def main():
    """
    This method is the entry point for the program. It performs the following steps:

    1. Parses the command line arguments.
    2. Sets the logging level based on the arguments.
    3. Connects to the Panorama device.
    4. Creates a PaloConfig instance for managing the Panorama configuration.
    5. Processes each device group in the Panorama configuration.
    6. Commits the changes to the Panorama device.
    7. Pushes the changes to each device group.

    If any errors occur during the process, a message will be logged and the method will return a non-zero value.

    Returns:
        int: The exit code of the method. 0 indicates success, while non-zero values indicate failure.
    """
    args = parse_arguments()
    set_log_level(args.log_level)

    try:
        # Create a panorama object
        pan = connect_to_panorama(
            hostname=args.hostname,
            username=args.username,
            password=args.password,
        )

        # Create PaloConfig instance
        panorama_config = PaloConfig(pan)

        # Retrieve or create the device group
        device_group = panorama_config.create_device_group(args.device_group)

        # Prepare address object configuration
        addr_obj_config = {
            "name": args.address_name,
            "type": args.address_type,
            "value": args.address_value,
            "description": args.address_description,
            "tag": args.address_tags,
        }

        # Configure address object
        panorama_config.address_objects([addr_obj_config], device_group)

        # Commit changes to Panorama
        panorama_config.commit_panorama(
            description="Commit changes to Panorama",
            admins=[args.username],
            device_groups=[args.device_group],
        )

        # Commit changes to each device group
        panorama_config.commit_all(
            style=PanoramaCommitAll.STYLE_DEVICE_GROUP,
            name=args.device_group,
            description=f"Commit changes to device group: {args.device_group}",
            admins=[args.username],
            include_template=True,
        )
        return json.loads('{"status": "completed"}')

    except PanDeviceError as e:
        logger.critical(f"Critical error in PAN-OS operations: {e}")
        return json.loads('{"status": "errored"}')
    except Exception as e:
        logger.critical(f"Unexpected error occurred: {e}")
        return json.loads('{"status": "errored"}')


if __name__ == "__main__":
    # The script exits with the status code returned by main()
    sys.exit(main())
