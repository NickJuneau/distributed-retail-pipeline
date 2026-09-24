from services.replay.parser import normalizeRow
import csv, json, time, random

def main():
    with open(file='data/online-retail-dataset.csv', mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)

        for row in reader:
            rowDict = normalizeRow(row)
            jsonStr = json.dumps(rowDict)

            print(jsonStr)

            # Will stream a new transaction between every x and y seconds
            time.sleep(random.uniform(.1, 1))

if __name__ == "__main__":
    main()