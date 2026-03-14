# Texas Service Groups Configuration

# Web Service Group
resource "scm_service_group" "web_services" {
  folder  = var.folder_name
  name    = "texas-web-services"
  members = [
    scm_service.web_http.name,
    scm_service.web_https.name
  ]
  tags = [scm_tag.texas_tag.name, scm_tag.web_server_tag.name, scm_tag.automation_tag.name, scm_tag.terraform_tag.name]
}

# Database Service Group
resource "scm_service_group" "database_services" {
  folder  = var.folder_name
  name    = "texas-database-services"
  members = [
    scm_service.db_mysql.name,
    scm_service.db_mssql.name,
    scm_service.db_postgres.name
  ]
  tags = [scm_tag.texas_tag.name, scm_tag.database_tag.name, scm_tag.automation_tag.name, scm_tag.terraform_tag.name]
}

# Management Service Group
resource "scm_service_group" "management_services" {
  folder  = var.folder_name
  name    = "texas-management-services"
  members = [
    scm_service.mgmt_ssh.name,
    scm_service.mgmt_rdp.name
  ]
  tags = [scm_tag.texas_tag.name, scm_tag.automation_tag.name, scm_tag.terraform_tag.name]
}

# Application Service Group
resource "scm_service_group" "application_services" {
  folder  = var.folder_name
  name    = "texas-application-services"
  members = [
    scm_service.app_custom_tcp.name,
    scm_service.app_custom_udp.name
  ]
  tags = [scm_tag.texas_tag.name, scm_tag.automation_tag.name, scm_tag.terraform_tag.name]
}

# All Texas Services Group
resource "scm_service_group" "all_texas_services" {
  folder  = var.folder_name
  name    = "texas-all-services"
  members = [
    scm_service_group.web_services.name,
    scm_service_group.database_services.name,
    scm_service_group.management_services.name,
    scm_service_group.application_services.name
  ]
  tags = [scm_tag.texas_tag.name, scm_tag.automation_tag.name, scm_tag.terraform_tag.name]
}