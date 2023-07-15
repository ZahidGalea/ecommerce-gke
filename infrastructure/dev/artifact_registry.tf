resource "google_artifact_registry_repository" "my-repo" {
  location      = local.default_region
  repository_id = "front-app"
  format        = "DOCKER"

  docker_config {
    immutable_tags = true
  }
}