terraform {
  required_version = ">= 1.5.7"
  required_providers {
    scm = {
      source  = "paloaltonetworks/scm"
      version = ">= 0.10.1"
    }
  }
}
