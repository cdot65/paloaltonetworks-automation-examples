output "created_address_objects" {
  value = [for obj in panos_address_object.address_objs : obj.name]
}
