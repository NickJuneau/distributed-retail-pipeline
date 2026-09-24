from services.replay.parser import normalizeRow
import csv, json, time, random

CSV_PATH = 'data/online-retail-dataset.csv'
MAX_EVENTS = 20 # Set to None for full run

def main():
    count = 0

    with open(file=CSV_PATH, mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)

        for row in reader:
            try:
                rowDict = normalizeRow(row)
                jsonStr = json.dumps(rowDict)

                print(jsonStr)

                count+=1
                # If MAX_EVENTS is None it will skip the if statement (Short Cicruit)
                if MAX_EVENTS and count >= MAX_EVENTS:
                    print(f"\nReached dev limit of {MAX_EVENTS} transactions. Exiting...")
                    break

                # Will stream a new transaction between every x and y seconds
                time.sleep(random.uniform(.1, 1))
            except Exception as e:
                print(f"Error processing row: {e}")
                continue

if __name__ == "__main__":
    main()