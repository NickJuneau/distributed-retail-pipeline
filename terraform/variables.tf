variable "project_id" {
    description = "The GCP project ID"
    type = string
    default = "distributed-retail-pipeline"
}

variable "region" {
    description = "The primary GCP region where infrastructure will be deployed"
    type = string
    default = "us-central1"
}

variable "zone" {
    description = "The specific GCP availability zone within the selected region"
    type = string
    default = "us-central1-a"
}
