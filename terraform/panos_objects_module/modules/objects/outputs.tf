output "address_object_names" {
  value = [for obj in panos_address_object.address_objs : obj.name]
}

output "static_address_group_names" {
  value = [for grp in panos_address_group.static_groups : grp.name]
}

output "dynamic_address_group_names" {
  value = [for grp in panos_address_group.dynamic_groups : grp.name]
}

output "service_object_names" {
  value = [for svc in panos_service_object.service_objs : svc.name]
}
