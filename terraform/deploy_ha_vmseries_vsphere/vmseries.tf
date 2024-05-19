//* vSphere Provider ----------------------------------------------------- *//

provider "vsphere" {
  // version        = "1.5.0"
  vsphere_server = var.vsphere_server
  user           = var.user
  password       = var.password

  allow_unverified_ssl = "true"
}

//* vSphere data --------------------------------------------------------- *//

// datacenter
data "vsphere_datacenter" "dc" {
  name = var.vsphere_datacenter
}

// compute
data "vsphere_compute_cluster" "cluster" {
  name          = var.vsphere_cluster
  datacenter_id = data.vsphere_datacenter.dc.id
}

data "vsphere_host" "host" {
  name          = var.vsphere_host
  datacenter_id = data.vsphere_datacenter.dc.id
}

// storage
data "vsphere_datastore" "datastore" {
  name          = var.vsphere_datastore
  datacenter_id = data.vsphere_datacenter.dc.id
}

// networking
data "vsphere_network" "mgmt_network" {
  name          = var.vsphere_port_group_mgmt
  datacenter_id = data.vsphere_datacenter.dc.id
}

data "vsphere_network" "untrust_network" {
  name          = var.vsphere_port_group_untrust
  datacenter_id = data.vsphere_datacenter.dc.id
}

data "vsphere_network" "trust_network" {
  name          = var.vsphere_port_group_trust
  datacenter_id = data.vsphere_datacenter.dc.id
}

// VM template
data "vsphere_virtual_machine" "template" {
  name          = var.vsphere_vm_template
  datacenter_id = data.vsphere_datacenter.dc.id
}

//* Bootstrap file ------------------------------------------------------- *//

resource "local_file" "config" {
  content  = <<EOF
type=dhcp-client
ip-address=${var.pavm_ip_address}s
hostname=${var.pavm_hostname}
tplname=${var.panorama_tplname}
default-gateway=${var.pavm_gateway}
netmask=${var.pavm_netmask}
vm-auth-key=${var.panorama_vm_auth_key}
panorama-server=${var.panorama_server_ip}
dgname=${var.panorama_dgname}
dns-primary=${var.pavm_dns_primary}
dns-secondary=${var.pavm_dns_secondary}
EOF
  filename = "${path.module}/bts/config/init-cfg.txt"
}

resource "local_file" "license" {
  content  = var.pavm_authcode
  filename = "${path.module}/bts/license/authcodes"
}

resource "local_file" "software" {
  content  = ""
  filename = "${path.module}/bts/software/.software"
}

resource "local_file" "content" {
  content  = ""
  filename = "${path.module}/bts/content/.content"
}

// build ISO file with our files

resource "null_resource" "bts" {
  provisioner "local-exec" {
    command = "/usr/bin/mkisofs -J -o ${path.module}/bts_${var.vsphere_vm_name}.iso ${path.module}/bts"
  }
}

//* vSphere Resources ---------------------------------------------------- *//

// Upload our bootstrap ISO
resource "vsphere_file" "bts_iso_upload" {
  datacenter       = var.vsphere_datacenter
  datastore        = var.vsphere_datastore
  source_file      = "${path.module}/bts_${var.vsphere_vm_name}.iso"
  destination_file = "/bts_${var.vsphere_vm_name}.iso"
}


// Create a vSphere VM folder
resource "vsphere_folder" "terraform-pa-vm" {
  path          = var.vsphere_vm_folder
  type          = "vm"
  datacenter_id = data.vsphere_datacenter.dc.id
}

// Create our firewall
resource "vsphere_virtual_machine" "terraform-pa-vm" {

  // VM placement
  name             = var.vsphere_vm_name
  resource_pool_id = data.vsphere_compute_cluster.cluster.resource_pool_id
  datastore_id     = data.vsphere_datastore.datastore.id
  folder           = vsphere_folder.terraform-pa-vm.path

  // VM resources
  num_cpus = var.vsphere_vcpu_number
  memory   = var.vsphere_memory_size

  // Guest OS
  guest_id = data.vsphere_virtual_machine.template.guest_id

  // VM storage
  disk {
    label            = "${var.vsphere_vm_name}.vmdk"
    size             = data.vsphere_virtual_machine.template.disks.0.size
    thin_provisioned = data.vsphere_virtual_machine.template.disks.0.thin_provisioned
    eagerly_scrub    = data.vsphere_virtual_machine.template.disks.0.eagerly_scrub
  }

  scsi_type = "lsilogic"

  cdrom {
    datastore_id = data.vsphere_datastore.datastore.id
    path         = "/bts_${var.vsphere_vm_name}.iso"
  }

  // VM networking - Management interface
  network_interface {
    network_id   = data.vsphere_network.mgmt_network.id
    adapter_type = data.vsphere_virtual_machine.template.network_interface_types[0]
  }

  // VM networking - untrsut interface
  network_interface {
    network_id   = data.vsphere_network.untrust_network.id
    adapter_type = data.vsphere_virtual_machine.template.network_interface_types[0]
  }

  // VM networking - trust interface
  network_interface {
    network_id   = data.vsphere_network.trust_network.id
    adapter_type = data.vsphere_virtual_machine.template.network_interface_types[0]
  }

  // Customization of the VM
  clone {
    template_uuid = data.vsphere_virtual_machine.template.id
  }

  // Advanced options
  wait_for_guest_net_timeout  = 10
  wait_for_guest_net_routable = false
}
