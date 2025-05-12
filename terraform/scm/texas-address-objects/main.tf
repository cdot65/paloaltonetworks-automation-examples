# Texas Address Objects Configuration

# First, create the Texas folder if it doesn't exist
# Note: SCM might not support folder creation via Terraform
# You may need to create this folder manually in the SCM interface

# Dallas Office
resource "scm_address_object" "dallas_office" {
  folder      = var.folder_name
  name        = "dallas-office"
  description = "Dallas headquarters IP address"
  ip_netmask  = "192.168.1.0/24"
  tags        = ["Automation", "Terraform"]
}

# Austin Office
resource "scm_address_object" "austin_office" {
  folder      = var.folder_name
  name        = "austin-office"
  description = "Austin branch office IP address"
  ip_netmask  = "192.168.2.0/24"
  tags        = ["Automation", "Terraform"]
}

# Houston Office
resource "scm_address_object" "houston_office" {
  folder      = var.folder_name
  name        = "houston-office"
  description = "Houston branch office IP address"
  ip_netmask  = "192.168.3.0/24"
  tags        = ["Automation", "Terraform"]
}

# San Antonio Office
resource "scm_address_object" "san_antonio_office" {
  folder      = var.folder_name
  name        = "san-antonio-office"
  description = "San Antonio branch office IP address"
  ip_netmask  = "192.168.4.0/24"
  tags        = ["Automation", "Terraform"]
}

# Fort Worth Office
resource "scm_address_object" "fort_worth_office" {
  folder      = var.folder_name
  name        = "fort-worth-office"
  description = "Fort Worth branch office IP address"
  ip_netmask  = "192.168.5.0/24"
  tags        = ["Automation", "Terraform"]
}

# Texas Data Center 
resource "scm_address_object" "texas_datacenter" {
  folder      = var.folder_name
  name        = "texas-datacenter"
  description = "Texas primary data center"
  ip_netmask  = "10.10.0.0/16"
  tags        = ["Automation", "Terraform"]
}

# Texas Development Server
resource "scm_address_object" "texas_dev_server" {
  folder      = var.folder_name
  name        = "texas-dev-server"
  description = "Texas development server"
  ip_netmask  = "10.20.30.40/32"
  tags        = ["Automation", "Terraform"]
}

# Texas Web Server
resource "scm_address_object" "texas_web_server" {
  folder      = var.folder_name
  name        = "texas-web-server"
  description = "Texas web server"
  ip_netmask  = "10.20.30.50/32"
  tags        = ["Automation", "Terraform"]
}

# Texas Database Server
resource "scm_address_object" "texas_db_server" {
  folder      = var.folder_name
  name        = "texas-db-server"
  description = "Texas database server"
  ip_netmask  = "10.20.30.60/32"
  tags        = ["Automation", "Terraform"]
}

# Texas Public IP Range
resource "scm_address_object" "texas_public_ips" {
  folder      = var.folder_name
  name        = "texas-public-ips"
  description = "Texas public IP address range"
  ip_range    = "203.0.113.1-203.0.113.50"
  tags        = ["Automation", "Terraform"]
}