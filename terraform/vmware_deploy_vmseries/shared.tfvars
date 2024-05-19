// vSphere Authentication
user           = "automation@vsphere.local"
vsphere_server = "10.0.0.2"
password       = "mysecretpassword"

// vSphere specifications
vsphere_datacenter         = "Redtail"
vsphere_vm_template        = "PA-VM-ESX-10.2.3"
vsphere_cluster            = "headquarters"
vsphere_host               = "dal-esx-01"
vsphere_vcpu_number        = "2"
vsphere_memory_size        = "6656"
vsphere_datastore          = "dal-dst-03"
vsphere_port_group_mgmt    = "Management"
vsphere_port_group_untrust = "Dallas_WAN"
vsphere_port_group_trust   = "Dallas_DMZ"

// VM specific parameters
pavm_netmask       = "/16"
pavm_gateway       = "10.0.0.1"
pavm_dns_primary   = "10.30.0.50"
pavm_dns_secondary = "10.30.0.51"
pavm_authcode      = "MYAUTHCODE"

// Panorama details
panorama_server_ip = "10.0.0.46"
panorama_tplname   = "BaseTemplate"
panorama_dgname    = "branch"
# panorama_vm_auth_key = ""
