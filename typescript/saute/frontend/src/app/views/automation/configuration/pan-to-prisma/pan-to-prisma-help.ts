export const SYNC_TO_PRISMA_SCRIPT = `
# standard library imports
import logging
import argparse
from typing import Dict, List, Optional, Tuple, Any
from pydantic import BaseModel

# third party library imports
from environs import Env

# Palo Alto Networks PAN-OS imports
from panos.objects import AddressGroup as PanoramaAddressGroup
from panos.objects import AddressObject as PanoramaAddressObject
from panos.panorama import DeviceGroup, Panorama
from panos.policies import PreRulebase, PostRulebase, SecurityRule

# Palo Alto Networks Prisma imports
from panapi import PanApiSession
from panapi.config.objects import Address as PrismaAddress
from panapi.config.objects import AddressGroup as PrismaAddressGroup
from panapi.config.security import SecurityRule as PrismaSecurityRule


# ----------------------------------------------------------------------------
# Configure logging
# ----------------------------------------------------------------------------
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s"
)


# ----------------------------------------------------------------------------
# Load environment variables from .env file
# ----------------------------------------------------------------------------
env = Env()
env.read_env()

pan_config = {
    "pan_url": env("PANURL", "panorama.lab.com"),
    "api_key": env("PANTOKEN", "supersecret"),
}

prisma_config = {
    "client_id": env("PRISMA_CLIENT_ID", "automation@tsg.iam.panserviceaccount.com"),
    "client_secret": env(
        "PRISMA_CLIENT_SECRET", "12345678-1234-5678-90ab-1234567890ab"
    ),
    "tenant": env("PRISMA_TENANT", "1234567890"),
    "token_url": env(
        "PRISMA_TOKEN_URL",
        "https://auth.apps.paloaltonetworks.com/am/oauth2/access_token",
    ),
}


# ----------------------------------------------------------------------------
# Define data models
# ----------------------------------------------------------------------------
class SecurityRuleData(BaseModel):
    rule_name: str
    security_profile_group: Optional[List[str]]
    source_zones: List[str]
    destination_zones: List[str]
    source_addresses: List[str]
    destination_addresses: List[str]
    applications: List[str]
    services: List[str]
    actions: str
    description: Optional[str]


class AddressObjectData(BaseModel):
    source: str
    name: str
    value: str
    type: str


class AddressGroupData(BaseModel):
    source: str
    name: str
    description: Optional[str]
    static_value: List[str]


# ----------------------------------------------------------------------------
# Function to parse command line arguments
# ----------------------------------------------------------------------------
def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Parse arguments passed from Saute frontend."
    )
    parser.add_argument(
        "--config-objects",
        dest="config_objects",
        default="all",
        help="Comma-separated list of config objects to process (default: %(default)s). Options: address-objects, address-groups, security-rules, all",
    )
    parser.add_argument(
        "--pan-url",
        dest="pan_url",
        default=pan_config["pan_url"],
        help="Panorama URL (default: %(default)s)",
    )
    parser.add_argument(
        "--pan-token",
        dest="api_key",
        default=pan_config["api_key"],
        help="Panorama API token (default: %(default)s)",
    )
    parser.add_argument(
        "--client-id",
        dest="client_id",
        default=prisma_config["client_id"],
        help="Prisma Access Client ID (default: %(default)s)",
    )
    parser.add_argument(
        "--client-secret",
        dest="client_secret",
        default=prisma_config["client_secret"],
        help="Prisma Access Client Secret (default: %(default)s)",
    )
    parser.add_argument(
        "--tenant",
        dest="tsg_id",
        default=prisma_config["tenant"],
        help="Prisma Access Tenant Service Group ID (default: %(default)s)",
    )
    parser.add_argument(
        "--token-url",
        dest="token_url",
        default=prisma_config["token_url"],
        help="Prisma Access Token URL (default: %(default)s)",
    )
    return parser.parse_args()


# ----------------------------------------------------------------------------
# Function to create and return an instance of Panorama
# ----------------------------------------------------------------------------
def setup_panorama_client(pan_url: str, api_key: str) -> Panorama:
    logging.debug(f"pan_url: {pan_url}")
    logging.debug(f"api_key: {api_key}")
    return Panorama(hostname=pan_url, api_key=api_key)


# ----------------------------------------------------------------------------
# Function to fetch security rules
# ----------------------------------------------------------------------------
def get_security_rules(pan: Panorama) -> List[SecurityRuleData]:
    pre_rulebase = PreRulebase()
    post_rulebase = PostRulebase()

    pan.add(pre_rulebase)
    pan.add(post_rulebase)

    pre_rules = SecurityRule.refreshall(pre_rulebase)
    post_rules = SecurityRule.refreshall(post_rulebase)

    rules = pre_rules + post_rules

    rules_data = []
    for rule in rules:
        rule_data = SecurityRuleData(
            rule_name=rule.name,
            security_profile_group=rule.group if rule.group else None,
            source_zones=rule.fromzone,
            destination_zones=rule.tozone,
            source_addresses=rule.source,
            destination_addresses=rule.destination,
            applications=rule.application,
            services=rule.service,
            actions=rule.action,
            description=rule.description,
        )
        rules_data.append(rule_data)

    return rules_data


# ----------------------------------------------------------------------------
# Function to fetch address objects and groups
# ----------------------------------------------------------------------------
def get_address_objects_and_groups(
    pan: Panorama,
) -> Tuple[List[AddressObjectData], List[AddressGroupData]]:
    pan_address_objects = PanoramaAddressObject.refreshall(pan)
    logging.debug(pan_address_objects)

    pan_address_groups = PanoramaAddressGroup.refreshall(pan)
    logging.debug(pan_address_groups)

    address_objects = []
    address_groups = []

    for each in pan_address_objects:
        if not each.description:
            each.description = ""
        address_objects.append(
            AddressObjectData(
                source="Shared",
                name=each.name,
                value=each.value,
                type=each.type,
                description=each.description,
            )
        )

    for each in pan_address_groups:
        if each.static_value:
            if not each.description:
                each.description = ""
            address_groups.append(
                AddressGroupData(
                    source="Shared",
                    name=each.name,
                    description=each.description,
                    static_value=each.static_value,
                )
            )

    device_groups = DeviceGroup.refreshall(pan)

    for dg in device_groups:
        dg_address_objects = PanoramaAddressObject.refreshall(dg)
        for each in dg_address_objects:
            if not each.description:
                each.description = ""
            address_objects.append(
                AddressObjectData(
                    source=dg.name,
                    name=each.name,
                    value=each.value,
                    type=each.type,
                    description=each.description,
                )
            )

        dg_address_groups = PanoramaAddressGroup.refreshall(dg)
        for each in dg_address_groups:
            if each.static_value:
                if not each.description:
                    each.description = ""
                address_groups.append(
                    AddressGroupData(
                        source=dg.name,
                        name=each.name,
                        description=each.description,
                        static_value=each.static_value,
                    )
                )

    return address_objects, address_groups


# ----------------------------------------------------------------------------
# Function to create Prisma address objects
# ----------------------------------------------------------------------------
def create_prisma_address_objects(
    address_objects: List[AddressObjectData], session: PanApiSession
) -> List[Dict[str, str]]:
    prisma_address_objects = []
    for address_object in address_objects:
        logging.debug(address_object)
        # Initialize the object with only the fields that are always present
        prisma_address_data = {
            "folder": "Prisma Access",
            "name": f"{address_object.source}-{address_object.name}",
        }

        # Add description field if it exists in address_object
        if hasattr(address_object, "description") and address_object.description:
            prisma_address_data["description"] = address_object.description

        # Assign different keys based on the type of the address_object
        if address_object.type == "ip-netmask":
            prisma_address_data["ip_netmask"] = address_object.value
        elif address_object.type == "fqdn":
            prisma_address_data["fqdn"] = address_object.value
        elif address_object.type == "ip-range":
            prisma_address_data["ip_range"] = address_object.value

        prisma_address = PrismaAddress(**prisma_address_data)
        prisma_address.create(session)
        prisma_address_objects.append(prisma_address_data)
    return prisma_address_objects


# ----------------------------------------------------------------------------
# Function to create Prisma address groups
# ----------------------------------------------------------------------------
def create_prisma_address_groups(
    address_groups: List[AddressGroupData], session: PanApiSession
) -> List[Dict[str, str]]:
    prisma_address_groups = []
    for address_group in address_groups:
        logging.debug("address_group: %s", address_group)
        try:
            # Create a new list of address object names for Prisma
            prisma_static_value = [
                f"{address_group.source}-{name}" for name in address_group.static_value
            ]
            prisma_address_group_data = {
                "folder": "Prisma Access",
                "name": f"{address_group.source}-{address_group.name}",
                "description": address_group.description,
                "static": prisma_static_value,
            }
            prisma_address_group = PrismaAddressGroup(**prisma_address_group_data)
            prisma_address_group.create(session)
        except Exception as e:
            logging.error("Error creating address group object: %s", e)
            return
        prisma_address_groups.append(prisma_address_group_data)
    return prisma_address_groups


# ----------------------------------------------------------------------------
# Function to create Prisma security rules
# ----------------------------------------------------------------------------
def create_prisma_security_rules(
    security_rules: List[SecurityRuleData], session: PanApiSession
) -> List[Dict[str, str]]:
    prisma_security_rules = []
    for security_rule in security_rules:
        logging.debug("security_rule: %s", security_rule)

        try:
            prisma_security_rule_data = {
                "name": security_rule.rule_name,
                "folder": "Prisma Access",
                "position": "pre",
                "action": security_rule.actions,
                "from": ["any"],
                "to": ["any"],
                "source": ["any"],
                "destination": ["any"],
                "source_user": ["any"],
                "category": ["any"],
                "application": security_rule.applications,
                "service": ["any"],
                "log_setting": "Cortex Data Lake",
                "description": security_rule.description
                if security_rule.description
                else "n/a",
            }
            prisma_security_rule = PrismaSecurityRule(**prisma_security_rule_data)
            logging.debug("prisma_security_rule: %s", prisma_security_rule)
            prisma_security_rule.create(session)
        except Exception as e:
            logging.error("Error creating security rule: %s", e)
            return

        prisma_security_rules.append(prisma_security_rule_data)
    return prisma_security_rules


# ----------------------------------------------------------------------------
# Main execution of our script
# ----------------------------------------------------------------------------
def run_pan_to_prisma(
    pan_url: str,
    api_key: str,
    client_id: str,
    client_secret: str,
    tsg_id: str,
    token_url: str,
    config_objects: str,
) -> Dict[str, Any]:
    # initialize result dictionary
    result = {}

    # process config objects to determine which parts of the config we will work on
    config_objects_list = [item.strip() for item in config_objects.split(",")]
    process_all = "all" in config_objects_list
    process_address_objects = process_all or "address-objects" in config_objects_list
    process_address_groups = process_all or "address-groups" in config_objects_list
    process_security_rules = process_all or "security-rules" in config_objects_list

    # authenticate with Panorama
    logging.info("Authenticating with Panorama...")
    pan = setup_panorama_client(pan_url, api_key)
    logging.debug(pan)

    # authenticate with Prisma
    try:
        session = PanApiSession()
        logging.info("Authenticating with Prisma Access...")
        logging.debug(f"client_id: {client_id}")
        logging.debug(f"client_secret: {client_secret}")
        logging.debug(f"tsg_id: {tsg_id}")
        logging.debug(f"token_url: {token_url}")

        session.authenticate(
            client_id=client_id,
            client_secret=client_secret,
            scope=f"profile tsg_id:{tsg_id} email",
            token_url=token_url,
        )
    except Exception as e:
        logging.error(f"Error with Prisma authentication: {e}")
        return {"error": str(e)}

    # fetch address objects and groups
    if process_address_objects or process_address_groups:
        try:
            logging.info("Retrieving address objects and groups...")
            address_objects, address_groups = get_address_objects_and_groups(pan)
        except Exception as e:
            logging.error("Error retrieving address objects and groups: %s", e)
            return

        # console logging when debugging
        for address_object in address_objects:
            logging.debug(address_object.json(indent=2))

        for address_group in address_groups:
            logging.debug(address_group.json(indent=2))

        # Add to result dictionary
        result["panorama_address_objects"] = [ao.dict() for ao in address_objects]
        result["panorama_address_groups"] = [ag.dict() for ag in address_groups]

    # Create Prisma address objects
    if process_address_objects:
        try:
            logging.info("Creating Prisma address objects...")
            prisma_address_objects = create_prisma_address_objects(
                address_objects, session
            )
        except Exception as e:
            logging.error(f"Error with Prisma API calls: {e}")
            return {"error": str(e)}

        # Add to result dictionary
        result["prisma_address_objects"] = prisma_address_objects

    # Create Prisma address groups
    if process_address_groups:
        try:
            logging.info("Creating Prisma address groups...")
            prisma_address_groups = create_prisma_address_groups(
                address_groups, session
            )
        except Exception as e:
            logging.error(f"Error with Prisma API calls: {e}")
            return {"error": str(e)}

        # Add to result dictionary
        result["prisma_address_groups"] = prisma_address_groups

    # Create Prisma security rules
    if process_security_rules:
        # fetch security rules
        try:
            logging.info("Retrieving security rules...")
            rules = get_security_rules(pan)
            logging.debug(rules)
        except Exception as e:
            logging.error("Error retrieving security rules: %s", e)
            return

        # console logging when debugging
        for rule_data in rules:
            logging.debug(rule_data.json(indent=2))

        # Add to result dictionary
        result["panorama_security_rules"] = [sr.dict() for sr in rules]
        try:
            logging.info("Creating Prisma security rules...")
            prisma_security_rules = create_prisma_security_rules(rules, session)
        except Exception as e:
            logging.error(f"Error with Prisma API calls: {e}")
            return {"error": str(e)}

        # Add to result dictionary
        result["prisma_security_rules"] = prisma_security_rules

    logging.info("Completed job successfully!")
    return result


# ----------------------------------------------------------------------------
# Execute main function
# ----------------------------------------------------------------------------
if __name__ == "__main__":
    args = parse_arguments()
    result = run_pan_to_prisma(
        args.pan_url,
        args.api_key,
        args.client_id,
        args.client_secret,
        args.tsg_id,
        args.token_url,
        args.config_objects,
    )
    logging.debug(result)
`;
