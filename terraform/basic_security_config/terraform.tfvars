/* Firewall Connectivity -------------------------------------------------- */
firewall = {
  fw_ip    = "austin-fw3.cdot.io"
  username = "officehours"
  password = "paloalto123"
}

/* Ethernet Interfaces ---------------------------------------------------- */
ethernet_interfaces = {
  mpls = {
    name       = "ethernet1/7"
    mode       = "layer3"
    vsys       = "vsys1"
    static_ips = ["216.254.243.1/24"]
  }
  guest = {
    name       = "ethernet1/8"
    mode       = "layer3"
    vsys       = "vsys1"
    static_ips = ["192.168.1.1/24"]
  }
}

/* Virtual Routers -------------------------------------------------------- */
vr_name = "lab"

/* Security Zones --------------------------------------------------------- */
zones = {
  mpls = {
    name = "mpls"
    mode = "layer3"
  }
  guest = {
    name = "guest"
    mode = "layer3"
  }
}

/* Service Objects -------------------------------------------------------- */
service_objects = {
  service_tcp_221 = {
    name             = "service-tcp-221"
    vsys             = "vsys1"
    protocol         = "tcp"
    description      = "Service object to map port 22 to 221"
    destination_port = "221"
  }
  service_tcp_222 = {
    name             = "service-tcp-222"
    vsys             = "vsys1"
    protocol         = "tcp"
    description      = "Service object to map port 22 to 222"
    destination_port = "222"
  }
  http_81 = {
    name             = "service-tcp-81"
    vsys             = "vsys1"
    protocol         = "tcp"
    description      = "Service object to map port 80 to 81"
    destination_port = "81"
  }
}

/* NAT Policies ----------------------------------------------------------- */
nat_policies = {
  guest_mpls_out = {
    name                  = "guest-mpls-out"
    audit_comment         = "Pushed by Terraform"
    source_zones          = ["guest"]
    destination_zone      = "mpls"
    destination_interface = "ethernet1/7"
    source_addresses      = ["any"]
    destination_addresses = ["any"]
  }
}

/* Security Policies ------------------------------------------------------ */
security_policies = {
  guest_to_mpls_allow = {
    name                  = "guest-to-mpls-allow"
    audit_comment         = "Initial config"
    source_zones          = ["guest"]
    source_addresses      = ["any"]
    source_users          = ["any"]
    destination_zones     = ["mpls"]
    destination_addresses = ["any"]
    applications          = ["any"]
    services              = ["application-default"]
    categories            = ["any"]
    action                = "allow"
  }
}
