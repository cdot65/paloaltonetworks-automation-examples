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
