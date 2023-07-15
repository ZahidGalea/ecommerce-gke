resource "google_container_cluster" "cluster" {
  name             = "ecommerce-gke"
  location         = local.default_region
  enable_autopilot = true

  master_auth {

    client_certificate_config {
      issue_client_certificate = false
    }
  }

  lifecycle = [reservation_affinity, machine_type]

  network    = google_compute_network.ecommerce-vpc.name
  subnetwork = google_compute_subnetwork.subnetwork-gke-base.name

  node_config {
    machine_type = "n1-standard-1"

    metadata = {
      disable-legacy-endpoints = "true"
    }

  }
}