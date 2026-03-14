terraform {
  required_providers {
    panos = {
      source  = "PaloAltoNetworks/panos"
      version = "2.0.0"
    }
  }
}

provider "panos" {
  hostname                = var.ngfw.hostname
  username                = var.ngfw.username
  password                = var.ngfw.password
  skip_verify_certificate = true
}