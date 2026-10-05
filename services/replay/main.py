from services.replay.parser import normalizeRow
import csv, json, time, random
from google.cloud import pubsub_v1

CSV_PATH = 'data/online-retail-dataset.csv'
MAX_EVENTS = 10 # Set to None for full run

def main():
    # initialize the Pub/Sub publisher client
    publisher = pubsub_v1.PublisherClient()

    # Build full topic path
    project_id = "distributed-retail-pipeline"
    topic_id = "retail-transactions"
    topic_path = publisher.topic_path(project_id, topic_id)

    print(f"Publishing event stream to GCP Pub/Sub topic: {topic_path}...\n")

    count = 0

    with open(file=CSV_PATH, mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)

        for row in reader:
            try:
                rowDict = normalizeRow(row)
                jsonStr = json.dumps(rowDict)

                # print(jsonStr)
                # Encode JSON string as UTF-8 bytes
                data_bytes = jsonStr.encode("utf-8")

                # Publish to GCP Pub/Sub and wait for GCP confirmation
                future = publisher.publish(topic_path, data=data_bytes)
                message_id = future.result()

                print(f"[{count + 1}] Published Invoice {rowDict['invoice_no']} -> Message ID: {message_id}")

                count+=1
                # If MAX_EVENTS is None it will skip the if statement (Short Cicruit)
                if MAX_EVENTS and count >= MAX_EVENTS:
                    print(f"\nReached dev limit of {MAX_EVENTS} transactions.")
                    break

                # Will stream a new transaction between every x and y seconds
                time.sleep(random.uniform(.1, 1))
            except Exception as e:
                print(f"Error processing row: {e}")
                continue

if __name__ == "__main__":
    main()