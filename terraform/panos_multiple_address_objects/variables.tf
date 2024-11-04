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

# List of Address Objects
variable "address_objects" {
  description = "List of address objects to create"
  type = map(object({
    value       = string
    description = string
  }))
}
