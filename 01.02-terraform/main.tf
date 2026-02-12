provider "google" {
  credentials = file(var.credentials)
  project     = var.project
  region      = var.region
}

resource "google_bigquery_dataset" "terraform-bq" {
  dataset_id                  = var.bq_dataset_name
  description                 = "Big Query Dataset"
  location                    = var.location
}

resource "google_storage_bucket" "terraform-bucket" {
  name          = var.gcs_bucket_name
  location      = var.location
  force_destroy = true

uniform_bucket_level_access = true
  

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}