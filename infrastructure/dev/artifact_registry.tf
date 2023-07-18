resource "google_artifact_registry_repository" "front-app" {
  location      = local.default_region
  repository_id = "presentation"
  format        = "DOCKER"
}