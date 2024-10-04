# standard library imports
import argparse
import sys

# pan-os-python SDK imports
from panos.errors import PanDeviceError
from panos.panorama import Panorama, PanoramaCommitAll, DeviceGroup
from panos.policies import PreRulebase, SecurityRule

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
        "--rule-name",
        required=True,
        help="Security rule name",
    )
    parser.add_argument(
        "--rule-description",
        default="",
        help="Security rule description",
    )
    parser.add_argument(
        "--rule-tag",
        nargs="*",
        default=[],
        help="Security rule tags",
    )
    parser.add_argument(
        "--rule-disabled",
        action="store_true",
        help="Disable the security rule",
    )
    parser.add_argument(
        "--rule-from-zone",
        required=True,
        nargs="+",
        help="From zone(s) for the security rule",
    )
    parser.add_argument(
        "--rule-to-zone",
        required=True,
        nargs="+",
        help="To zone(s) for the security rule",
    )
    parser.add_argument(
        "--rule-source",
        required=True,
        nargs="+",
        help="Source address(es) for the security rule",
    )
    parser.add_argument(
        "--rule-destination",
        required=True,
        nargs="+",
        help="Destination address(es) for the security rule",
    )
    parser.add_argument(
        "--rule-application",
        required=True,
        nargs="+",
        help="Application(s) for the security rule",
    )
    parser.add_argument(
        "--rule-service",
        required=True,
        nargs="+",
        help="Service(s) for the security rule",
    )
    parser.add_argument(
        "--rule-category",
        nargs="+",
        help="URL category for the security rule",
    )
    parser.add_argument(
        "--rule-security-profile-group",
        help="Security profile group for the security rule",
    )
    parser.add_argument(
        "--rule-log-setting",
        help="Log setting for the security rule",
    )
    parser.add_argument(
        "--rule-action",
        required=True,
        choices=["allow", "deny", "drop", "reset-client", "reset-server", "reset-both"],
        help="Action for the security rule",
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

        # Prepare security rule configuration
        security_rule_config = {
            "name": args.rule_name,
            "fromzone": args.rule_from_zone,
            "tozone": args.rule_to_zone,
            "source": args.rule_source,
            "destination": args.rule_destination,
            "application": args.rule_application,
            "service": args.rule_service,
            "action": args.rule_action,
            "description": args.rule_description,
            "tag": args.rule_tag,
            "disabled": args.rule_disabled,
            "log_setting": args.rule_log_setting,
            "group": args.rule_security_profile_group,
            "category": args.rule_category,
        }

        # Configure security rule
        panorama_config.security_rules(
            security_rule_configuration=[security_rule_config],
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
