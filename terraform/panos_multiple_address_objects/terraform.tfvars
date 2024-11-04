# Firewall Connection Details
hostname = "192.168.255.55"
username = "terraform"
password = "this-is-an-example"

# List of Address Objects
address_objects = {
  "Web-Server-1" = {
    value       = "192.168.1.10"
    description = "Primary web server"
  },
  "Database-Server" = {
    value       = "192.168.1.20"
    description = "Database server"
  },
  "App-Server" = {
    value       = "192.168.1.30"
    description = "Application server"
  }
}
