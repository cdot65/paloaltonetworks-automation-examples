# variables.tf

variable "vcenter_user" {
  description = "Username for vCenter authentication"
  type        = string
}

variable "vcenter_password" {
  description = "Password for vCenter authentication"
  type        = string
  sensitive   = true
}

variable "vcenter_server" {
  description = "vCenter server address"
  type        = string
}

variable "datacenter_name" {
  description = "Name of the vSphere datacenter"
  type        = string
}

variable "datastore_name" {
  description = "Name of the vSphere datastore"
  type        = string
}

variable "cluster_name" {
  description = "Name of the vSphere cluster"
  type        = string
}

variable "network_name" {
  description = "Name of the network to attach the VM to"
  type        = string
}

variable "host_name" {
  description = "Name of the ESXi host to deploy the VM on"
  type        = string
}

variable "template_name" {
  description = "Name of the template to clone the VM from"
  type        = string
}

variable "vm_name" {
  description = "Name of the virtual machine"
  type        = string
}

variable "vm_ipv4_address" {
  description = "Static IPv4 address for the VM"
  type        = string
}

variable "vm_ipv4_netmask" {
  description = "IPv4 netmask for the VM"
  type        = number
}

variable "vm_ipv4_gateway" {
  description = "IPv4 gateway for the VM"
  type        = string
}

variable "vm_domain" {
  description = "Domain name for the VM"
  type        = string
}

variable "vm_cpu_count" {
  description = "Number of vCPUs for the VM"
  type        = number
}

variable "vm_memory" {
  description = "Amount of memory (in MB) for the VM"
  type        = number
}

variable "vm_disk_size" {
  description = "Size of the disk (in GB) for the VM"
  type        = number
}

variable "tags" {
  description = "List of tags to associate with the VM"
  type        = list(string)
}