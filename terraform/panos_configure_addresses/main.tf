resource "panos_address_object" "address_obj" {
  name        = var.address_name
  value       = var.address_value
  description = var.address_description
  vsys        = "vsys1"

  lifecycle {
    create_before_destroy = true
  }
}
