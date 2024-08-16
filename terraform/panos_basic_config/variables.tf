/* Firewall Connectivity -------------------------------------------------- */

variable "firewall" {
  description = "Firewall connection details"
  type = object({
    fw_ip    = string,
    username = string,
    password = string,
  })
}

/* Ethernet Interfaces ---------------------------------------------------- */
variable "ethernet_interfaces" {
  type = map(object({
    name       = string,
    mode       = string,
    vsys       = string,
    static_ips = list(string)
  }))
}

/* Virtual Routers -------------------------------------------------------- */
variable "vr_name" {
  description = "Name of our virtual router"
}

/* Security Zones --------------------------------------------------------- */
variable "zones" {
  type = map(object({
    name = string,
    mode = string
  }))
}

/* Service Objects -------------------------------------------------------- */
variable "service_objects" {
  type = map(object({
    name             = string
    vsys             = string
    protocol         = string
    description      = string
    destination_port = string
  }))
}

/* NAT Policies ----------------------------------------------------------- */
variable "nat_policies" {
  type = map(object({
    name                  = string,
    audit_comment         = string,
    source_zones          = list(string),
    destination_zone      = string,
    destination_interface = string,
    source_addresses      = list(string),
    destination_addresses = list(string)
  }))
}

/* Security Policies ------------------------------------------------------ */
variable "security_policies" {
  type = map(object({
    name                  = string,
    audit_comment         = string,
    source_zones          = list(string),
    source_addresses      = list(string),
    source_users          = list(string),
    destination_zones     = list(string),
    destination_addresses = list(string),
    applications          = list(string),
    services              = list(string),
    categories            = list(string),
    action                = string
  }))
}
