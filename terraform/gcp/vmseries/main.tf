# Create VPC Networks (if needed)
resource "google_compute_network" "mgmt" {
  count                   = var.create_networks ? 1 : 0
  name                    = "${var.name_prefix}-${var.mgmt_network_name}"
  auto_create_subnetworks = false
  project                 = var.project_id
}

resource "google_compute_network" "untrust" {
  count                   = var.create_networks ? 1 : 0
  name                    = "${var.name_prefix}-${var.untrust_network_name}"
  auto_create_subnetworks = false
  project                 = var.project_id
}

resource "google_compute_network" "trust" {
  count                   = var.create_networks ? 1 : 0
  name                    = "${var.name_prefix}-${var.trust_network_name}"
  auto_create_subnetworks = false
  project                 = var.project_id
}

# Create Subnets
resource "google_compute_subnetwork" "mgmt" {
  count         = var.create_networks ? 1 : 0
  name          = "${var.name_prefix}-${var.mgmt_subnet_name}"
  ip_cidr_range = var.mgmt_subnet_cidr
  region        = var.region
  network       = google_compute_network.mgmt[0].id
  project       = var.project_id
}

resource "google_compute_subnetwork" "untrust" {
  count         = var.create_networks ? 1 : 0
  name          = "${var.name_prefix}-${var.untrust_subnet_name}"
  ip_cidr_range = var.untrust_subnet_cidr
  region        = var.region
  network       = google_compute_network.untrust[0].id
  project       = var.project_id
}

resource "google_compute_subnetwork" "trust" {
  count         = var.create_networks ? 1 : 0
  name          = "${var.name_prefix}-${var.trust_subnet_name}"
  ip_cidr_range = var.trust_subnet_cidr
  region        = var.region
  network       = google_compute_network.trust[0].id
  project       = var.project_id
}

# Firewall Rules
resource "google_compute_firewall" "mgmt_ingress" {
  name    = "${var.name_prefix}-mgmt-ingress"
  network = var.create_networks ? google_compute_network.mgmt[0].id : var.mgmt_network_name
  project = var.project_id

  allow {
    protocol = "tcp"
    ports    = ["22", "443"]
  }

  source_ranges = var.allowed_mgmt_ips
  target_tags   = var.tags
}

resource "google_compute_firewall" "untrust_ingress" {
  name    = "${var.name_prefix}-untrust-ingress"
  network = var.create_networks ? google_compute_network.untrust[0].id : var.untrust_network_name
  project = var.project_id

  allow {
    protocol = "all"
  }

  source_ranges = ["0.0.0.0/0"]
  target_tags   = var.tags
}

resource "google_compute_firewall" "trust_ingress" {
  name    = "${var.name_prefix}-trust-ingress"
  network = var.create_networks ? google_compute_network.trust[0].id : var.trust_network_name
  project = var.project_id

  allow {
    protocol = "all"
  }

  source_ranges = ["0.0.0.0/0"]
  target_tags   = var.tags
}

# Public IP for Management Interface (optional)
resource "google_compute_address" "mgmt" {
  count   = var.create_public_ip ? 1 : 0
  name    = "${var.name_prefix}-mgmt-ip"
  region  = var.region
  project = var.project_id
}

# VM-Series Instance using the module
module "vmseries" {
  source  = "PaloAltoNetworks/swfw-modules/google//modules/vmseries"
  version = "~> 2.0"

  name              = "${var.name_prefix}-fw"
  zone              = var.zone
  ssh_keys          = var.ssh_keys
  vmseries_image    = var.vmseries_image_name
  machine_type      = var.machine_type
  min_cpu_platform  = var.min_cpu_platform
  tags              = var.tags
  scopes            = var.scopes
  bootstrap_options = var.bootstrap_options

  # Network Interfaces
  network_interfaces = [
    # Management Interface (nic0)
    {
      subnetwork    = var.create_networks ? google_compute_subnetwork.mgmt[0].self_link : var.mgmt_subnet_name
      private_ip    = null
      public_nat    = var.create_public_ip
      public_nat_ip = var.create_public_ip ? google_compute_address.mgmt[0].address : null
    },
    # Untrust Interface (nic1)
    {
      subnetwork    = var.create_networks ? google_compute_subnetwork.untrust[0].self_link : var.untrust_subnet_name
      private_ip    = null
      public_nat    = false
      public_nat_ip = null
    },
    # Trust Interface (nic2)
    {
      subnetwork    = var.create_networks ? google_compute_subnetwork.trust[0].self_link : var.trust_subnet_name
      private_ip    = null
      public_nat    = false
      public_nat_ip = null
    }
  ]

  depends_on = [
    google_compute_subnetwork.mgmt,
    google_compute_subnetwork.untrust,
    google_compute_subnetwork.trust
  ]
}

