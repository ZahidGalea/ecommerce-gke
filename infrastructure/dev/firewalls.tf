resource "google_compute_firewall" "front-end-firewall" {
  name    = "gke-firewall"
  network = google_compute_network.ecommerce-vpc.name

  allow {
    protocol = "tcp"
    ports    = ["80", "443"]
  }

  source_ranges = ["0.0.0.0/0"]
}