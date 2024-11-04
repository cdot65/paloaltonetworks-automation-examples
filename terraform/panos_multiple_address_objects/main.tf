resource "panos_address_object" "address_objs" {
  for_each = var.address_objects

  name        = each.key
  value       = each.value.value
  description = each.value.description
  vsys        = "vsys1"

  lifecycle {
    create_before_destroy = true
  }
}
