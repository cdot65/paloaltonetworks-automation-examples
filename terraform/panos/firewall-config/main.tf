# ----------------------------------------------------------------------------
# DNS Settings
# ----------------------------------------------------------------------------
resource "panos_dns_settings" "NGFW" {

  # targets system level dns settings
  location = var.dns_settings.NGFW.location

  # configuration
  dns_settings      = var.dns_settings.NGFW.dns_settings
  fqdn_refresh_time = var.dns_settings.NGFW.fqdn_refresh_time
}
