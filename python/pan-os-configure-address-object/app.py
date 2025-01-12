# standard library imports
import argparse
import sys

# pan-os-python SDK imports
from panos.errors import PanDeviceError
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
    parser = argparse.ArgumentParser(
        description="Configure Palo Alto Networks Panorama"
    )
    parser.add_argument(
        "-l",
        "--log-level",
        choices=["debug", "info", "warning", "error", "critical"],
        default="info",
        help="Set the logging level",
        type=lambda x: x.lower(),
    )
    parser.add_argument(
        "--hostname",
        required=True,
        help="Panorama hostname or IP address",
    )
    parser.add_argument(
        "--username",
        required=True,
        help="Panorama username",
    )
    parser.add_argument(
        "--password",
        required=True,
        help="Panorama password",
    )
    parser.add_argument(
        "--device-group",
        required=True,
        help="Device group name",
    )
    parser.add_argument(
        "--address-name",
        required=True,
        help="Address object name",
    )
    parser.add_argument(
        "--address-type",
        required=True,
        help="Address object type",
    )
    parser.add_argument(
        "--address-value",
        required=True,
        help="Address object value",
    )
    parser.add_argument(
        "--address-description",
        default="",
        help="Address object description",
    )
    parser.add_argument(
        "--address-tags",
        nargs="*",
        default=[],
        help="Address object tags",
    )
    return parser.parse_args()


def connect_to_panorama(
    hostname: str,
    username: str,
    password: str,
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
        panorama_config.address_objects(
            address_object_configuration=[addr_obj_config],
            device_group=device_group,
        )

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
        print('{"status": "completed"}')  # Print JSON to stdout
        return 0

    except PanDeviceError as e:
        logger.critical(f"Critical error in PAN-OS operations: {e}")
        print('{"status": "errored"}')  # Print JSON to stdout
        return 1
    except Exception as e:
        logger.critical(f"Unexpected error occurred: {e}")
        print('{"status": "errored"}')  # Print JSON to stdout
        return 1


if __name__ == "__main__":
    # The script exits with the status code returned by main()
    sys.exit(main())
