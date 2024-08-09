# standard library imports
import logging

# 3rd party imports
from config import settings
from panos.panorama import Panorama, DeviceGroup
from panos.objects import AddressObject, AddressGroup, Tag
from panos.network import Zone, Interface
from panos.policies import PostRulebase, PreRulebase, SecurityRule
from panos.errors import PanDeviceError

# ----------------------------------------------------------------------------
# Configure logging
# ----------------------------------------------------------------------------
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s"
)

# ----------------------------------------------------------------------------
# create a panorama object
# ----------------------------------------------------------------------------
pan = Panorama(
    hostname=settings.panos_config.panorama.base_url,
    api_key=settings.panos_config.panorama.api_key,
)

# ----------------------------------------------------------------------------
# test our Panorama creds, attempt to refresh the system info with pan object
# ----------------------------------------------------------------------------
try:
    pan.refresh_system_info()
    logging.info("Successfully connected to Panorama with credentials")
except PanDeviceError as pan_device_error:
    logging.error("Failed to connect to Panorama: %s", pan_device_error)
    exit(1)  # Exit the script if connection fails

# ----------------------------------------------------------------------------
# create device group and attach to Panorama
# ----------------------------------------------------------------------------
device_group_name = "Magnolia"
device_group = DeviceGroup(device_group_name)
pan.add(device_group)
logging.info(f"Successfully attached {device_group_name} device group object to Panorama object")

# ----------------------------------------------------------------------------
# create tags and add them to the device group
# ----------------------------------------------------------------------------
dg_config = settings.panos_config.device_groups.get(device_group_name)
if dg_config and dg_config.objects.tags:
    for tag_config in dg_config.objects.tags:
        tag = Tag(
            name=tag_config.name,
            color=tag_config.color,
            comments=tag_config.comments
        )
        device_group.add(tag)
        tag.create()
    logging.info(f"Created and added tags to the {device_group_name} device group")
else:
    logging.warning(f"No tags found for {device_group_name} device group")

# # ----------------------------------------------------------------------------
# # create address groups and add them to the device group
# # ----------------------------------------------------------------------------
# for group in settings.address_groups:
#     addr_group = AddressGroup(
#         name=group.name,
#         static_value=group.members
#     )
#     device_group.add(addr_group)
#     addr_group.create()
# logging.info("Created and added address groups to the device group")
#
# # ----------------------------------------------------------------------------
# # create security zones and associate them with interfaces
# # ----------------------------------------------------------------------------
# for zone_config in settings.security_zones:
#     zone = Zone(name=zone_config.name)
#     device_group.add(zone)
#     zone.create()
#
#     for intf_name in zone_config.interfaces:
#         interface = Interface(name=intf_name)
#         zone.add(interface)
#         interface.create()
# logging.info("Created security zones and associated them with interfaces")
#
# # ----------------------------------------------------------------------------
# # create pre-rulebase and security rules
# # ----------------------------------------------------------------------------
# pre_rulebase = PreRulebase()
# device_group.add(pre_rulebase)
#
# for rule in settings.security_rules.pre_rules:
#     new_rule = SecurityRule(
#         name=rule.name,
#         fromzone=rule.from_zone,
#         tozone=rule.to_zone,
#         source=rule.source,
#         destination=rule.destination,
#         application=rule.application,
#         service=rule.service,
#         action=rule.action,
#     )
#     pre_rulebase.add(new_rule)
#     new_rule.create()
# logging.info("Created pre-rulebase security rules")
#
# # ----------------------------------------------------------------------------
# # create post-rulebase and security rules
# # ----------------------------------------------------------------------------
# post_rulebase = PostRulebase()
# device_group.add(post_rulebase)
#
# for rule in settings.security_rules.post_rules:
#     new_rule = SecurityRule(
#         name=rule.name,
#         fromzone=rule.from_zone,
#         tozone=rule.to_zone,
#         source=rule.source,
#         destination=rule.destination,
#         application=rule.application,
#         service=rule.service,
#         action=rule.action,
#     )
#     post_rulebase.add(new_rule)
#     new_rule.create()
# logging.info("Created post-rulebase security rules")
#
# # ----------------------------------------------------------------------------
# # ensure "Deny Any" rule is at the bottom of post-rulebase
# # ----------------------------------------------------------------------------
# deny_all = SecurityRule.find(post_rulebase, name="Deny Any")
# if deny_all:
#     deny_all.refresh()
#     deny_all.move(location="bottom")
# else:
#     deny_all = SecurityRule(
#         name="Deny Any",
#         fromzone=["any"],
#         tozone=["any"],
#         source=["any"],
#         destination=["any"],
#         application=["any"],
#         service=["any"],
#         action="deny",
#     )
#     post_rulebase.add(deny_all)
#     deny_all.create()
# logging.info("Ensured 'Deny Any' rule is at the bottom of post-rulebase")

# ----------------------------------------------------------------------------
# commit changes to Panorama and push to device group
# ----------------------------------------------------------------------------
pan.commit(sync=True)
logging.info("Successfully committed changes to Panorama")

pan.commit_all(
    sync=True,
    devicegroup=device_group.name,
)
logging.info(f"Configuration pushed to device group: {device_group.name}")
