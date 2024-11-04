terraform {
  required_providers {
    panos = {
      source  = "PaloAltoNetworks/panos"
      version = "1.11.1"
    }
  }
}

provider "panos" {
  hostname = var.hostname
  username = var.username
  password = var.password
}
