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
    field = "source_event_time"
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
