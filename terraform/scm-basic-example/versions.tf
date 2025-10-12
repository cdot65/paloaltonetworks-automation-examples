terraform {
  required_version = ">= 1.0"

  required_providers {
    scm = {
      source  = "PaloAltoNetworks/scm"
      version = "~> 1.0.1"
    }
  }
}
