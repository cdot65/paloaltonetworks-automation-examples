# ============================================================================
# Address Objects - Austin Folder
# ============================================================================
# Address objects organized by tier: web, app, data, dmz, and external
# ============================================================================

# ----------------------------------------------------------------------------
# Web Tier Address Objects
# ----------------------------------------------------------------------------

# Production Web Servers
resource "scm_address" "web_prod_1" {
  folder      = "Austin"
  name        = "web-prod-1"
  description = "Production web server 1"
  ip_netmask  = "10.1.10.10/32"
  tag         = [scm_tag.production.name, scm_tag.web_tier.name]
  depends_on  = [scm_tag.production, scm_tag.web_tier]
}

resource "scm_address" "web_prod_2" {
  folder      = "Austin"
  name        = "web-prod-2"
  description = "Production web server 2"
  ip_netmask  = "10.1.10.11/32"
  tag         = [scm_tag.production.name, scm_tag.web_tier.name]
  depends_on  = [scm_tag.production, scm_tag.web_tier]
}

resource "scm_address" "web_prod_subnet" {
  folder      = "Austin"
  name        = "web-prod-subnet"
  description = "Production web server subnet"
  ip_netmask  = "10.1.10.0/24"
  tag         = [scm_tag.production.name, scm_tag.web_tier.name]
  depends_on  = [scm_tag.production, scm_tag.web_tier]
}

# Development Web Servers
resource "scm_address" "web_dev_1" {
  folder      = "Austin"
  name        = "web-dev-1"
  description = "Development web server 1"
  ip_netmask  = "10.2.10.10/32"
  tag         = [scm_tag.development.name, scm_tag.web_tier.name]
  depends_on  = [scm_tag.development, scm_tag.web_tier]
}

resource "scm_address" "web_dev_subnet" {
  folder      = "Austin"
  name        = "web-dev-subnet"
  description = "Development web server subnet"
  ip_netmask  = "10.2.10.0/24"
  tag         = [scm_tag.development.name, scm_tag.web_tier.name]
  depends_on  = [scm_tag.development, scm_tag.web_tier]
}

# ----------------------------------------------------------------------------
# Application Tier Address Objects
# ----------------------------------------------------------------------------

resource "scm_address" "app_prod_1" {
  folder      = "Austin"
  name        = "app-prod-1"
  description = "Production app server 1"
  ip_netmask  = "10.1.20.10/32"
  tag         = [scm_tag.production.name, scm_tag.app_tier.name]
  depends_on  = [scm_tag.production, scm_tag.app_tier]
}

resource "scm_address" "app_prod_2" {
  folder      = "Austin"
  name        = "app-prod-2"
  description = "Production app server 2"
  ip_netmask  = "10.1.20.11/32"
  tag         = [scm_tag.production.name, scm_tag.app_tier.name]
  depends_on  = [scm_tag.production, scm_tag.app_tier]
}

resource "scm_address" "app_prod_range" {
  folder      = "Austin"
  name        = "app-prod-range"
  description = "Production app server IP range"
  ip_range    = "10.1.20.10-10.1.20.20"
  tag         = [scm_tag.production.name, scm_tag.app_tier.name]
  depends_on  = [scm_tag.production, scm_tag.app_tier]
}

resource "scm_address" "app_dev_subnet" {
  folder      = "Austin"
  name        = "app-dev-subnet"
  description = "Development app server subnet"
  ip_netmask  = "10.2.20.0/24"
  tag         = [scm_tag.development.name, scm_tag.app_tier.name]
  depends_on  = [scm_tag.development, scm_tag.app_tier]
}

# ----------------------------------------------------------------------------
# Data Tier Address Objects
# ----------------------------------------------------------------------------

resource "scm_address" "db_prod_1" {
  folder      = "Austin"
  name        = "db-prod-1"
  description = "Production database server 1"
  ip_netmask  = "10.1.30.10/32"
  tag         = [scm_tag.production.name, scm_tag.data_tier.name]
  depends_on  = [scm_tag.production, scm_tag.data_tier]
}

resource "scm_address" "db_prod_2" {
  folder      = "Austin"
  name        = "db-prod-2"
  description = "Production database server 2"
  ip_netmask  = "10.1.30.11/32"
  tag         = [scm_tag.production.name, scm_tag.data_tier.name]
  depends_on  = [scm_tag.production, scm_tag.data_tier]
}

resource "scm_address" "db_prod_range" {
  folder      = "Austin"
  name        = "db-prod-range"
  description = "Production database IP range"
  ip_range    = "10.1.30.10-10.1.30.20"
  tag         = [scm_tag.production.name, scm_tag.data_tier.name]
  depends_on  = [scm_tag.production, scm_tag.data_tier]
}

resource "scm_address" "db_dev_subnet" {
  folder      = "Austin"
  name        = "db-dev-subnet"
  description = "Development database subnet"
  ip_netmask  = "10.2.30.0/24"
  tag         = [scm_tag.development.name, scm_tag.data_tier.name]
  depends_on  = [scm_tag.development, scm_tag.data_tier]
}

# ----------------------------------------------------------------------------
# DMZ and External Resources
# ----------------------------------------------------------------------------

resource "scm_address" "dmz_proxy_1" {
  folder      = "Austin"
  name        = "dmz-proxy-1"
  description = "DMZ proxy server 1"
  ip_netmask  = "192.168.100.10/32"
  tag         = [scm_tag.production.name, scm_tag.dmz.name]
  depends_on  = [scm_tag.production, scm_tag.dmz]
}

resource "scm_address" "dmz_proxy_2" {
  folder      = "Austin"
  name        = "dmz-proxy-2"
  description = "DMZ proxy server 2"
  ip_netmask  = "192.168.100.11/32"
  tag         = [scm_tag.production.name, scm_tag.dmz.name]
  depends_on  = [scm_tag.production, scm_tag.dmz]
}

resource "scm_address" "dmz_subnet" {
  folder      = "Austin"
  name        = "dmz-subnet"
  description = "DMZ subnet"
  ip_netmask  = "192.168.100.0/24"
  tag         = [scm_tag.dmz.name]
  depends_on  = [scm_tag.dmz]
}

# FQDN addresses
resource "scm_address" "api_endpoint" {
  folder      = "Austin"
  name        = "api-endpoint"
  description = "External API endpoint"
  fqdn        = "api.company.com"
  tag         = [scm_tag.production.name]
  depends_on  = [scm_tag.production]
}

resource "scm_address" "cdn_endpoint" {
  folder      = "Austin"
  name        = "cdn-endpoint"
  description = "CDN endpoint"
  fqdn        = "cdn.company.com"
  tag         = [scm_tag.production.name]
  depends_on  = [scm_tag.production]
}
