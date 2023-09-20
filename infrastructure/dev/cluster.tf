resource "google_container_cluster" "cluster" {
  count = 0 # TODO: Remover
  name             = "ecommerce-gke"
  location         = local.default_region
  enable_autopilot = true

  master_auth {

    client_certificate_config {
      issue_client_certificate = false
    }
  }

  network    = google_compute_network.ecommerce-vpc.name
  subnetwork = google_compute_subnetwork.subnetwork-gke-base.name

  node_config {
    machine_type = "e2-medium"

    metadata = {
      disable-legacy-endpoints = "true"
    }

    reservation_affinity {
      consume_reservation_type = "NO_RESERVATION"
    }

  }
}