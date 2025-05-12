output "dallas_office_id" {
  description = "ID of the Dallas office address object"
  value       = scm_address_object.dallas_office.id
}

output "austin_office_id" {
  description = "ID of the Austin office address object"
  value       = scm_address_object.austin_office.id
}

output "houston_office_id" {
  description = "ID of the Houston office address object"
  value       = scm_address_object.houston_office.id
}

output "san_antonio_office_id" {
  description = "ID of the San Antonio office address object"
  value       = scm_address_object.san_antonio_office.id
}

output "fort_worth_office_id" {
  description = "ID of the Fort Worth office address object"
  value       = scm_address_object.fort_worth_office.id
}

output "texas_datacenter_id" {
  description = "ID of the Texas datacenter address object"
  value       = scm_address_object.texas_datacenter.id
}

output "all_address_object_ids" {
  description = "IDs of all created address objects"
  value = {
    dallas_office     = scm_address_object.dallas_office.id
    austin_office     = scm_address_object.austin_office.id
    houston_office    = scm_address_object.houston_office.id
    san_antonio_office = scm_address_object.san_antonio_office.id
    fort_worth_office = scm_address_object.fort_worth_office.id
    texas_datacenter  = scm_address_object.texas_datacenter.id
    texas_dev_server  = scm_address_object.texas_dev_server.id
    texas_web_server  = scm_address_object.texas_web_server.id
    texas_db_server   = scm_address_object.texas_db_server.id
    texas_public_ips  = scm_address_object.texas_public_ips.id
  }
}