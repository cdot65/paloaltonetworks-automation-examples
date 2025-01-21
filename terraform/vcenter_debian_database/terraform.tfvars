# terraform.tfvars

vcenter_user     = "your_vcenter_user"
vcenter_password = "your_vcenter_password"
vcenter_server   = "vcenter.example.io"
datacenter_name  = "Datacenter"
datastore_name   = "datastore1"
cluster_name     = "Cluster"
network_name     = "database"
host_name        = "esx1.example.io"
template_name    = "debian-template"
vm_name          = "postgres-vm"
vm_ipv4_address  = "192.168.1.100"
vm_ipv4_netmask  = 24
vm_ipv4_gateway  = "192.168.1.1"
vm_domain        = "example.io"
vm_cpu_count     = 4
vm_memory        = 4096
vm_disk_size     = 24
tags             = ["postgres", "database"]