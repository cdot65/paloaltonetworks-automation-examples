# Texas Tags Configuration

# Location Tags
resource "scm_tag" "texas_tag" {
  folder   = var.folder_name
  name     = "Texas"
  color    = "Blue"
  comments = "State of Texas"
}

resource "scm_tag" "dallas_tag" {
  folder   = var.folder_name
  name     = "Dallas"
  color    = "Red"
  comments = "Dallas, Texas location"
}

resource "scm_tag" "austin_tag" {
  folder   = var.folder_name
  name     = "Austin"
  color    = "Green"
  comments = "Austin, Texas location"
}

resource "scm_tag" "houston_tag" {
  folder   = var.folder_name
  name     = "Houston"
  color    = "Yellow"
  comments = "Houston, Texas location"
}

resource "scm_tag" "san_antonio_tag" {
  folder   = var.folder_name
  name     = "SanAntonio"
  color    = "Orange"
  comments = "San Antonio, Texas location"
}

resource "scm_tag" "fort_worth_tag" {
  folder   = var.folder_name
  name     = "FortWorth"
  color    = "Copper"
  comments = "Fort Worth, Texas location"
}

# Environment Tags
resource "scm_tag" "production_tag" {
  folder   = var.folder_name
  name     = "Production"
  color    = "Red"
  comments = "Production environment"
}

resource "scm_tag" "development_tag" {
  folder   = var.folder_name
  name     = "Development"
  color    = "Yellow"
  comments = "Development environment"
}

resource "scm_tag" "staging_tag" {
  folder   = var.folder_name
  name     = "Staging"
  color    = "Orange"
  comments = "Staging environment"
}

# Infrastructure Tags
resource "scm_tag" "datacenter_tag" {
  folder   = var.folder_name
  name     = "Datacenter"
  color    = "Midnight Blue"
  comments = "Datacenter infrastructure"
}

resource "scm_tag" "web_server_tag" {
  folder   = var.folder_name
  name     = "WebServer"
  color    = "Green"
  comments = "Web server resources"
}

resource "scm_tag" "database_tag" {
  folder   = var.folder_name
  name     = "Database"
  color    = "Purple"
  comments = "Database resources"
}

# Management Tags
resource "scm_tag" "automation_tag" {
  folder   = var.folder_name
  name     = "Automation"
  color    = "Cyan"
  comments = "Managed by automation"
}

resource "scm_tag" "terraform_tag" {
  folder   = var.folder_name
  name     = "Terraform"
  color    = "Purple"
  comments = "Managed by Terraform"
}