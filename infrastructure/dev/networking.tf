## VPC CREATION
resource "google_compute_network" "ecommerce-vpc" {
  depends_on              = [module.project-services]
  name                    = "ecommerce-vpc-${local.environment}"
  auto_create_subnetworks = false
}

## SUBNET
resource "google_compute_subnetwork" "subnetwork-database" {
  name          = "ecommerce-database-${local.environment}"
  region        = local.default_region
  network       = google_compute_network.ecommerce-vpc.name
  ip_cidr_range = "10.0.72.0/21" # 16382 IPs
  log_config {
    aggregation_interval = "INTERVAL_30_SEC"
    metadata             = "INCLUDE_ALL_METADATA"
  }
}

resource "google_compute_subnetwork" "subnetwork-gke-base" {
  name          = "gke-base-${local.environment}"
  region        = local.default_region
  network       = google_compute_network.ecommerce-vpc.name
  ip_cidr_range = "10.0.64.0/21" # 16382 IPs
  log_config {
    aggregation_interval = "INTERVAL_30_SEC"
    metadata             = "INCLUDE_ALL_METADATA"
  }
}


## NAT
resource "google_compute_router" "router" {
  name    = "cloudnat-router"
  region  = local.default_region
  network = google_compute_network.ecommerce-vpc.name
  bgp {
    asn = 64514
  }
}

resource "google_compute_router_nat" "nat" {
  project                            = local.project_id
  name                               = "cloudnat-config"
  router                             = google_compute_router.router.name
  region                             = google_compute_router.router.region
  nat_ip_allocate_option             = "AUTO_ONLY"
  source_subnetwork_ip_ranges_to_nat = "ALL_SUBNETWORKS_ALL_IP_RANGES"

  log_config {
    enable = true
    filter = "ERRORS_ONLY"
  }
}