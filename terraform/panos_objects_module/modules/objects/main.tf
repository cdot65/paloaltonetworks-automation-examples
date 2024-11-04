# Address Objects
resource "panos_address_object" "address_objs" {
  for_each = var.address_objects

  name        = each.key
  value       = each.value.value
  description = each.value.description
  vsys        = var.vsys
  tags        = each.value.tags

  lifecycle {
    create_before_destroy = true
  }
}

# Static Address Groups
resource "panos_address_group" "static_groups" {
  for_each = var.static_address_groups

  name             = each.key
  description      = each.value.description
  vsys             = var.vsys
  static_addresses = each.value.static_addresses
  tags             = each.value.tags

  lifecycle {
    create_before_destroy = true
  }
}

# Dynamic Address Groups
resource "panos_address_group" "dynamic_groups" {
  for_each = var.dynamic_address_groups

  name          = each.key
  description   = each.value.description
  vsys          = var.vsys
  dynamic_match = each.value.dynamic_match
  tags          = each.value.tags

  lifecycle {
    create_before_destroy = true
  }
}

# Service Objects
resource "panos_service_object" "service_objs" {
  for_each = var.service_objects

  name             = each.key
  vsys             = var.vsys
  protocol         = each.value.protocol
  description      = each.value.description
  source_port      = each.value.source_port
  destination_port = each.value.destination_port
  tags             = each.value.tags

  lifecycle {
    create_before_destroy = true
  }
}

# Tags
resource "panos_administrative_tag" "tags" {
  for_each = var.tags

  name    = each.key
  vsys    = var.vsys
  color   = each.value.color
  comment = each.value.comment

  lifecycle {
    create_before_destroy = true
  }
}

# Dynamic Address Group Entries (IP Tags)
resource "panos_ip_tag" "ip_tags" {
  for_each = var.ip_tags

  ip   = each.value.ip
  vsys = var.vsys
  tags = each.value.tags

  lifecycle {
    create_before_destroy = true
  }
}
