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

def callback(message: pubsub_v1.subscriber.message.Message):
    """Processes incoming Pub/Sub messages and streams them into BigQuery."""
    try:
        payload_str = message.data.decode("utf-8")
        event_dict = json.loads(payload_str)

        errors = bq_client.insert_rows_json(TABLE_REF, [event_dict])

        if not errors:
            invoice_no = event_dict.get("invoice_no", "UNKNOWN")
            print(f"[Worker] Successfully inserted Invoice {invoice_no} into BigQuery")
            message.ack()
        else:
            print(f"[Worker] BigQuery insertion error: {errors}")
            message.ack()

    except Exception as e:
        print(f"[Worker] Error processing message: {e}")
        message.ack()

def main():
    print(f"Ingestion Worker listening on {subscription_path}...\n")
    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)

    with subscriber:
        try:
            streaming_pull_future.result()
        except KeyboardInterrupt:
            print("\nShutting down worker...")
            streaming_pull_future.cancel()

if __name__ == "__main__":
    main()