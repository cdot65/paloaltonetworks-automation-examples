variable "scm_host" {
  description = "The hostname of Strata Cloud Manager API"
  type        = string
  default     = "api.sase.paloaltonetworks.com"
}

variable "scm_auth_url" {
  description = "The URL to send auth credentials to which will return a JWT"
  type        = string
  default     = "https://auth.apps.paloaltonetworks.com/auth/v1/oauth2/access_token"
}

variable "scm_client_id" {
  description = "The client ID for the connection"
  type        = string
  default     = ""
  sensitive   = true
}

variable "scm_client_secret" {
  description = "The client secret for the connection"
  type        = string
  default     = ""
  sensitive   = true
}

variable "scm_scope" {
  description = "The client scope"
  type        = string
  default     = ""
  sensitive   = true
}

variable "scm_auth_file" {
  description = "Path to JSON file with auth credentials for SCM"
  type        = string
  default     = ""
}

variable "scm_logging" {
  description = "The logging level of the provider (quiet, action, path, info, debug)"
  type        = string
  default     = "quiet"
}

variable "folder" {
  description = "The folder in which resources will be created (e.g., 'Shared', 'Mobile Users', etc.)"
  type        = string
  default     = "Shared"
}

variable "environment" {
  description = "Environment name for tagging resources"
  type        = string
  default     = "development"
}

variable "project_name" {
  description = "Project name for resource naming"
  type        = string
  default     = "scm-test"
}
