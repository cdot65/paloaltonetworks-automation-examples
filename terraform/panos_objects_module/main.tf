module "objects" {
  source = "./modules/objects"

  hostname = var.hostname
  username = var.username
  password = var.password
  vsys     = "vsys1"

  address_objects = {
    "ntp1" = {
      value       = "10.0.0.1"
      description = "NTP Server 1"
      tags        = ["internal", "ntp"]
    },
    "ntp2" = {
      value       = "10.0.0.2"
      description = "NTP Server 2"
      tags        = ["internal", "ntp"]
    },
    "localnet" = {
      value       = "192.168.80.0/24"
      description = "The 192.168.80 network"
      tags        = ["internal", "dmz"]
    }
  }

  static_address_groups = {
    "static ntp grp" = {
      description      = "My NTP servers"
      static_addresses = [
        "ntp1",
        "ntp2",
      ]
      tags = []
    }
  }

  dynamic_address_groups = {
    "dynamic grp" = {
      description   = "My internal NTP servers"
      dynamic_match = "'internal' and 'ntp'"
      tags          = []
    }
  }

  service_objects = {
    "my_service" = {
      protocol         = "tcp"
      description      = "My service object"
      source_port      = "2000-2049,2051-2099"
      destination_port = "32123"
      tags             = ["internal", "dmz"]
    }
  }

  tags = {
    "internal" = {
      color   = "color5"
      comment = "Internal resources"
    },
    "ntp" = {
      color   = "color3"
      comment = "NTP servers"
    },
    "dmz" = {
      color   = "color4"
      comment = "DMZ resources"
    },
    "Automation" = {
      color   = "color6"
      comment = "Automated tags"
    }
  }

  ip_tags = {
    "example1" = {
      ip   = "10.2.3.4"
      tags = ["Automation"]
    }
  }
}
