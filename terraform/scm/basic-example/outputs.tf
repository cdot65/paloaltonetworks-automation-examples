# ============================================================================
# Outputs - Austin Folder Resources
# ============================================================================

# ----------------------------------------------------------------------------
# Tags Outputs
# ----------------------------------------------------------------------------

output "tags" {
  description = "All created tags with their IDs"
  value = {
    production  = scm_tag.production.id
    development = scm_tag.development.id
    web_tier    = scm_tag.web_tier.id
    app_tier    = scm_tag.app_tier.id
    data_tier   = scm_tag.data_tier.id
    dmz         = scm_tag.dmz.id
  }
}

# ----------------------------------------------------------------------------
# Address Objects Outputs
# ----------------------------------------------------------------------------

output "address_objects_web_tier" {
  description = "Web tier address objects"
  value = {
    web_prod_1 = {
      id         = scm_address.web_prod_1.id
      name       = scm_address.web_prod_1.name
      ip_netmask = scm_address.web_prod_1.ip_netmask
      tags       = scm_address.web_prod_1.tag
    }
    web_prod_2 = {
      id         = scm_address.web_prod_2.id
      name       = scm_address.web_prod_2.name
      ip_netmask = scm_address.web_prod_2.ip_netmask
      tags       = scm_address.web_prod_2.tag
    }
    web_prod_subnet = {
      id         = scm_address.web_prod_subnet.id
      name       = scm_address.web_prod_subnet.name
      ip_netmask = scm_address.web_prod_subnet.ip_netmask
      tags       = scm_address.web_prod_subnet.tag
    }
    web_dev_1 = {
      id         = scm_address.web_dev_1.id
      name       = scm_address.web_dev_1.name
      ip_netmask = scm_address.web_dev_1.ip_netmask
      tags       = scm_address.web_dev_1.tag
    }
    web_dev_subnet = {
      id         = scm_address.web_dev_subnet.id
      name       = scm_address.web_dev_subnet.name
      ip_netmask = scm_address.web_dev_subnet.ip_netmask
      tags       = scm_address.web_dev_subnet.tag
    }
  }
}

output "address_objects_app_tier" {
  description = "Application tier address objects"
  value = {
    app_prod_1 = {
      id         = scm_address.app_prod_1.id
      name       = scm_address.app_prod_1.name
      ip_netmask = scm_address.app_prod_1.ip_netmask
      tags       = scm_address.app_prod_1.tag
    }
    app_prod_2 = {
      id         = scm_address.app_prod_2.id
      name       = scm_address.app_prod_2.name
      ip_netmask = scm_address.app_prod_2.ip_netmask
      tags       = scm_address.app_prod_2.tag
    }
    app_prod_range = {
      id       = scm_address.app_prod_range.id
      name     = scm_address.app_prod_range.name
      ip_range = scm_address.app_prod_range.ip_range
      tags     = scm_address.app_prod_range.tag
    }
    app_dev_subnet = {
      id         = scm_address.app_dev_subnet.id
      name       = scm_address.app_dev_subnet.name
      ip_netmask = scm_address.app_dev_subnet.ip_netmask
      tags       = scm_address.app_dev_subnet.tag
    }
  }
}

output "address_objects_data_tier" {
  description = "Data tier address objects"
  value = {
    db_prod_1 = {
      id         = scm_address.db_prod_1.id
      name       = scm_address.db_prod_1.name
      ip_netmask = scm_address.db_prod_1.ip_netmask
      tags       = scm_address.db_prod_1.tag
    }
    db_prod_2 = {
      id         = scm_address.db_prod_2.id
      name       = scm_address.db_prod_2.name
      ip_netmask = scm_address.db_prod_2.ip_netmask
      tags       = scm_address.db_prod_2.tag
    }
    db_prod_range = {
      id       = scm_address.db_prod_range.id
      name     = scm_address.db_prod_range.name
      ip_range = scm_address.db_prod_range.ip_range
      tags     = scm_address.db_prod_range.tag
    }
    db_dev_subnet = {
      id         = scm_address.db_dev_subnet.id
      name       = scm_address.db_dev_subnet.name
      ip_netmask = scm_address.db_dev_subnet.ip_netmask
      tags       = scm_address.db_dev_subnet.tag
    }
  }
}

output "address_objects_dmz" {
  description = "DMZ address objects"
  value = {
    dmz_proxy_1 = {
      id         = scm_address.dmz_proxy_1.id
      name       = scm_address.dmz_proxy_1.name
      ip_netmask = scm_address.dmz_proxy_1.ip_netmask
      tags       = scm_address.dmz_proxy_1.tag
    }
    dmz_proxy_2 = {
      id         = scm_address.dmz_proxy_2.id
      name       = scm_address.dmz_proxy_2.name
      ip_netmask = scm_address.dmz_proxy_2.ip_netmask
      tags       = scm_address.dmz_proxy_2.tag
    }
    dmz_subnet = {
      id         = scm_address.dmz_subnet.id
      name       = scm_address.dmz_subnet.name
      ip_netmask = scm_address.dmz_subnet.ip_netmask
      tags       = scm_address.dmz_subnet.tag
    }
  }
}

output "address_objects_external" {
  description = "External FQDN address objects"
  value = {
    api_endpoint = {
      id   = scm_address.api_endpoint.id
      name = scm_address.api_endpoint.name
      fqdn = scm_address.api_endpoint.fqdn
      tags = scm_address.api_endpoint.tag
    }
    cdn_endpoint = {
      id   = scm_address.cdn_endpoint.id
      name = scm_address.cdn_endpoint.name
      fqdn = scm_address.cdn_endpoint.fqdn
      tags = scm_address.cdn_endpoint.tag
    }
  }
}

# ----------------------------------------------------------------------------
# Address Groups Outputs
# ----------------------------------------------------------------------------

output "address_groups_production" {
  description = "Production environment address groups"
  value = {
    prod_web_servers = {
      id      = scm_address_group.prod_web_servers.id
      name    = scm_address_group.prod_web_servers.name
      members = scm_address_group.prod_web_servers.static
      tags    = scm_address_group.prod_web_servers.tag
    }
    prod_app_servers = {
      id      = scm_address_group.prod_app_servers.id
      name    = scm_address_group.prod_app_servers.name
      members = scm_address_group.prod_app_servers.static
      tags    = scm_address_group.prod_app_servers.tag
    }
    prod_db_servers = {
      id      = scm_address_group.prod_db_servers.id
      name    = scm_address_group.prod_db_servers.name
      members = scm_address_group.prod_db_servers.static
      tags    = scm_address_group.prod_db_servers.tag
    }
  }
}

output "address_groups_development" {
  description = "Development environment address groups"
  value = {
    dev_web_servers = {
      id      = scm_address_group.dev_web_servers.id
      name    = scm_address_group.dev_web_servers.name
      members = scm_address_group.dev_web_servers.static
      tags    = scm_address_group.dev_web_servers.tag
    }
    dev_app_servers = {
      id      = scm_address_group.dev_app_servers.id
      name    = scm_address_group.dev_app_servers.name
      members = scm_address_group.dev_app_servers.static
      tags    = scm_address_group.dev_app_servers.tag
    }
    dev_db_servers = {
      id      = scm_address_group.dev_db_servers.id
      name    = scm_address_group.dev_db_servers.name
      members = scm_address_group.dev_db_servers.static
      tags    = scm_address_group.dev_db_servers.tag
    }
  }
}

output "address_groups_combined" {
  description = "Combined and special purpose address groups"
  value = {
    all_web_servers = {
      id      = scm_address_group.all_web_servers.id
      name    = scm_address_group.all_web_servers.name
      members = scm_address_group.all_web_servers.static
      tags    = scm_address_group.all_web_servers.tag
    }
    all_prod_infrastructure = {
      id      = scm_address_group.all_prod_infrastructure.id
      name    = scm_address_group.all_prod_infrastructure.name
      members = scm_address_group.all_prod_infrastructure.static
      tags    = scm_address_group.all_prod_infrastructure.tag
    }
    dmz_servers = {
      id      = scm_address_group.dmz_servers.id
      name    = scm_address_group.dmz_servers.name
      members = scm_address_group.dmz_servers.static
      tags    = scm_address_group.dmz_servers.tag
    }
    external_endpoints = {
      id      = scm_address_group.external_endpoints.id
      name    = scm_address_group.external_endpoints.name
      members = scm_address_group.external_endpoints.static
      tags    = scm_address_group.external_endpoints.tag
    }
  }
}

# ----------------------------------------------------------------------------
# Summary Outputs
# ----------------------------------------------------------------------------

output "resource_summary" {
  description = "Summary of all created resources"
  value = {
    tags           = 6
    addresses      = 18
    address_groups = 10
    total          = 34
  }
}

output "address_count_by_tier" {
  description = "Count of addresses by tier"
  value = {
    web_tier  = "5 addresses"
    app_tier  = "4 addresses"
    data_tier = "4 addresses"
    dmz       = "3 addresses"
    external  = "2 addresses"
    total     = "18 addresses"
  }
}

output "folder_location" {
  description = "SCM folder where all resources are located"
  value       = "Austin"
}
