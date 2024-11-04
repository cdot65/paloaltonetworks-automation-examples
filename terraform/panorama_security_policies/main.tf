resource "panos_panorama_address_object" "example" {
  name         = "localnet"
  value        = "192.168.80.0/24"
  description  = "The 192.168.80 network"
  tags = ["internal", "dmz"]
  device_group = var.device_group

  lifecycle {
    create_before_destroy = true
  }
}

resource "panos_panorama_administrative_tag" "example" {
  name    = "tag1"
  color   = "color5"
  comment = "Internal resources"

  # Panorama tags are globally defined; no device group is needed

  lifecycle {
    create_before_destroy = true
  }
}

resource "panos_zone" "bizdev" {
  name     = "bizdev"
  template = panos_panorama_template.tmpl1.name
  mode     = "layer3"
  interfaces = [
    panos_panorama_ethernet_interface.e2.name,
    panos_panorama_ethernet_interface.e3.name,
  ]
  enable_user_id = true
  exclude_acls = ["192.168.0.0/16"]

  lifecycle {
    create_before_destroy = true
  }
}



resource "panos_panorama_security_rule_group" "example1" {
  device_group       = var.device_group
  position_keyword   = "before"
  position_reference = panos_panorama_security_rule_group.example2.rule[0].name

  rule {
    name   = "Allow bizdev to dmz"
    source_zones = [panos_zone.bizdev.name]
    source_addresses = ["any"]
    source_users = ["any"]
    destination_zones = ["any"]
    destination_addresses = ["any"]
    applications = ["any"]
    services = ["application-default"]
    categories = ["any"]
    action = "allow"
  }
  rule {
    name   = "Deny sales to eng"
    source_zones = ["any"]
    source_addresses = ["any"]
    source_users = ["any"]
    destination_zones = ["any"]
    destination_addresses = ["any"]
    applications = ["any"]
    services = ["application-default"]
    categories = ["any"]
    action = "deny"
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "panos_panorama_security_rule_group" "example2" {
  device_group     = var.device_group
  position_keyword = "bottom"

  rule {
    name   = "Deny everything else"
    source_zones = ["any"]
    source_addresses = ["any"]
    source_users = ["any"]
    destination_zones = ["any"]
    destination_addresses = ["any"]
    applications = ["any"]
    services = ["application-default"]
    categories = ["any"]
    action = "deny"
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "panos_panorama_template" "tmpl1" {
  name = var.template

  lifecycle {
    create_before_destroy = true
  }
}

resource "panos_panorama_ethernet_interface" "e2" {
  template = panos_panorama_template.tmpl1.name
  name     = "ethernet1/6"
  mode     = "layer3"

  lifecycle {
    create_before_destroy = true
  }
}

resource "panos_panorama_ethernet_interface" "e3" {
  template = panos_panorama_template.tmpl1.name
  name     = "ethernet1/7"
  mode     = "layer3"

  lifecycle {
    create_before_destroy = true
  }
}
