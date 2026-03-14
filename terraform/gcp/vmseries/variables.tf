variable "project_id" {
  description = "The GCP project ID where resources will be created"
  type        = string
}

variable "region" {
  description = "The GCP region for resource deployment"
  type        = string
  default     = "us-central1"
}

variable "zone" {
  description = "The GCP zone for resource deployment"
  type        = string
  default     = "us-central1-a"
}

variable "name_prefix" {
  description = "Prefix to be added to all resource names"
  type        = string
  default     = "vmseries"
}

variable "ssh_keys" {
  description = "SSH public keys for accessing the VM-Series instance (format: 'username:ssh-rsa AAAA...')"
  type        = string
}

variable "vmseries_image_name" {
  description = "VM-Series image name from Palo Alto Networks public project"
  type        = string
  default     = "vmseries-flex-bundle2-1022"
}

variable "machine_type" {
  description = "Machine type for the VM-Series instance"
  type        = string
  default     = "n1-standard-4"
}

variable "min_cpu_platform" {
  description = "Minimum CPU platform for the VM-Series instance. Must be compatible with the machine_type. n1 machines support up to Skylake, n2 machines support Cascade Lake and newer."
  type        = string
  default     = "Intel Skylake"
}

variable "bootstrap_bucket_name" {
  description = "Name of the GCS bucket containing bootstrap configuration (optional)"
  type        = string
  default     = null
}

variable "bootstrap_options" {
  description = "Bootstrap options for VM-Series"
  type        = map(string)
  default     = {}
}

variable "mgmt_network_name" {
  description = "Name of the management VPC network"
  type        = string
  default     = "mgmt-network"
}

variable "mgmt_subnet_name" {
  description = "Name of the management subnet"
  type        = string
  default     = "mgmt-subnet"
}

variable "mgmt_subnet_cidr" {
  description = "CIDR range for management subnet"
  type        = string
  default     = "10.0.0.0/24"
}

variable "untrust_network_name" {
  description = "Name of the untrust VPC network"
  type        = string
  default     = "untrust-network"
}

variable "untrust_subnet_name" {
  description = "Name of the untrust subnet"
  type        = string
  default     = "untrust-subnet"
}

variable "untrust_subnet_cidr" {
  description = "CIDR range for untrust subnet"
  type        = string
  default     = "10.0.1.0/24"
}

variable "trust_network_name" {
  description = "Name of the trust VPC network"
  type        = string
  default     = "trust-network"
}

variable "trust_subnet_name" {
  description = "Name of the trust subnet"
  type        = string
  default     = "trust-subnet"
}

variable "trust_subnet_cidr" {
  description = "CIDR range for trust subnet"
  type        = string
  default     = "10.0.2.0/24"
}

variable "create_networks" {
  description = "Whether to create new VPC networks or use existing ones"
  type        = bool
  default     = true
}

variable "allowed_mgmt_ips" {
  description = "List of IP addresses/ranges allowed to access the management interface"
  type        = list(string)
  default     = ["0.0.0.0/0"]
}

variable "tags" {
  description = "Tags to apply to resources"
  type        = list(string)
  default     = ["vmseries"]
}

variable "scopes" {
  description = "Scopes for the VM-Series service account"
  type        = list(string)
  default = [
    "https://www.googleapis.com/auth/compute.readonly",
    "https://www.googleapis.com/auth/cloud.useraccounts.readonly",
    "https://www.googleapis.com/auth/devstorage.read_only",
    "https://www.googleapis.com/auth/logging.write",
    "https://www.googleapis.com/auth/monitoring.write",
  ]
}

variable "create_public_ip" {
  description = "Whether to create and attach a public IP to the management interface"
  type        = bool
  default     = true
}

