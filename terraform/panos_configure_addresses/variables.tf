# Firewall Connection Details
variable "hostname" {
  description = "Hostname or IP address of the PAN-OS firewall"
  type        = string
}

variable "username" {
  description = "Username for authentication"
  type        = string
}

variable "password" {
  description = "Password for authentication"
  type        = string
  sensitive   = true
}

# Address Object Parameters
variable "address_name" {
  description = "Name of the address object"
  type        = string
}

variable "address_value" {
  description = "IP address or FQDN for the address object"
  type        = string
}

variable "address_description" {
  description = "Description of the address object"
  type        = string
  default     = ""
}
