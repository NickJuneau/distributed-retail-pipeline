resource "google_bigquery_dataset" "retail_analytics" {
  dataset_id = "retail_analytics"
  location = var.region
  friendly_name = "Retail Analytics"
  description = "Dataset containing normalized retail transaction events."
}

resource "google_bigquery_table" "transactions" {
  dataset_id = google_bigquery_dataset.retail_analytics.dataset_id
  table_id = "transactions"
  deletion_protection = false

  time_partitioning {
    type = "DAY"
    field = "replayed_at"
  }

  clustering = [ "stock_code", "country", "event_type" ]
  
  schema = jsonencode([
    {
      name = "invoice_no"
      type = "STRING"
      mode = "REQUIRED"
    },
    {
      name = "event_type"
      type = "STRING"
      mode = "NULLABLE"
    },
    {
      name = "stock_code"
      type = "STRING"
      mode = "NULLABLE"
    },
    {
      name = "description"
      type = "STRING"
      mode = "NULLABLE"
    },
    {
      name = "quantity"
      type = "INTEGER"
      mode = "NULLABLE"
    },
    {
      name = "unit_price"
      type = "FLOAT"
      mode = "NULLABLE"
    },
    {
      name = "customer_id"
      type = "STRING"
      mode = "NULLABLE"
    },
    {
      name = "country"
      type = "STRING"
      mode = "NULLABLE"
    },
    {
      name = "source_event_time"
      type = "TIMESTAMP"
      mode = "REQUIRED"
    },
    {
      name = "replayed_at"
      type = "TIMESTAMP"
      mode = "REQUIRED"
    }
  ])
}

resource "google_pubsub_topic" "retail_transactions" {
  name = "retail-transactions"
}

resource "google_pubsub_subscription" "retail_transactions_sub" {
  name = "retail-transactions-sub"
  topic = google_pubsub_topic.retail_transactions.id
  ack_deadline_seconds = 20

  # Retain unacknowledged messages for up to 7 days
  message_retention_duration = "604800s"
}

resource "google_artifact_registry_repository" "retail_repo" {
  location = var.region
  repository_id = "retail-pipeline"
  description = "Docker repository for retail pipeline microservices"
  format = "DOCKER"
}

resource "google_service_account" "replay_vm_sa" {
  account_id = "replay-vm-sa"
  display_name = "Service Account for Replay Producer VM"
}

resource "google_project_iam_member" "replay_pubsub_publisher" {
  project = var.project_id
  role = "roles/pubsub.publisher"
  member = "serviceAccount:${google_service_account.replay_vm_sa.email}"
}

resource "google_project_iam_member" "replay_ar_reader" {
  project = var.project_id
  role = "roles/artifactregistry.reader"
  member = "serviceAccount:${google_service_account.replay_vm_sa.email}"
}

resource "google_compute_instance" "replay_vm" {
  name = "replay-producer-vm"
  machine_type = "e2-micro"
  zone = var.zone

  boot_disk {
    initialize_params {
      image = "cos-cloud/cos-stable"
    }
  }

  network_interface {
    network = "default"
    access_config {}
  }

  service_account {
    email = google_service_account.replay_vm_sa.email
    scopes = ["cloud-platform"]
  }

  # Startup script: Pulls and runs the replay container automatically on boot
  metadata_startup_script = <<-EOF
    #!/bin/bash
    docker-credential-gcr configure-docker --registries=us-central1-docker.pkg.dev
    docker run -d --restart=always \
      --name replay-producer \
      -e GOOGLE_CLOUD_PROJECT="${var.project_id}" \
      us-central1-docker.pkg.dev/${var.project_id}/retail-pipeline/replay-service:v1 \
      --limit 100 --delay 1.0
  EOF

  depends_on = [ 
    google_artifact_registry_repository.retail_repo, 
    google_project_iam_member.replay_ar_reader,
    google_project_iam_member.replay_pubsub_publisher
  ]
}

