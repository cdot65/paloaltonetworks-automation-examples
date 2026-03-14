# ----------------------------------------------------------------------------
# DNS Settings
# ----------------------------------------------------------------------------
resource "panos_dns_settings" "Panorama" {

  # targets 'localhost.localdomain' by default in xpath
  location = var.dns_settings.Panorama.location

  # configuration
  dns_setting = var.dns_settings.Panorama.dns_setting
}

resource "panos_dns_settings" "Branch" {

  # targets 'localhost.localdomain' by default in xpath
  location = var.dns_settings.Branch.location

  # configuration
  dns_setting = var.dns_settings.Branch.dns_setting

  # depends on clause
  depends_on = [
    panos_template.Branch
  ]
}

# ----------------------------------------------------------------------------
# NTP Settings
# ----------------------------------------------------------------------------
resource "panos_ntp_settings" "Panorama" {

  # targets 'localhost.localdomain'
  location = var.ntp_settings.Panorama.location

  # configuration
  ntp_servers = var.ntp_settings.Panorama.ntp_servers
}

resource "panos_ntp_settings" "Branch" {

  # targets 'Branch-Template'
  location = var.ntp_settings.Branch.location

  # configuration
  ntp_servers = var.ntp_settings.Branch.ntp_servers
}

# ----------------------------------------------------------------------------
# Panorama Templates
# ----------------------------------------------------------------------------
resource "panos_template" "Branch" {

  # targets 'localhost.localdomain' by default in xpath
  location = {
    panorama = {}
  }

  # configuration
  name        = var.templates.Branch.name
  description = var.templates.Branch.description
}

# ----------------------------------------------------------------------------
# Panorama Template Stacks
# ----------------------------------------------------------------------------
resource "panos_template_stack" "Dallas" {

  # targets 'localhost.localdomain' by default in xpath
  location = {
    panorama = {}
  }

  # configuration
  name         = var.template_stacks.Dallas.name
  description  = var.template_stacks.Dallas.description
  templates    = [panos_template.Branch.name]
  devices      = var.template_stacks.Dallas.devices
  default_vsys = var.template_stacks.Dallas.default_vsys

  # depends on clause
  depends_on = [
    panos_template.Branch
  ]
}

resource "panos_template_stack" "Woodlands" {

  # targets 'localhost.localdomain' by default in xpath
  location = {
    panorama = {}
  }

  # configuration
  name         = var.template_stacks.Woodlands.name
  description  = var.template_stacks.Woodlands.description
  templates    = [panos_template.Branch.name]
  devices      = var.template_stacks.Woodlands.devices
  default_vsys = var.template_stacks.Woodlands.default_vsys

  # depends on clause
  depends_on = [
    panos_template.Branch
  ]
}

# ----------------------------------------------------------------------------
# Panorama Template Interface Management Profile
# ----------------------------------------------------------------------------
resource "panos_interface_management_profile" "Local_Management" {

  # targets 'Branch-Template'
  location = var.interface_management_profiles.Local_Management.location

  # configuration
  name          = var.interface_management_profiles.Local_Management.name
  ping          = var.interface_management_profiles.Local_Management.ping
  https         = var.interface_management_profiles.Local_Management.https
  permitted_ips = var.interface_management_profiles.Local_Management.permitted_ips
  ssh           = var.interface_management_profiles.Local_Management.ssh

  # depends on clause
  depends_on = [
    panos_template.Branch
  ]
}

# ----------------------------------------------------------------------------
# Panorama Template Variables
# ----------------------------------------------------------------------------
resource "panos_template_variable" "interface_lan" {

  # targets template Branch-Template
  location = var.template_variables.interface_lan.location

  # configuration
  name        = var.template_variables.interface_lan.name
  description = var.template_variables.interface_lan.description
  type        = var.template_variables.interface_lan.type

  # depends on clause
  depends_on = [
    panos_template_stack.Dallas,
    panos_template_stack.Woodlands
  ]
}

resource "panos_template_variable" "interface_wan" {

  # targets template Branch-Template
  location = var.template_variables.interface_wan.location

  # configuration
  name        = var.template_variables.interface_wan.name
  description = var.template_variables.interface_wan.description
  type        = var.template_variables.interface_wan.type

  # depends on clause
  depends_on = [
    panos_template_stack.Dallas,
    panos_template_stack.Woodlands
  ]
}

# ----------------------------------------------------------------------------
# Panorama Template Ethernet Interfaces
# ----------------------------------------------------------------------------
resource "panos_ethernet_interface" "ethernet1" {

  # targets template Branch-Template
  location = var.ethernet_interfaces.ethernet1.location

  # configuration
  name    = var.ethernet_interfaces.ethernet1.name
  comment = var.ethernet_interfaces.ethernet1.comment
  layer3  = var.ethernet_interfaces.ethernet1.layer3

  # depends on clause
  depends_on = [
    panos_template_variable.interface_wan
  ]
}

resource "panos_ethernet_interface" "ethernet2" {

  # targets template Branch-Template
  location = var.ethernet_interfaces.ethernet2.location

  # configuration
  name    = var.ethernet_interfaces.ethernet2.name
  comment = var.ethernet_interfaces.ethernet2.comment
  layer3  = var.ethernet_interfaces.ethernet2.layer3

  # depends on clause
  depends_on = [
    panos_template_variable.interface_lan
  ]
}

# override currently produces The plugin6.(*GRPCProvider).ApplyResourceChange request was cancelled.
# resource "panos_ethernet_interface" "Dallas_ethernet2" {
#
#   # targets template Branch-Template
#   location = {
#     template_stack = {
#       name = "Dallas-TemplateStack"
#     }
#   }
#
#   # configuration
#   name = var.ethernet_interfaces.ethernet2.name
#   layer3 = {
#     ips = [
#       { name = "192.168.1.1/24" }
#     ]
#   }
#
#   # depends on clause
#   depends_on = [panos_ethernet_interface.ethernet2]
# }

# ----------------------------------------------------------------------------
# Panorama Template Loopback Interfaces
# ----------------------------------------------------------------------------
resource "panos_loopback_interface" "Loopback1" {

  # targets template Branch-Template, vsys1
  location = var.loopback_interfaces.Loopback1.location

  # configuration
  name                         = var.loopback_interfaces.Loopback1.name
  adjust_tcp_mss               = var.loopback_interfaces.Loopback1.adjust_tcp_mss
  comment                      = var.loopback_interfaces.Loopback1.comment
  interface_management_profile = var.loopback_interfaces.Loopback1.interface_management_profile
  ips                          = var.loopback_interfaces.Loopback1.ips
  mtu                          = var.loopback_interfaces.Loopback1.mtu

  # depends on clause
  depends_on = [
    panos_template_variable.interface_wan
  ]
}

# ----------------------------------------------------------------------------
# Panorama Template Security Zones
# ----------------------------------------------------------------------------
resource "panos_zone" "untrust_zone" {

  # targets template Branch-Template
  location = var.zones.untrust_zone.location

  # configuration
  name                         = var.zones.untrust_zone.name
  enable_device_identification = var.zones.untrust_zone.enable_device_identification
  enable_user_identification   = var.zones.untrust_zone.enable_user_identification
  network                      = var.zones.untrust_zone.network

  # depends on clause
  depends_on = [
    panos_ethernet_interface.ethernet1
  ]
}

resource "panos_zone" "trust_zone" {

  # targets template Branch-Template
  location = var.zones.trust_zone.location

  # configuration
  name                         = var.zones.trust_zone.name
  enable_device_identification = var.zones.trust_zone.enable_device_identification
  enable_user_identification   = var.zones.trust_zone.enable_user_identification
  network                      = var.zones.trust_zone.network

  # depends on clause
  depends_on = [
    panos_ethernet_interface.ethernet2
  ]
}

# ----------------------------------------------------------------------------
# Panorama Template Virtual Routers
# ----------------------------------------------------------------------------
resource "panos_virtual_router" "branch_vr" {

  # targets template Branch-Template
  location = var.virtual_routers.branch_vr.location

  # configuration
  name = var.virtual_routers.branch_vr.name
  interfaces = [
    var.ethernet_interfaces.ethernet1.name,
    var.ethernet_interfaces.ethernet2.name
  ]
  routing_table = var.virtual_routers.branch_vr.routing_table

  # depends on clause
  depends_on = [
    panos_zone.untrust_zone,
    panos_zone.trust_zone,
  ]
}

# ----------------------------------------------------------------------------
# Panorama Device Groups
# ----------------------------------------------------------------------------
resource "panos_device_group" "Branch" {

  # targets 'localhost.localdomain' by default
  location = var.device_groups.Branch.location

  # configuration
  name = var.device_groups.Branch.name

  # depends on clause
  depends_on = [
    panos_virtual_router.branch_vr,
  ]

}

resource "panos_device_group" "Dallas" {
  # targets 'localhost.localdomain' by default
  location = var.device_groups.Dallas.location

  # configuration
  name    = var.device_groups.Dallas.name
  devices = var.device_groups.Dallas.devices

  # depends on clause
  depends_on = [
    panos_device_group.Branch,
  ]
}

resource "panos_device_group" "Woodlands" {
  # targets 'localhost.localdomain' by default
  location = var.device_groups.Woodlands.location

  # configuration
  name    = var.device_groups.Woodlands.name
  devices = var.device_groups.Woodlands.devices

  # depends on clause
  depends_on = [
    panos_device_group.Branch,
  ]
}

# ----------------------------------------------------------------------------
# Panorama Device Group Parents
# ----------------------------------------------------------------------------
resource "panos_device_group_parent" "Dallas" {

  # targets 'localhost.localdomain' by default
  location = var.device_group_parents.Dallas.location

  # configuration
  device_group = var.device_group_parents.Dallas.device_group
  parent       = var.device_group_parents.Dallas.parent

  # depends on clause
  depends_on = [
    panos_device_group.Dallas,
  ]
}

# Branch device group (Parent)
resource "panos_device_group_parent" "Woodlands" {

  # targets 'localhost.localdomain' by default
  location = var.device_group_parents.Woodlands.location

  # configuration
  device_group = var.device_group_parents.Woodlands.device_group
  parent       = var.device_group_parents.Woodlands.parent

  # depends on clause
  depends_on = [
    panos_device_group.Woodlands,
  ]
}

# ----------------------------------------------------------------------------
# Panorama Device Group Administrative Tags
# ----------------------------------------------------------------------------
resource "panos_administrative_tag" "Automation" {

  # targets Branch-DG device group
  location = var.administrative_tags.Automation.location

  # configuration
  name     = var.administrative_tags.Automation.name
  color    = var.administrative_tags.Automation.color
  comments = var.administrative_tags.Automation.comments

  # depends on clause
  depends_on = [
    panos_device_group.Branch,
  ]
}

resource "panos_administrative_tag" "Staging" {

  # targets Branch-DG device group
  location = var.administrative_tags.Staging.location

  # configuration
  name     = var.administrative_tags.Staging.name
  color    = var.administrative_tags.Staging.color
  comments = var.administrative_tags.Staging.comments

  # depends on clause
  depends_on = [
    panos_device_group.Branch,
  ]
}

resource "panos_administrative_tag" "Production" {

  # targets Branch-DG device group
  location = var.administrative_tags.Production.location

  # configuration
  name     = var.administrative_tags.Production.name
  color    = var.administrative_tags.Production.color
  comments = var.administrative_tags.Production.comments

  # depends on clause
  depends_on = [
    panos_device_group.Branch,
  ]
}

resource "panos_administrative_tag" "Critical" {

  # targets Branch-DG device group
  location = var.administrative_tags.Critical.location

  # configuration
  name     = var.administrative_tags.Critical.name
  color    = var.administrative_tags.Critical.color
  comments = var.administrative_tags.Critical.comments

  # depends on clause
  depends_on = [
    panos_device_group.Branch,
  ]
}

# ----------------------------------------------------------------------------
# Panorama Device Group Address Objects
# ----------------------------------------------------------------------------
resource "panos_addresses" "Branch" {

  # targets 'Branch-DG' Device Group
  location = var.addresses.Branch.location

  # configuration
  addresses = var.addresses.Branch.addresses

  # depends on clause
  depends_on = [
    panos_device_group.Branch,
    panos_administrative_tag.Automation,
    panos_administrative_tag.Critical,
    panos_administrative_tag.Production,
    panos_administrative_tag.Staging
  ]
}

# ----------------------------------------------------------------------------
# Panorama Device Group Address Groups
# ----------------------------------------------------------------------------
resource "panos_address_group" "Branch_Webservers" {

  # targets 'Branch-DG' Device Group
  location = var.address_groups.Branch.location

  # configuration
  name        = var.address_groups.Branch.groups.Webservers.name
  description = var.address_groups.Branch.groups.Webservers.description
  static      = var.address_groups.Branch.groups.Webservers.static
  tags        = var.address_groups.Branch.groups.Webservers.tags

  # depends on clause
  depends_on = [
    panos_device_group.Branch,
    panos_addresses.Branch
  ]
}

resource "panos_address_group" "Branch_Databases" {

  # targets 'Branch-DG' Device Group
  location = var.address_groups.Branch.location

  # configuration
  name        = var.address_groups.Branch.groups.Databases.name
  description = var.address_groups.Branch.groups.Databases.description
  static      = var.address_groups.Branch.groups.Databases.static
  tags        = var.address_groups.Branch.groups.Databases.tags

  # depends on clause
  depends_on = [
    panos_device_group.Branch,
    panos_addresses.Branch
  ]
}

resource "panos_address_group" "Branch_Cloud_Workloads" {

  # targets 'Branch-DG' Device Group
  location = var.address_groups.Branch.location

  # configuration
  name        = var.address_groups.Branch.groups.Cloud_Workloads.name
  description = var.address_groups.Branch.groups.Cloud_Workloads.description
  dynamic     = var.address_groups.Branch.groups.Cloud_Workloads.dynamic
  tags        = var.address_groups.Branch.groups.Cloud_Workloads.tags

  # depends on clause
  depends_on = [
    panos_device_group.Branch,
    panos_addresses.Branch
  ]
}

# ----------------------------------------------------------------------------
# Panorama Device Group Services
# ----------------------------------------------------------------------------
resource "panos_service" "web_service_dev" {

  # targets 'Branch-DG' Device Group
  location = var.services.Branch.location

  # configuration
  name        = var.services.Branch.services.web_service_dev.name
  description = var.services.Branch.services.web_service_dev.description
  tags        = var.services.Branch.services.web_service_dev.tags
  protocol    = var.services.Branch.services.web_service_dev.protocol

  # depends on clause
  depends_on = [
    panos_device_group.Branch,
    panos_administrative_tag.Automation,
    panos_administrative_tag.Critical,
    panos_administrative_tag.Production,
    panos_administrative_tag.Staging
  ]
}

resource "panos_service" "dns_dev" {

  # targets 'Branch-DG' Device Group
  location = var.services.Branch.location

  # configuration
  name        = var.services.Branch.services.dns_service_dev.name
  description = var.services.Branch.services.dns_service_dev.description
  tags        = var.services.Branch.services.dns_service_dev.tags
  protocol    = var.services.Branch.services.dns_service_dev.protocol

  # depends on clause
  depends_on = [
    panos_device_group.Branch,
    panos_administrative_tag.Automation,
    panos_administrative_tag.Critical,
    panos_administrative_tag.Production,
    panos_administrative_tag.Staging
  ]
}

# ----------------------------------------------------------------------------
# Panorama Device Group Service Groups
# ----------------------------------------------------------------------------
resource "panos_service_group" "web_group_dev" {

  # targets 'Branch-DG' Device Group
  location = var.service_groups.Branch.location

  # configuration
  name = var.service_groups.Branch.groups.web_group_dev.name
  # description = var.service_groups.Branch.groups.web_group_dev.description
  tags    = var.service_groups.Branch.groups.web_group_dev.tags
  members = var.service_groups.Branch.groups.web_group_dev.members

  # depends on clause
  depends_on = [
    panos_device_group.Branch,
    panos_service.web_service_dev,
  ]
}

# ----------------------------------------------------------------------------
# Panorama Device Group Security Policies
# ----------------------------------------------------------------------------
resource "panos_security_policy" "branch_policy" {

  # targets 'Branch-DG' Device Group
  location = var.security_policies.Branch.location

  # configuration
  rules = var.security_policies.Branch.policy_rules

  depends_on = [
    panos_device_group.Branch,
    panos_service.web_service_dev,
    panos_service.dns_dev,
    panos_administrative_tag.Automation
  ]
}

# ----------------------------------------------------------------------------
# Panorama Device Group Custom URL Categories
# ----------------------------------------------------------------------------
resource "panos_custom_url_category" "blocked_sites" {

  # targets 'Branch-DG' Device Group
  location = var.custom_url_categories.Branch.location

  # configuration
  name             = var.custom_url_categories.Branch.categories.blocked_sites.name
  description      = var.custom_url_categories.Branch.categories.blocked_sites.description
  type             = var.custom_url_categories.Branch.categories.blocked_sites.type
  list             = var.custom_url_categories.Branch.categories.blocked_sites.list
  disable_override = var.custom_url_categories.Branch.categories.blocked_sites.disable_override

  depends_on = [
    panos_device_group.Branch
  ]
}