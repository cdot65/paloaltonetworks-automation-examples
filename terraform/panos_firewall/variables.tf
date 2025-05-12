# ----------------------------------------------------------------------------
# NGFW appliance
# ----------------------------------------------------------------------------
variable "ngfw" {
  type = object({
    hostname = string
    username = string
    password = string
  })
}

# ----------------------------------------------------------------------------
# DNS Settings
# ----------------------------------------------------------------------------
variable "dns_settings" {
  type = map(object({
    location = optional(object({
      system = optional(object({
        ngfw_device = optional(string)
      })),
      template = optional(object({
        name = optional(string)
        ngfw_device = optional(string)
        panorama_device = optional(string)
      })),
      template_stack = optional(object({
        name = optional(string)
        ngfw_device = optional(string)
        panorama_device = optional(string)
      }))
    }))
    dns_settings = optional(object({
      servers = optional(object({
        primary = optional(string) # Primary DNS server IP
        secondary = optional(string) # Secondary DNS server IP
      }))
    }))
    fqdn_refresh_time = optional(number) # Periodic Timer for refreshing expired FQDN object entries
  }))
}

# # ----------------------------------------------------------------------------
# # NTP Settings
# # ----------------------------------------------------------------------------
# variable "ntp_settings" {
#   description = "Configuration for multiple panos_ntp_settings resources"
#   type = map(object({
#     location = object({
#       system = optional(object({
#         ngfw_device = optional(string)
#       }))
#       template = optional(object({
#         name            = string
#         ngfw_device     = optional(string)
#         panorama_device = optional(string)
#       }))
#       template_stack = optional(object({
#         name            = string
#         ngfw_device     = optional(string)
#         panorama_device = optional(string)
#       }))
#     })
#     ntp_servers = optional(object({
#       primary_ntp_server = optional(object({
#         ntp_server_address = string
#         authentication_type = optional(object({
#           autokey = optional(string)
#           none    = optional(string)
#           symmetric_key = optional(object({
#             key_id = optional(number)
#             md5 = optional(object({
#               authentication_key = optional(string)
#             }))
#             sha1 = optional(object({
#               authentication_key = optional(string)
#             }))
#           }))
#         }))
#       }))
#       secondary_ntp_server = optional(object({
#         ntp_server_address = string
#         authentication_type = optional(object({
#           autokey = optional(string)
#           none    = optional(string)
#           symmetric_key = optional(object({
#             key_id = optional(number)
#             md5 = optional(object({
#               authentication_key = optional(string)
#             }))
#             sha1 = optional(object({
#               authentication_key = optional(string)
#             }))
#           }))
#         }))
#       }))
#     }))
#   }))
# }
#
# # ----------------------------------------------------------------------------
# # NGFW Templates
# # ----------------------------------------------------------------------------
# variable "templates" {
#   type = map(object({
#     description = string
#     name        = string
#   }))
# }
#
# # ----------------------------------------------------------------------------
# # NGFW Template Stacks
# # ----------------------------------------------------------------------------
# variable "template_stacks" {
#   type = map(object({
#     description  = string
#     name         = string
#     devices      = list(string)
#     default_vsys = optional(string)
#   }))
# }
#
# # ----------------------------------------------------------------------------
# # NGFW Template Variables
# # ----------------------------------------------------------------------------
# variable "template_variables" {
#   type = map(object({
#     description = string
#     name        = string
#     location = object({
#       template = object({
#         name            = string
#         panorama_device = string
#       })
#     })
#     type = object({
#       as_number       = optional(string)
#       device_id       = optional(string)
#       device_priority = optional(string)
#       egress_max      = optional(string)
#       fqdn            = optional(string)
#       group_id        = optional(string)
#       interface       = optional(string)
#       ip_netmask      = optional(string)
#       ip_range        = optional(string)
#       link_tag        = optional(string)
#       qos_profile     = optional(string)
#     })
#   }))
# }
#
# # ----------------------------------------------------------------------------
# # NGFW Template Interface Management Profile
# # ----------------------------------------------------------------------------
# variable "interface_management_profiles" {
#   type = map(object({
#     location = object({
#       ngfw = optional(object({
#         ngfw_device = optional(string)
#       }))
#       template = optional(object({
#         name            = string
#         ngfw_device     = optional(string)
#         panorama_device = optional(string)
#       }))
#       template_stack = optional(object({
#         name            = string
#         ngfw_device     = optional(string)
#         panorama_device = optional(string)
#       }))
#     })
#     name                       = string
#     http                       = optional(bool)
#     http_ocsp                  = optional(bool)
#     https                      = optional(bool)
#     permitted_ips              = optional(list(string))
#     ping                       = optional(bool)
#     response_pages             = optional(bool)
#     snmp                       = optional(bool)
#     ssh                        = optional(bool)
#     telnet                     = optional(bool)
#     userid_service             = optional(bool)
#     userid_syslog_listener_ssl = optional(bool)
#     userid_syslog_listener_udp = optional(bool)
#   }))
# }
#
# # ----------------------------------------------------------------------------
# # NGFW Template Ethernet Interfaces
# # ----------------------------------------------------------------------------
# variable "ethernet_interfaces" {
#   type = map(object({
#     name = string
#     location = optional(object({
#       ngfw = optional(object({
#         ngfw_device = optional(string)
#       })),
#       template = optional(object({
#         vsys            = string
#         name            = optional(string)
#         ngfw_device     = optional(string)
#         panorama_device = optional(string)
#       })),
#       template_stack = optional(object({
#         name            = optional(string)
#         ngfw_device     = optional(string)
#         panorama_device = optional(string)
#       }))
#     }))
#     comment = optional(string)
#     ha      = optional(object({})), # Not defined in the documentation
#     layer3 = optional(object({
#       adjust_tcp_mss = optional(object({
#         enable              = optional(bool)
#         ipv4_mss_adjustment = optional(number)
#         ipv6_mss_adjustment = optional(number)
#       })),
#       arp = optional(list(object({
#         name       = string
#         hw_address = optional(string)
#       }))),
#       bonjour = optional(object({
#         enable = optional(bool)
#       })),
#       dhcp_client = optional(object({
#         create_default_route = optional(bool)
#         default_route_metric = optional(number)
#         enable               = optional(bool)
#         send_hostname = optional(object({
#           enable   = optional(bool)
#           hostname = optional(string)
#         }))
#       })),
#       interface_management_profile = optional(string)
#       ips = optional(list(object({
#         name          = string
#         sdwan_gateway = optional(string)
#       }))),
#       ipv6 = optional(object({
#         addresses = optional(list(object({
#           name = string
#           advertise = optional(object({
#             auto_config_flag   = optional(bool)
#             enable             = optional(bool)
#             onlink_flag        = optional(bool)
#             preferred_lifetime = optional(string)
#             valid_lifetime     = optional(string)
#           })),
#           anycast             = optional(string)
#           enable_on_interface = optional(bool)
#           prefix              = optional(string)
#         }))),
#         dns_server = optional(object({
#           dns_support = optional(object({
#             enable = optional(bool)
#             server = optional(list(object({
#               name     = string
#               lifetime = optional(number) # (4-3600 seconds)
#             }))),
#             suffix = optional(list(object({
#               name     = string
#               lifetime = optional(number) # (4-3600 seconds)
#             })))
#           })),
#           enable = optional(bool)
#           source = optional(object({
#             dhcpv6 = optional(object({
#               prefix_pool = optional(string)
#             })),
#             manual = optional(object({
#               suffix = optional(list(object({
#                 name     = string
#                 lifetime = optional(number) # (4-3600 seconds)
#               })))
#             }))
#           }))
#         })),
#         enabled      = optional(bool)
#         interface_id = optional(string)
#         neighbor_discovery = optional(object({
#           dad_attempts       = optional(number)
#           enable_dad         = optional(bool)
#           enable_ndp_monitor = optional(bool)
#           neighbor = optional(list(object({
#             name       = string
#             hw_address = optional(string)
#           }))),
#           ns_interval    = optional(number)
#           reachable_time = optional(number)
#           router_advertisement = optional(object({
#             enable                   = optional(bool)
#             enable_consistency_check = optional(bool)
#             hop_limit                = optional(string)
#             lifetime                 = optional(number)
#             link_mtu                 = optional(string)
#             managed_flag             = optional(bool)
#             max_interval             = optional(number)
#             min_interval             = optional(number)
#             other_flag               = optional(bool)
#             reachable_time           = optional(string)
#             retransmission_timer     = optional(string)
#             router_preference        = optional(string)
#           }))
#         }))
#       })),
#       lldp = optional(object({
#         enable  = optional(bool)
#         profile = optional(string)
#       })),
#       mtu             = optional(number)
#       ndp_proxy       = optional(bool)
#       netflow_profile = optional(string)
#       sdwan_link_settings = optional(object({
#         enable                  = optional(bool)
#         sdwan_interface_profile = optional(string)
#         upstream_nat = optional(object({
#           enable    = optional(bool)
#           static_ip = optional(string)
#         }))
#       })),
#       untagged_sub_interface = optional(bool)
#     })),
#     link_duplex = optional(string)
#     link_speed  = optional(string)
#     link_state  = optional(string)
#     poe = optional(object({
#       enabled        = optional(bool)
#       reserved_power = optional(number)
#     })),
#     tap = optional(object({
#       netflow_profile = optional(string)
#     }))
#   }))
# }
#
# # ----------------------------------------------------------------------------
# # NGFW Template Loopback Interfaces
# # ----------------------------------------------------------------------------
# variable "loopback_interfaces" {
#   type = map(object({
#     location = object({
#       ngfw = optional(object({
#         ngfw_device = optional(string)
#       }))
#       template = optional(object({
#         name            = string
#         ngfw_device     = optional(string)
#         panorama_device = optional(string)
#       }))
#       template_stack = optional(object({
#         name            = string
#         ngfw_device     = optional(string)
#         panorama_device = optional(string)
#       }))
#     })
#     name = string
#     adjust_tcp_mss = optional(object({
#       enable              = optional(bool)
#       ipv4_mss_adjustment = optional(number)
#       ipv6_mss_adjustment = optional(number)
#     }))
#     comment                      = optional(string)
#     interface_management_profile = optional(string)
#     ips                          = optional(list(string))
#     ipv6 = optional(object({
#       addresses = optional(list(object({
#         name                = string
#         enable_on_interface = optional(bool)
#       })))
#       enabled = optional(bool)
#     }))
#     mtu             = optional(number)
#     netflow_profile = optional(string)
#   }))
# }
#
# # ----------------------------------------------------------------------------
# # NGFW Template Security Zones
# # ----------------------------------------------------------------------------
# variable "zones" {
#   type = map(object({
#     name = string
#     location = object({
#       from_panorama_vsys = optional(object({
#         vsys = optional(string)
#       })),
#       template = optional(object({
#         name            = optional(string)
#         ngfw_device     = optional(string)
#         panorama_device = optional(string)
#         vsys            = optional(string)
#       })),
#       template_stack = optional(object({
#         name            = optional(string)
#         ngfw_device     = optional(string)
#         panorama_device = optional(string)
#         vsys            = optional(string)
#       })),
#       vsys = optional(object({
#         name        = optional(string)
#         ngfw_device = optional(string)
#       }))
#     })
#     device_acl = optional(object({
#       exclude_list = optional(list(string))
#       include_list = optional(list(string))
#     }))
#     enable_device_identification = optional(bool)
#     enable_user_identification   = optional(bool)
#     network = optional(object({
#       enable_packet_buffer_protection = optional(bool)
#       layer2                          = optional(list(string))
#       layer3                          = optional(list(string))
#       log_setting                     = optional(list(string))
#       tap                             = optional(list(string))
#       virtual_wire                    = optional(list(string))
#       zone_protection_profile         = optional(list(string))
#     }))
#     user_acl = optional(object({
#       exclude_list = optional(list(string))
#       include_list = optional(list(string))
#     }))
#   }))
# }
#
# # ----------------------------------------------------------------------------
# # NGFW Template Virtual Routers
# # ----------------------------------------------------------------------------
# variable "virtual_routers" {
#   type = map(object({
#     name = string
#     location = optional(object({
#       ngfw = optional(object({
#         ngfw_device = optional(string)
#       }))
#       template = optional(object({
#         name            = optional(string)
#         ngfw_device     = optional(string)
#         panorama_device = optional(string)
#       }))
#       template_stack = optional(object({
#         name            = optional(string)
#         ngfw_device     = optional(string)
#         panorama_device = optional(string)
#       }))
#     }))
#     administrative_distances = optional(object({
#       ebgp        = optional(number)
#       ibgp        = optional(number)
#       ospf_ext    = optional(number)
#       ospf_int    = optional(number)
#       ospfv3_ext  = optional(number)
#       ospfv3_int  = optional(number)
#       rip         = optional(number)
#       static      = optional(number)
#       static_ipv6 = optional(number)
#     }))
#     ecmp = optional(object({
#       enable             = optional(bool)
#       max_paths          = optional(number)
#       strict_source_path = optional(bool)
#       symmetric_return   = optional(bool)
#       algorithm = optional(object({
#         balanced_round_robin = optional(object({})), # No content provided in the documentation
#         ip_hash = optional(object({
#           hash_seed = optional(number)
#           src_only  = optional(bool)
#           use_port  = optional(bool)
#         })),
#         ip_modulo = optional(object({})), # No content provided in the documentation
#         weighted_round_robin = optional(object({
#           interfaces = optional(list(object({
#             name   = string
#             weight = optional(number)
#           })))
#         }))
#       }))
#     }))
#     interfaces = optional(list(string))
#     protocol = optional(object({
#       bgp    = optional(object({ enable = optional(bool) }))
#       ospf   = optional(object({ enable = optional(bool) }))
#       ospfv3 = optional(object({ enable = optional(bool) }))
#       rip    = optional(object({ enable = optional(bool) }))
#     }))
#     routing_table = optional(object({
#       ip = optional(object({
#         static_routes = optional(list(object({
#           name        = string
#           admin_dist  = optional(number)
#           destination = optional(string)
#           interface   = optional(string)
#           metric      = optional(number)
#           next_hop = optional(object({
#             fqdn       = optional(string)
#             ip_address = optional(string)
#             next_vr    = optional(string)
#             tunnel     = optional(string)
#           }))
#           route_table = optional(string)
#         })))
#       }))
#       ipv6 = optional(object({
#         static_routes = optional(list(object({
#           name        = string
#           admin_dist  = optional(number)
#           destination = optional(string)
#           interface   = optional(string)
#           metric      = optional(number)
#           next_hop = optional(object({
#             fqdn         = optional(string)
#             ipv6_address = optional(string)
#             next_vr      = optional(string)
#             tunnel       = optional(string)
#           }))
#           route_table = optional(string)
#         })))
#       }))
#     }))
#   }))
# }
#
# # ----------------------------------------------------------------------------
# # NGFW Device Groups
# # ----------------------------------------------------------------------------
# variable "device_groups" {
#   type = map(object({
#     location = optional(object({
#       ngfw = optional(object({
#         panorama_device = optional(string)
#       }))
#     }))
#     name = optional(string) # The device group who is being set up
#     devices = optional(list(object({
#       name = optional(string)
#     })))
#   }))
# }
#
# # ----------------------------------------------------------------------------
# # NGFW Device Group Parents
# # ----------------------------------------------------------------------------
# variable "device_group_parents" {
#   type = map(object({
#     location = optional(object({
#       ngfw = optional(object({
#         panorama_device = optional(string)
#       }))
#     }))
#     device_group = optional(string) # The child device group
#     parent       = optional(string) # The parent device group. Leaving empty moves the device group under 'shared'.
#   }))
# }
#
# # ----------------------------------------------------------------------------
# # NGFW Device Group Administrative Tags
# # ----------------------------------------------------------------------------
# variable "administrative_tags" {
#   type = map(object({
#     location = object({
#       device_group = optional(object({
#         name            = optional(string) # Device group name
#         panorama_device = optional(string) # NGFW device
#       })),
#       from_panorama_shared = optional(bool) # Located in shared in the config pushed from NGFW
#       from_panorama_vsys = optional(object({
#         vsys = optional(string) # The vsys
#       })),
#       shared = optional(bool) # Located in shared
#       vsys = optional(object({
#         name        = optional(string) # The vsys name
#         ngfw_device = optional(string) # The NGFW device
#       }))
#     })
#     name     = string           # The name of the tag
#     color    = optional(string) # The color of the tag
#     comments = optional(string) # Additional comments for the tag
#   }))
# }
#
# # ----------------------------------------------------------------------------
# # NGFW Device Group Address Objects
# # ----------------------------------------------------------------------------
# variable "addresses" {
#   type = map(object({
#     location = object({
#       device_group = optional(object({
#         name            = optional(string) # Device group name
#         panorama_device = optional(string) # NGFW device
#       })),
#       from_panorama_shared = optional(bool) # Located in shared in the config pushed from NGFW
#       from_panorama_vsys = optional(object({
#         vsys = optional(string) # The vsys
#       })),
#       shared = optional(bool) # Located in shared
#       vsys = optional(object({
#         name        = optional(string) # The vsys name
#         ngfw_device = optional(string) # The NGFW device
#       }))
#     })
#     addresses = map(object({
#       description = optional(string)       # Description of the address
#       fqdn        = optional(string)       # FQDN value
#       ip_netmask  = optional(string)       # IP/netmask value
#       ip_range    = optional(string)       # IP range value
#       ip_wildcard = optional(string)       # IP wildcard value
#       tags        = optional(list(string)) # Administrative tags
#     }))
#   }))
# }
#
# # ----------------------------------------------------------------------------
# # NGFW Device Group Address Groups
# # ----------------------------------------------------------------------------
# variable "address_groups" {
#   type = map(object({
#     location = object({
#       device_group = object({
#         name            = string
#         panorama_device = optional(string)
#       })
#       from_panorama_shared = optional(bool)
#       from_panorama_vsys = optional(object({
#         vsys = string
#       }))
#       shared = optional(bool)
#       vsys = optional(object({
#         name        = string
#         ngfw_device = optional(string)
#       }))
#     })
#     groups = map(object({
#       name        = string
#       description = optional(string)
#       static      = optional(list(string))
#       dynamic     = optional(string)
#       tags        = optional(list(string))
#     }))
#   }))
# }
#
# # ----------------------------------------------------------------------------
# # NGFW Device Group Services
# # ----------------------------------------------------------------------------
# variable "services" {
#   type = map(object({
#     location = object({
#       device_group = optional(object({
#         name            = string
#         panorama_device = optional(string)
#       }))
#       shared               = optional(bool)
#       from_panorama_shared = optional(bool)
#       vsys = optional(object({
#         name        = string
#         ngfw_device = optional(string)
#       }))
#     })
#     services = map(object({
#       name        = string
#       description = optional(string)
#       tags        = optional(list(string))
#       protocol = optional(object({
#         tcp = optional(object({
#           destination_port = string
#           source_port      = optional(string)
#           override = optional(object({
#             halfclose_timeout = optional(number)
#             timeout           = optional(number)
#             timewait_timeout  = optional(number)
#           }))
#         }))
#         udp = optional(object({
#           destination_port = string
#           source_port      = optional(string)
#           override = optional(object({
#             timeout = optional(number)
#           }))
#         }))
#       }))
#     }))
#   }))
# }
#
# # ----------------------------------------------------------------------------
# # NGFW Device Group Service Groups
# # ----------------------------------------------------------------------------
# variable "service_groups" {
#   type = map(object({
#     location = object({
#       device_group = optional(object({
#         name            = string
#         panorama_device = optional(string)
#       }))
#       shared               = optional(bool)
#       from_panorama_shared = optional(bool)
#       vsys = optional(object({
#         name        = string
#         ngfw_device = optional(string)
#       }))
#     })
#     groups = map(object({
#       name        = string
#       description = optional(string)
#       members     = optional(list(string))
#       tags        = optional(list(string))
#     }))
#   }))
# }
#
# # ----------------------------------------------------------------------------
# # NGFW Device Group Security Policies
# # ----------------------------------------------------------------------------
# variable "security_policies" {
#   type = map(object({
#     location = object({
#       device_group = optional(object({
#         name            = string
#         panorama_device = optional(string)
#         rulebase        = optional(string)
#       }))
#       shared = optional(object({
#         rulebase = optional(string)
#       }))
#       from_panorama_shared = optional(bool)
#       vsys = optional(object({
#         name        = string
#         ngfw_device = optional(string)
#         rulebase    = optional(string)
#       }))
#     })
#     policy_rules = list(object({
#       name                               = string
#       description                        = optional(string)
#       tags                               = optional(list(string))
#       source_zones                       = optional(list(string))
#       source_addresses                   = optional(list(string))
#       source_users                       = optional(list(string))
#       source_hips                        = optional(list(string))
#       destination_zones                  = optional(list(string))
#       destination_addresses              = optional(list(string))
#       destination_hips                   = optional(list(string))
#       applications                       = optional(list(string))
#       services                           = optional(list(string))
#       categories                         = optional(list(string))
#       action                             = optional(string)
#       log_setting                        = optional(string)
#       log_start                          = optional(bool)
#       log_end                            = optional(bool)
#       disabled                           = optional(bool)
#       disable_server_response_inspection = optional(bool)
#       negate_source                      = optional(bool)
#       negate_destination                 = optional(bool)
#       icmp_unreachable                   = optional(bool)
#       rule_type                          = optional(string)
#       uuid                               = optional(string)
#       profile_setting = optional(object({
#         group = optional(string)
#         profiles = optional(object({
#           virus             = optional(list(string))
#           spyware           = optional(list(string))
#           vulnerability     = optional(list(string))
#           url_filtering     = optional(list(string))
#           file_blocking     = optional(list(string))
#           wildfire_analysis = optional(list(string))
#           data_filtering    = optional(list(string))
#         }))
#       }))
#     }))
#   }))
# }
#
# # ----------------------------------------------------------------------------
# # NGFW Device Group Custom URL Categories
# # ----------------------------------------------------------------------------
# variable "custom_url_categories" {
#  type = map(object({
#    location = object({
#      device_group = optional(object({
#        name            = string
#        panorama_device = optional(string)
#      }))
#      shared               = optional(bool)
#      from_panorama_shared = optional(bool)
#      vsys = optional(object({
#        name        = string
#        ngfw_device = optional(string)
#      }))
#    })
#    categories = map(object({
#      name              = string
#      description       = optional(string)
#      type              = optional(string)
#      list              = optional(list(string))
#      disable_override  = optional(bool)
#    }))
#  }))
# }