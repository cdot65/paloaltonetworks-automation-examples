# ----------------------------------------------------------------------------
# Templates
# ----------------------------------------------------------------------------
output "branch_template" {
  value = panos_template.Branch.name
}

# ----------------------------------------------------------------------------
# Template Stacks
# ----------------------------------------------------------------------------
output "dallas_template_stack" {
  value = panos_template_stack.Dallas.name
}

output "woodlands_template_stack" {
  value = panos_template_stack.Woodlands.name
}

# ----------------------------------------------------------------------------
# Device Groups
# ----------------------------------------------------------------------------
output "branch_device_group" {
  value = panos_device_group.Branch.name
}

output "dallas_device_group" {
  value = panos_device_group.Dallas.name
}

output "woodlands_device_group" {
  value = panos_device_group.Woodlands.name
}

# ----------------------------------------------------------------------------
# Security Policy
# ----------------------------------------------------------------------------
output "branch_security_rules" {
  value = panos_security_policy.branch_policy.rules
}

# ----------------------------------------------------------------------------
# Services
# ----------------------------------------------------------------------------
output "web_service" {
  value = panos_service.web_service_dev.name
}

output "dns_service" {
  value = panos_service.dns_dev.name
}

# ----------------------------------------------------------------------------
# Zones
# ----------------------------------------------------------------------------
output "untrust_zone" {
  value = panos_zone.untrust_zone.name
}

output "trust_zone" {
  value = panos_zone.trust_zone.name
}
