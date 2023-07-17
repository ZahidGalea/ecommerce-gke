resource "google_artifact_registry_repository" "front-app" {
  location      = local.default_region
  repository_id = "front-app"
  format        = "DOCKER"
}