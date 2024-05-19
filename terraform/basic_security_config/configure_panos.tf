/* Ethernet Interfaces ---------------------------------------------------- */
resource "panos_ethernet_interface" "mpls" {
  name                      = var.ethernet_interfaces["mpls"].name
  mode                      = var.ethernet_interfaces["mpls"].mode
  vsys                      = var.ethernet_interfaces["mpls"].vsys
  enable_dhcp               = true
  create_dhcp_default_route = true

  lifecycle {
    create_before_destroy = true
  }

}

resource "panos_ethernet_interface" "guest" {
  name       = var.ethernet_interfaces["guest"].name
  mode       = var.ethernet_interfaces["guest"].mode
  vsys       = var.ethernet_interfaces["guest"].vsys
  static_ips = var.ethernet_interfaces["guest"].static_ips

  lifecycle {
    create_before_destroy = true
  }

}

/* Virtual Routers -------------------------------------------------------- */
resource "panos_virtual_router" "default_vr" {
  name = var.vr_name
  interfaces = [
    panos_ethernet_interface.mpls.name,
    panos_ethernet_interface.guest.name
  ]

  lifecycle {
    create_before_destroy = true
  }

  depends_on = [
    panos_ethernet_interface.mpls,
    panos_ethernet_interface.guest
  ]

}

/* Security Zones --------------------------------------------------------- */
resource "panos_zone" "mpls" {
  name = var.zones["mpls"].name
  mode = var.zones["mpls"].mode
  interfaces = [
    panos_ethernet_interface.mpls.name
  ]

  lifecycle {
    create_before_destroy = true
  }

  depends_on = [panos_ethernet_interface.guest]
}

resource "panos_zone" "guest" {
  name = var.zones["guest"].name
  mode = var.zones["guest"].mode
  interfaces = [
    panos_ethernet_interface.guest.name
  ]

  lifecycle {
    create_before_destroy = true
  }
}

/* Service Objects -------------------------------------------------------- */
resource "panos_service_object" "tcp_221" {
  name             = var.service_objects["service_tcp_221"].name
  vsys             = var.service_objects["service_tcp_221"].vsys
  protocol         = var.service_objects["service_tcp_221"].protocol
  description      = var.service_objects["service_tcp_221"].description
  destination_port = var.service_objects["service_tcp_221"].destination_port

  lifecycle {
    create_before_destroy = true
  }
}

resource "panos_service_object" "tcp_222" {
  name             = var.service_objects["service_tcp_222"].name
  vsys             = var.service_objects["service_tcp_222"].vsys
  protocol         = var.service_objects["service_tcp_222"].protocol
  description      = var.service_objects["service_tcp_222"].description
  destination_port = var.service_objects["service_tcp_222"].destination_port

  lifecycle {
    create_before_destroy = true
  }
}

resource "panos_service_object" "http_81" {
  name             = var.service_objects["http_81"].name
  vsys             = var.service_objects["http_81"].vsys
  protocol         = var.service_objects["http_81"].protocol
  description      = var.service_objects["http_81"].description
  destination_port = var.service_objects["http_81"].destination_port

  lifecycle {
    create_before_destroy = true
  }
}

/* NAT Policies ----------------------------------------------------------- */
resource "panos_nat_rule_group" "test" {
  rule {
    name          = var.nat_policies["guest_mpls_out"].name
    audit_comment = var.nat_policies["guest_mpls_out"].audit_comment

    original_packet {
      source_zones          = var.nat_policies["guest_mpls_out"].source_zones
      destination_zone      = var.nat_policies["guest_mpls_out"].destination_zone
      destination_interface = var.nat_policies["guest_mpls_out"].destination_interface
      source_addresses      = var.nat_policies["guest_mpls_out"].source_addresses
      destination_addresses = var.nat_policies["guest_mpls_out"].destination_addresses
    }

    translated_packet {
      source {
        dynamic_ip_and_port {
          interface_address {
            interface = panos_ethernet_interface.mpls.name
          }
        }
      }
      destination {}
    }
  }

  lifecycle {
    create_before_destroy = true
  }

  depends_on = [
    panos_zone.guest,
    panos_zone.mpls,
    panos_ethernet_interface.mpls,
    panos_ethernet_interface.guest
  ]

}


/* Security Policies ------------------------------------------------------ */
resource "panos_security_policy" "guest_to_mpls_allow" {
  rule {
    name                  = var.security_policies["guest_to_mpls_allow"].name
    audit_comment         = var.security_policies["guest_to_mpls_allow"].audit_comment
    source_zones          = var.security_policies["guest_to_mpls_allow"].source_zones
    source_addresses      = var.security_policies["guest_to_mpls_allow"].source_addresses
    source_users          = var.security_policies["guest_to_mpls_allow"].source_users
    destination_zones     = var.security_policies["guest_to_mpls_allow"].destination_zones
    destination_addresses = var.security_policies["guest_to_mpls_allow"].destination_addresses
    applications          = var.security_policies["guest_to_mpls_allow"].applications
    services              = var.security_policies["guest_to_mpls_allow"].services
    categories            = var.security_policies["guest_to_mpls_allow"].categories
    action                = var.security_policies["guest_to_mpls_allow"].action
  }

  lifecycle {
    create_before_destroy = true
  }

  depends_on = [
    panos_zone.guest,
    panos_zone.mpls,
    panos_ethernet_interface.mpls,
    panos_ethernet_interface.guest
  ]
}
