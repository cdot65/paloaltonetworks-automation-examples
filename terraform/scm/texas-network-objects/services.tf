# Texas Services Configuration

# Web Services
resource "scm_service" "web_http" {
  folder      = var.folder_name
  name        = "texas-http"
  description = "Texas HTTP Service"
  protocol = {
    tcp = {
      port = "80"
    }
  }
  tags = [scm_tag.texas_tag.name, scm_tag.web_server_tag.name, scm_tag.automation_tag.name, scm_tag.terraform_tag.name]
}

resource "scm_service" "web_https" {
  folder      = var.folder_name
  name        = "texas-https"
  description = "Texas HTTPS Service"
  protocol = {
    tcp = {
      port = "443"
    }
  }
  tags = [scm_tag.texas_tag.name, scm_tag.web_server_tag.name, scm_tag.automation_tag.name, scm_tag.terraform_tag.name]
}

# Database Services
resource "scm_service" "db_mysql" {
  folder      = var.folder_name
  name        = "texas-mysql"
  description = "Texas MySQL Service"
  protocol = {
    tcp = {
      port = "3306"
    }
  }
  tags = [scm_tag.texas_tag.name, scm_tag.database_tag.name, scm_tag.automation_tag.name, scm_tag.terraform_tag.name]
}

resource "scm_service" "db_mssql" {
  folder      = var.folder_name
  name        = "texas-mssql"
  description = "Texas Microsoft SQL Service"
  protocol = {
    tcp = {
      port = "1433"
    }
  }
  tags = [scm_tag.texas_tag.name, scm_tag.database_tag.name, scm_tag.automation_tag.name, scm_tag.terraform_tag.name]
}

resource "scm_service" "db_postgres" {
  folder      = var.folder_name
  name        = "texas-postgres"
  description = "Texas PostgreSQL Service"
  protocol = {
    tcp = {
      port = "5432"
    }
  }
  tags = [scm_tag.texas_tag.name, scm_tag.database_tag.name, scm_tag.automation_tag.name, scm_tag.terraform_tag.name]
}

# Management Services
resource "scm_service" "mgmt_ssh" {
  folder      = var.folder_name
  name        = "texas-ssh"
  description = "Texas SSH Service"
  protocol = {
    tcp = {
      port = "22"
    }
  }
  tags = [scm_tag.texas_tag.name, scm_tag.automation_tag.name, scm_tag.terraform_tag.name]
}

resource "scm_service" "mgmt_rdp" {
  folder      = var.folder_name
  name        = "texas-rdp"
  description = "Texas RDP Service"
  protocol = {
    tcp = {
      port = "3389"
    }
  }
  tags = [scm_tag.texas_tag.name, scm_tag.automation_tag.name, scm_tag.terraform_tag.name]
}

# Application Services
resource "scm_service" "app_custom_tcp" {
  folder      = var.folder_name
  name        = "texas-custom-app-tcp"
  description = "Texas Custom Application TCP Service"
  protocol = {
    tcp = {
      port = "8080-8090"
    }
  }
  tags = [scm_tag.texas_tag.name, scm_tag.web_server_tag.name, scm_tag.automation_tag.name, scm_tag.terraform_tag.name]
}

resource "scm_service" "app_custom_udp" {
  folder      = var.folder_name
  name        = "texas-custom-app-udp"
  description = "Texas Custom Application UDP Service"
  protocol = {
    udp = {
      port = "9000-9010"
    }
  }
  tags = [scm_tag.texas_tag.name, scm_tag.automation_tag.name, scm_tag.terraform_tag.name]
}