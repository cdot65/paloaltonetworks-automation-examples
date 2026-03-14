output "vmseries_instance_name" {
  description = "Name of the VM-Series instance"
  value       = module.vmseries.instance.name
}

output "vmseries_instance_id" {
  description = "Instance ID of the VM-Series"
  value       = module.vmseries.instance.instance_id
}

output "vmseries_self_link" {
  description = "Self-link of the VM-Series instance"
  value       = module.vmseries.self_link
}

output "mgmt_public_ip" {
  description = "Public IP address of the management interface"
  value       = var.create_public_ip ? google_compute_address.mgmt[0].address : "No public IP created"
}

output "mgmt_private_ip" {
  description = "Private IP address of the management interface (nic0)"
  value       = try(module.vmseries.private_ips["nic0"], "Not available yet")
}

output "untrust_private_ip" {
  description = "Private IP address of the untrust interface (nic1)"
  value       = try(module.vmseries.private_ips["nic1"], "Not available yet")
}

output "trust_private_ip" {
  description = "Private IP address of the trust interface (nic2)"
  value       = try(module.vmseries.private_ips["nic2"], "Not available yet")
}

output "all_public_ips" {
  description = "All public IP addresses assigned to the VM-Series"
  value       = module.vmseries.public_ips
}

output "mgmt_url" {
  description = "URL to access the VM-Series management interface"
  value       = var.create_public_ip ? "https://${google_compute_address.mgmt[0].address}" : "Use Cloud Console to access via IAP or set up Cloud VPN"
}

output "ssh_command" {
  description = "SSH command to connect to the VM-Series"
  value       = var.create_public_ip ? "ssh admin@${google_compute_address.mgmt[0].address}" : "Use gcloud compute ssh or IAP tunneling"
}

output "instance_zone" {
  description = "Zone where the VM-Series instance is deployed"
  value       = module.vmseries.instance.zone
}
