variable "hostname" {
  type = string
}

variable "username" {
  type = string
}

variable "password" {
  type      = string
  sensitive = true
}

variable "vsys" {
  description = "Virtual system to use"
  type        = string
  default     = "vsys1"
}

# Address Objects
variable "address_objects" {
  description = "Map of address objects"
  type = map(object({
    value       = string
    description = string
    tags        = list(string)
  }))
}

# Static Address Groups
variable "static_address_groups" {
  description = "Map of static address groups"
  type = map(object({
    description      = string
    static_addresses = list(string)
    tags             = list(string)
  }))
}

# Dynamic Address Groups
variable "dynamic_address_groups" {
  description = "Map of dynamic address groups"
  type = map(object({
    description   = string
    dynamic_match = string
    tags          = list(string)
  }))
}

# Service Objects
variable "service_objects" {
  description = "Map of service objects"
  type = map(object({
    protocol         = string
    description      = string
    source_port      = string
    destination_port = string
    tags             = list(string)
  }))
}

# Tags
variable "tags" {
  description = "Map of tags"
  type = map(object({
    color   = string
    comment = string
  }))
}

# Dynamic Address Group Entries (IP Tags)
variable "ip_tags" {
  description = "Map of IP tags"
  type = map(object({
    ip   = string
    tags = list(string)
  }))
}
