resource "google_artifact_registry_repository" "front-app-dev" {
  location      = local.default_region
  repository_id = "presentation-dev"
  format        = "DOCKER"
}

resource "google_artifact_registry_repository" "front-app-prod" {
  location      = local.default_region
  repository_id = "presentation-prod"
  format        = "DOCKER"
}