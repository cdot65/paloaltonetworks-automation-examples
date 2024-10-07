# standard library imports
import logging
import argparse
import sys
from typing import Dict, List, Optional, Tuple, Any

# third party library imports
from config import settings

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
# Load environment variables from .secrets file
# ----------------------------------------------------------------------------
source_prisma_access = {
    "client_id": settings.oauth.source.client_id,
    "client_secret": settings.oauth.source.client_secret,
    "tenant": settings.oauth.source.tsg,
    "token_url": settings.oauth.token_url,
}
destination_prisma_access = {
    "client_id": settings.oauth.destination.client_id,
    "client_secret": settings.oauth.destination.client_secret,
    "tenant": settings.oauth.destination.tsg,
    "token_url": settings.oauth.token_url,
}


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
    return parser.parse_args()


# ----------------------------------------------------------------------------
# Function to filter rules that contain the specified tag
# ----------------------------------------------------------------------------
def filter_rules_by_tag(rules_data, tag):
    filtered_rules_data = []
    for rule_data in rules_data:
        # Check if the rule has tags and the specified tag is in the rule's tags
        if "tag" in rule_data and tag in rule_data["tag"]:
            filtered_rules_data.append(rule_data)
    return filtered_rules_data


# ----------------------------------------------------------------------------
# Prisma address objects
# ----------------------------------------------------------------------------
def get_address_objects_and_groups(session: PanApiSession) -> Tuple[List, List]:

    # name of our folder
    folder = {"folder": "Prisma Access"}

    # collect existing address objects in source tenant and append them to our empty placeholder address_objects
    source_address = PrismaAddress(**folder)
    address_objects = source_address.list(session)

    # collect existing address group in source tenant and append them to our empty placeholder address_groups
    source_address_groups = PrismaAddressGroup(**folder)
    address_groups = source_address_groups.list(session)

    return address_objects, address_groups


def create_prisma_address_objects(
    address_objects: List[PrismaAddress],
    session: PanApiSession,
) -> List[Dict[str, str]]:

    # empty placeholder
    prisma_address_objects = []

    for address_object in address_objects:
        logging.debug(address_object)
        ao = address_object.payload()
        # ao = {
        #     "folder": "Prisma Access",
        # }
        # if getattr(address_object, "name"):
        #     ao["name"] = address_object.name
        #
        # if getattr(address_object, "description"):
        #     ao["description"] = address_object.description
        #
        # if getattr(address_object, "value"):
        #     ao["value"] = address_object.value

        prisma_address = PrismaAddress(**ao)
        prisma_address.create(session)
        prisma_address_objects.append(address_object)
    return prisma_address_objects


# ----------------------------------------------------------------------------
# Function to create Prisma address groups
# ----------------------------------------------------------------------------
def create_prisma_address_groups(
    address_groups: List[PrismaAddressGroup], session: PanApiSession
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
            sys.exit(1)
        prisma_address_groups.append(prisma_address_group_data)
    return prisma_address_groups


# ----------------------------------------------------------------------------
# Function to create Prisma security rules
# ----------------------------------------------------------------------------
def create_prisma_security_rules(
    security_rules: Dict[str, Any], session: PanApiSession
) -> List[Dict[str, str]]:
    prisma_security_rules = []

    for device_group, rulebases in security_rules.items():
        logging.debug("device_group: %s", device_group)
        logging.debug("rulebases: %s", rulebases)

        if len(rulebases["pre_rules"]) > 0:
            logging.debug("pre_rules: %s", rulebases["pre_rules"])
            for rule in rulebases["pre_rules"]:
                logging.debug("rule: %s", rule)
                try:
                    # import ipdb

                    # ipdb.set_trace()

                    prisma_security_rule_data = {
                        "name": rule["rule_name"],
                        "folder": "Prisma Access",
                        "position": "pre",
                        "action": rule["actions"],
                        "from": ["any"],
                        "to": ["any"],
                        "source": ["any"],
                        "destination": ["any"],
                        "source_user": ["any"],
                        "category": ["any"],
                        "application": rule["applications"],
                        "service": ["any"],
                        "log_setting": "Cortex Data Lake",
                        "description": (
                            rule["description"] if rule["description"] else "n/a"
                        ),
                    }
                    prisma_security_rule = PrismaSecurityRule(
                        **prisma_security_rule_data
                    )
                    logging.debug("prisma_security_rule: %s", prisma_security_rule)
                    prisma_security_rule.create(session)
                except Exception as e:
                    logging.error("Error creating security rule: %s", e)

                prisma_security_rules.append(prisma_security_rule_data)

        if len(rulebases["post_rules"]) > 0:
            logging.debug("post_rules: %s", rulebases["post_rules"])
            for rule in rulebases["post_rules"]:
                logging.debug("rule: %s", rule)
                try:
                    prisma_security_rule_data = {
                        "name": rule["rule_name"],
                        "folder": "Prisma Access",
                        "position": "post",
                        "action": rule["actions"],
                        "from": ["any"],
                        "to": ["any"],
                        "source": ["any"],
                        "destination": ["any"],
                        "source_user": ["any"],
                        "category": ["any"],
                        "application": rule["applications"],
                        "service": ["any"],
                        "log_setting": "Cortex Data Lake",
                        "description": (
                            rule["description"] if rule["description"] else "n/a"
                        ),
                    }
                    prisma_security_rule = PrismaSecurityRule(
                        **prisma_security_rule_data
                    )
                    logging.debug("prisma_security_rule: %s", prisma_security_rule)
                    prisma_security_rule.create(session)
                except Exception as e:
                    logging.error("Error creating security rule: %s", e)
                    sys.exit(1)

                prisma_security_rules.append(prisma_security_rule_data)
    return prisma_security_rules


# ----------------------------------------------------------------------------
# Main execution of our script
# ----------------------------------------------------------------------------
def run_prisma_access_migrate(config_objects: str) -> Dict[str, Any]:

    # initialize result dictionary
    result = {}

    # process config objects to determine which parts of the config we will work on
    config_objects_list = [item.strip() for item in config_objects.split(",")]
    process_all = "all" in config_objects_list
    process_address_objects = process_all or "address_objects" in config_objects_list
    process_address_groups = process_all or "address_groups" in config_objects_list
    process_security_rules = process_all or "security_rules" in config_objects_list

    # Pseduo code
    # 1: authenticate with source Prisma Access Tenant
    # 2: retrieve all existing address objects
    # 3: retrieve all existing address groups
    # 4: authenticate with destination Prisma Access Tenant
    # 5: create all new address objects
    # 6: create all new address groups
    # 7: celebrate

    # authenticate with source Prisma Access Tenant
    try:
        source_session = PanApiSession()
        logging.info("Authenticating with source Prisma Access tenant...")

        source_session.authenticate(
            client_id=source_prisma_access["client_id"],
            client_secret=source_prisma_access["client_secret"],
            scope=f"profile tsg_id:{source_prisma_access['tenant']} email",
            token_url=source_prisma_access["token_url"],
        )
    except Exception as e:
        logging.error(f"Error with Prisma authentication: {e}")
        return {"error": str(e)}

    # fetch address objects and groups from source

    address_objects = []
    address_groups = []
    if process_address_objects or process_address_groups:
        try:
            logging.info("Retrieving address objects and groups from source tenant...")
            address_objects, address_groups = get_address_objects_and_groups(
                source_session
            )
        except Exception as e:
            logging.error("Error retrieving address objects and groups: %s", e)
            sys.exit(1)

    # authenticate with destination Prisma Access Tenant
    try:
        destination_session = PanApiSession()
        logging.info("Authenticating with destination Prisma Access tenant...")

        destination_session.authenticate(
            client_id=destination_prisma_access["client_id"],
            client_secret=destination_prisma_access["client_secret"],
            scope=f"profile tsg_id:{destination_prisma_access['tenant']} email",
            token_url=destination_prisma_access["token_url"],
        )
    except Exception as e:
        logging.error(f"Error with destination Prisma authentication: {e}")
        return {"error": str(e)}

    # Create Prisma address objects
    if process_address_objects:
        try:
            logging.info(
                "Creating Prisma address objects in destination prisma access tenant..."
            )
            prisma_address_objects = create_prisma_address_objects(
                address_objects,
                destination_session,
            )
        except Exception as e:
            logging.error(f"Error with Prisma API calls: {e}")
            return {"error": str(e)}

        # Add to result dictionary
        result["prisma_address_objects"] = prisma_address_objects

    # # Create Prisma address groups
    # if process_address_groups:
    #     try:
    #         logging.info("Creating Prisma address groups...")
    #         prisma_address_groups = create_prisma_address_groups(
    #             address_groups, session
    #         )
    #     except Exception as e:
    #         logging.error(f"Error with Prisma API calls: {e}")
    #         return {"error": str(e)}
    #
    #     # Add to result dictionary
    #     result["prisma_address_groups"] = prisma_address_groups
    #
    # # Create Prisma security rules
    # if process_security_rules:
    #     # fetch security rules
    #     try:
    #         logging.info("Retrieving security rules...")
    #
    #         # Fetch and process device groups
    #         device_groups = DeviceGroup.refreshall(pan)
    #         security_policy = {"shared": {"pre_rules": [], "post_rules": []}}
    #
    #         for dg in device_groups:
    #             dg_name = dg.name
    #
    #             # Skip the specified DeviceGroup
    #             if dg_name == "Service_Conn_Device_Group":
    #                 logging.info(f"Skipping DeviceGroup: {dg_name}")
    #                 continue
    #
    #             logging.info(f"Processing device group: {dg_name}")
    #
    #             # Fetch and convert security rules to SecurityRuleData
    #             dg_pre_rules_data = [
    #                 rule.dict()
    #                 for rule in get_security_rules(
    #                     pan,
    #                     device_group=dg,
    #                     position="pre",
    #                 )
    #             ]
    #             dg_post_rules_data = [
    #                 rule.dict()
    #                 for rule in get_security_rules(
    #                     pan,
    #                     device_group=dg,
    #                     position="post",
    #                 )
    #             ]
    #
    #             # Filter the converted rules
    #             dg_pre_rules_filtered = filter_rules_by_tag(
    #                 dg_pre_rules_data, "GlobalProtect"
    #             )
    #             dg_post_rules_filtered = filter_rules_by_tag(
    #                 dg_post_rules_data, "GlobalProtect"
    #             )
    #
    #             # Store filtered rules in the security policy dictionary
    #             security_policy[dg_name] = {
    #                 "pre_rules": dg_pre_rules_filtered,
    #                 "post_rules": dg_post_rules_filtered,
    #             }
    #
    #         # Fetch and convert shared rules to SecurityRuleData
    #         shared_pre_rules_data = [
    #             rule.dict()
    #             for rule in get_security_rules(
    #                 pan,
    #                 position="pre",
    #             )
    #         ]
    #         shared_post_rules_data = [
    #             rule.dict()
    #             for rule in get_security_rules(
    #                 pan,
    #                 position="post",
    #             )
    #         ]
    #
    #         # Filter the converted shared rules
    #         filtered_shared_pre_rules = filter_rules_by_tag(
    #             shared_pre_rules_data, "GlobalProtect"
    #         )
    #         filtered_shared_post_rules = filter_rules_by_tag(
    #             shared_post_rules_data, "GlobalProtect"
    #         )
    #
    #         # Update the security policy dictionary with filtered shared rules
    #         security_policy["shared"] = {
    #             "pre_rules": filtered_shared_pre_rules,
    #             "post_rules": filtered_shared_post_rules,
    #         }
    #         logging.debug(security_policy)
    #     except Exception as e:
    #         logging.error("Error retrieving security rules: %s", e)
    #         return
    #
    #     # Add to result dictionary
    #     result["panorama_security_rules"] = security_policy
    #     try:
    #         logging.info("Creating Prisma security rules...")
    #         prisma_security_rules = create_prisma_security_rules(
    #             security_policy, session
    #         )
    #     except Exception as e:
    #         logging.error(f"Error with Prisma API calls: {e}")
    #         return {"error": str(e)}
    #
    #     # Add to result dictionary
    #     result["prisma_security_rules"] = prisma_security_rules

    logging.info("Completed job successfully!")
    return result


# ----------------------------------------------------------------------------
# Execute main function
# ----------------------------------------------------------------------------
if __name__ == "__main__":
    args = parse_arguments()
    result = run_prisma_access_migrate(args.config_objects)
    logging.debug(result)
