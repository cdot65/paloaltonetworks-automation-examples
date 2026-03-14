provider "scm" {
  host          = var.scm_host
  client_id     = var.client_id
  client_secret = var.client_secret
  scope         = var.scope
}

terraform {
  required_providers {
    scm = {
      source  = "paloaltonetworks/scm"
      version = "0.1.0"
    }
  }
}