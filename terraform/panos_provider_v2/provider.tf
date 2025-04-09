terraform {
  required_providers {
    panos = {
      source  = "PaloAltoNetworks/panos"
      version = "2.0.0"
    }
  }
}

provider "panos" {
  hostname = var.panorama.hostname
  username = var.panorama.username
  password = var.panorama.password
  # verify_certificate = false # If using self-signed certs
}