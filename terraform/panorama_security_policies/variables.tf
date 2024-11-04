# Panorama Connection Details
variable "hostname" {
  description = "Hostname or IP address of the Panorama server"
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

# Device Group
variable "device_group" {
  description = "Name of the device group in Panorama"
  type        = string
  default     = "Austin"
}

# Template
variable "template" {
  description = "Name of the template in Panorama"
  type        = string
  default     = "Austin"
}
