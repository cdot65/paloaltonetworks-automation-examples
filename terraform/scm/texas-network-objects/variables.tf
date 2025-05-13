variable "scm_host" {
  description = "Hostname of the Strata Cloud Manager API"
  type        = string
  default     = "api.strata.paloaltonetworks.com"
}

variable "client_id" {
  description = "Client ID for Strata Cloud Manager API authentication"
  type        = string
  sensitive   = true
}

variable "client_secret" {
  description = "Client secret for Strata Cloud Manager API authentication"
  type        = string
  sensitive   = true
}

variable "scope" {
  description = "Scope for Strata Cloud Manager API authentication (e.g., tsg_id:12345)"
  type        = string
}

variable "folder_name" {
  description = "The folder where network objects will be created"
  type        = string
  default     = "Texas"
}