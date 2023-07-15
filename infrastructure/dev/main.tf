locals {
  project_name   = "ecommerce-dev"
  project_number = "1061889385151"
  project_id     = "ecommerce-dev-392819"
  default_region = "us-east1"
  default_zone   = "us-east1-c"
  environment    = "dev"
}


provider "google" {
  project = local.project_id
  region  = local.default_region
  zone    = local.default_zone
}

provider "google-beta" {
  project = local.project_id
  region  = local.default_region
  zone    = local.default_zone
}

module "project-services" {
  source  = "terraform-google-modules/project-factory/google//modules/project_services"
  version = "~> 14.2"

  project_id = local.project_id

  activate_apis = [
    "cloudresourcemanager.googleapis.com",
    "containerregistry.googleapis.com",
    "run.googleapis.com",
    "compute.googleapis.com",
    "container.googleapis.com",
    "artifactregistry.googleapis.com"

  ]
}
