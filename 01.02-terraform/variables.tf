variable "credentials" {
    description = "Service account key"
    default = "gcp-key.json"
}


variable "location" {
    
    description = "location"
    default     = "EU"
}

variable "region" {
    
    description = "region"
    default     = "europe-west1"
}

variable "project" {
    
    description = "project_id"
    default     = "terraform-demo-485515"
}

variable "gcs_bucket_name" {
    
    description = "My storage bucket name"
    default     = "terraform-demo-485515-bucket"
}

variable "bq_dataset_name" {
    
    description = "My Big Query dataset name"
    default     = "terraform_demo_485515_bq"
}


