# Tag outputs
output "tag_ids" {
  description = "IDs of created tags"
  value = {
    texas       = scm_tag.texas_tag.id
    dallas      = scm_tag.dallas_tag.id
    austin      = scm_tag.austin_tag.id
    houston     = scm_tag.houston_tag.id
    san_antonio = scm_tag.san_antonio_tag.id
    fort_worth  = scm_tag.fort_worth_tag.id
    production  = scm_tag.production_tag.id
    development = scm_tag.development_tag.id
    staging     = scm_tag.staging_tag.id
    datacenter  = scm_tag.datacenter_tag.id
    web_server  = scm_tag.web_server_tag.id
    database    = scm_tag.database_tag.id
    automation  = scm_tag.automation_tag.id
    terraform   = scm_tag.terraform_tag.id
  }
}

# Service outputs
output "service_ids" {
  description = "IDs of created services"
  value = {
    http         = scm_service.web_http.id
    https        = scm_service.web_https.id
    mysql        = scm_service.db_mysql.id
    mssql        = scm_service.db_mssql.id
    postgres     = scm_service.db_postgres.id
    ssh          = scm_service.mgmt_ssh.id
    rdp          = scm_service.mgmt_rdp.id
    custom_tcp   = scm_service.app_custom_tcp.id
    custom_udp   = scm_service.app_custom_udp.id
  }
}

# Service group outputs
output "service_group_ids" {
  description = "IDs of created service groups"
  value = {
    web_services        = scm_service_group.web_services.id
    database_services   = scm_service_group.database_services.id
    management_services = scm_service_group.management_services.id
    application_services = scm_service_group.application_services.id
    all_texas_services  = scm_service_group.all_texas_services.id
  }
}

output "all_texas_services_members" {
  description = "Members of the All Texas Services group"
  value       = scm_service_group.all_texas_services.members
}