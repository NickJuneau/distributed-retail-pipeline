import json
import sys
from google.cloud import pubsub_v1
from google.cloud import bigquery

# Configuration constants
PROJECT_ID = "distributed-retail-pipeline"
SUBSCRIPTION_ID = "retail-transactions-sub"
DATASET_ID = "retail_analytics"
TABLE_ID = "transactions"

TABLE_REF = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"

# Initialize GCP Clients
bq_client = bigquery.Client(project=PROJECT_ID)
subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)
