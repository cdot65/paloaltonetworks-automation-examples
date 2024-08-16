// vCenter connection

variable "user" {
  description = "vSphere user name"
}

variable "password" {
  description = "vSphere password"
}

variable "vsphere_server" {
  description = "vCenter server FQDN or IP"
}

// VM specifications

variable "vsphere_datacenter" {
  description = "In which datacenter the VM will be deployed"
}

variable "vsphere_vm_name" {
  description = "What is the name of the VM"
}

variable "vsphere_vm_template" {
  description = "Where is the VM template located"
}

variable "vsphere_vm_folder" {
  description = "In which folder the VM will be store"
}

variable "vsphere_cluster" {
  description = "In which cluster the VM will be deployed"
}

variable "vsphere_host" {
  description = "In which ESXi host the VM will be deployed"
}

variable "vsphere_vcpu_number" {
  description = "How many vCPU will be assigned to the VM"
}

variable "vsphere_memory_size" {
  description = "How much RAM will be assigned to the VM"
}

variable "vsphere_datastore" {
  description = "What is the name of the VM datastore"
}

variable "vsphere_port_group_mgmt" {
  description = "In which port group the VM NIC will be configured for management interface (default: VM Network)"
}

variable "vsphere_port_group_untrust" {
  description = "In which port group the VM NIC will be configured for untrust interface (default: VM Network)"
}

variable "vsphere_port_group_trust" {
  description = "In which port group the VM NIC will be configured for trust interface (default: VM Network)"
}

// firewall virtual machine settings

variable "pavm_hostname" {
  description = "VM-Series hostname (Optional)"
}

variable "pavm_ip_address" {
  description = "VM-Series management IP address (Optional)"
}

variable "pavm_netmask" {
  description = "VM-Series management netmask (Optional)"
}

variable "pavm_gateway" {
  description = "VM-Series management gateway (Optional)"
}

variable "pavm_dns_primary" {
  description = "VM-Series managemenet primary DNS (Optional)"
}

variable "pavm_dns_secondary" {
  description = "VM-Series management secondary DNS (Optional)"
}

variable "panorama_server_ip" {
  description = "Panorama Server IP address (Optional)"
}

variable "panorama_tplname" {
  description = "Panorama template stack name (Optional)"
}

variable "panorama_dgname" {
  description = "Panorama device group name (Optional)"
}

variable "panorama_vm_auth_key" {
  description = "Panorama VM authentication Key (Optional)"
}

variable "pavm_authcode" {
  description = "VM-Series license auth code (Optional)"
}
