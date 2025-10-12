# ============================================================================
# Address Groups - Austin Folder
# ============================================================================
# Address groups organized by environment and tier with proper dependencies
# ============================================================================

# ----------------------------------------------------------------------------
# Production Environment Groups
# ----------------------------------------------------------------------------

# Production Web Servers Group
resource "scm_address_group" "prod_web_servers" {
  folder      = "Austin"
  name        = "prod-web-servers"
  description = "All production web servers"
  static = [
    scm_address.web_prod_1.name,
    scm_address.web_prod_2.name,
    scm_address.web_prod_subnet.name
  ]
  tag = [scm_tag.production.name, scm_tag.web_tier.name]

  depends_on = [
    scm_address.web_prod_1,
    scm_address.web_prod_2,
    scm_address.web_prod_subnet,
    scm_tag.production,
    scm_tag.web_tier
  ]
}

# Production Application Servers Group
resource "scm_address_group" "prod_app_servers" {
  folder      = "Austin"
  name        = "prod-app-servers"
  description = "All production application servers"
  static = [
    scm_address.app_prod_1.name,
    scm_address.app_prod_2.name,
    scm_address.app_prod_range.name
  ]
  tag = [scm_tag.production.name, scm_tag.app_tier.name]

  depends_on = [
    scm_address.app_prod_1,
    scm_address.app_prod_2,
    scm_address.app_prod_range,
    scm_tag.production,
    scm_tag.app_tier
  ]
}

# Production Database Servers Group
resource "scm_address_group" "prod_db_servers" {
  folder      = "Austin"
  name        = "prod-db-servers"
  description = "All production database servers"
  static = [
    scm_address.db_prod_1.name,
    scm_address.db_prod_2.name,
    scm_address.db_prod_range.name
  ]
  tag = [scm_tag.production.name, scm_tag.data_tier.name]

  depends_on = [
    scm_address.db_prod_1,
    scm_address.db_prod_2,
    scm_address.db_prod_range,
    scm_tag.production,
    scm_tag.data_tier
  ]
}

# ----------------------------------------------------------------------------
# Development Environment Groups
# ----------------------------------------------------------------------------

# Development Web Servers Group
resource "scm_address_group" "dev_web_servers" {
  folder      = "Austin"
  name        = "dev-web-servers"
  description = "All development web servers"
  static = [
    scm_address.web_dev_1.name,
    scm_address.web_dev_subnet.name
  ]
  tag = [scm_tag.development.name, scm_tag.web_tier.name]

  depends_on = [
    scm_address.web_dev_1,
    scm_address.web_dev_subnet,
    scm_tag.development,
    scm_tag.web_tier
  ]
}

# Development Application Servers Group
resource "scm_address_group" "dev_app_servers" {
  folder      = "Austin"
  name        = "dev-app-servers"
  description = "All development application servers"
  static = [
    scm_address.app_dev_subnet.name
  ]
  tag = [scm_tag.development.name, scm_tag.app_tier.name]

  depends_on = [
    scm_address.app_dev_subnet,
    scm_tag.development,
    scm_tag.app_tier
  ]
}

# Development Database Servers Group
resource "scm_address_group" "dev_db_servers" {
  folder      = "Austin"
  name        = "dev-db-servers"
  description = "All development database servers"
  static = [
    scm_address.db_dev_subnet.name
  ]
  tag = [scm_tag.development.name, scm_tag.data_tier.name]

  depends_on = [
    scm_address.db_dev_subnet,
    scm_tag.development,
    scm_tag.data_tier
  ]
}

# ----------------------------------------------------------------------------
# Combined and Special Purpose Groups
# ----------------------------------------------------------------------------

# All Web Servers Group (combines prod and dev)
resource "scm_address_group" "all_web_servers" {
  folder      = "Austin"
  name        = "all-web-servers"
  description = "All web servers (production and development)"
  static = [
    scm_address.web_prod_1.name,
    scm_address.web_prod_2.name,
    scm_address.web_prod_subnet.name,
    scm_address.web_dev_1.name,
    scm_address.web_dev_subnet.name
  ]
  tag = [scm_tag.web_tier.name]

  depends_on = [
    scm_address.web_prod_1,
    scm_address.web_prod_2,
    scm_address.web_prod_subnet,
    scm_address.web_dev_1,
    scm_address.web_dev_subnet,
    scm_tag.web_tier
  ]
}

# DMZ Servers Group
resource "scm_address_group" "dmz_servers" {
  folder      = "Austin"
  name        = "dmz-servers"
  description = "All DMZ servers"
  static = [
    scm_address.dmz_proxy_1.name,
    scm_address.dmz_proxy_2.name,
    scm_address.dmz_subnet.name
  ]
  tag = [scm_tag.dmz.name]

  depends_on = [
    scm_address.dmz_proxy_1,
    scm_address.dmz_proxy_2,
    scm_address.dmz_subnet,
    scm_tag.dmz
  ]
}

# External Endpoints Group
resource "scm_address_group" "external_endpoints" {
  folder      = "Austin"
  name        = "external-endpoints"
  description = "External API and CDN endpoints"
  static = [
    scm_address.api_endpoint.name,
    scm_address.cdn_endpoint.name
  ]
  tag = [scm_tag.production.name]

  depends_on = [
    scm_address.api_endpoint,
    scm_address.cdn_endpoint,
    scm_tag.production
  ]
}

# All Production Infrastructure Group
resource "scm_address_group" "all_prod_infrastructure" {
  folder      = "Austin"
  name        = "all-prod-infrastructure"
  description = "All production infrastructure (web, app, db)"
  static = [
    scm_address.web_prod_1.name,
    scm_address.web_prod_2.name,
    scm_address.web_prod_subnet.name,
    scm_address.app_prod_1.name,
    scm_address.app_prod_2.name,
    scm_address.app_prod_range.name,
    scm_address.db_prod_1.name,
    scm_address.db_prod_2.name,
    scm_address.db_prod_range.name
  ]
  tag = [scm_tag.production.name]

  depends_on = [
    scm_address.web_prod_1,
    scm_address.web_prod_2,
    scm_address.web_prod_subnet,
    scm_address.app_prod_1,
    scm_address.app_prod_2,
    scm_address.app_prod_range,
    scm_address.db_prod_1,
    scm_address.db_prod_2,
    scm_address.db_prod_range,
    scm_tag.production
  ]
}
