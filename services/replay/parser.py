import csv
import json
from datetime import datetime, timezone

def main():

    count = 0
    ROWS_TO_READ = 10000

    purchaseCount = 0
    adjustmentCount = 0
    cancellationCount = 0
    unknownCount = 0
    unaccountedCases = 0
    
    with open(file='data/online-retail-dataset.csv', mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)

        for row in reader:
            eventType = classifyEvent(row)

            eventDict = {
                "invoiceNo": row["InvoiceNo"],
                "eventType": eventType,
                "stockCode": row["StockCode"],
                "description": row["Description"].strip() if row["Description"] else "",
                "quantity": int(row["Quantity"]),
                "unitPrice": float(row["UnitPrice"]),
                "customerId": row["CustomerID"] if row["CustomerID"] else None,
                "country": row["Country"], 
                "sourceEventTime": row["InvoiceDate"], 
                "replayedAt": datetime.now(timezone.utc).isoformat()
            }

            jsonString = json.dumps(eventDict, indent=2)

            # Get counts for testing
            if eventDict["eventType"] == "PURCHASE":
                purchaseCount += 1
            elif eventDict["eventType"] == "ADJUSTMENT":
                adjustmentCount += 1
            elif eventDict["eventType"] == "CANCELLATION":
                cancellationCount += 1
            elif eventDict["eventType"] == "UNKNOWN":
                unknownCount += 1
            elif eventDict["eventType"] == "NONE":
                unaccountedCases += 1
            
            # print(jsonString)

            count += 1
            if count == ROWS_TO_READ: # This loop will read ROWS_TO_READ amount of rows
                print(f"Purchases: {purchaseCount}\nAdjustments: {adjustmentCount}\nCancellations: {cancellationCount}\nUnknowns: {unknownCount}\nLeftover: {unaccountedCases}")
                break

            

def classifyEvent(row):
    # TODO implement code to decide what type of event
    # Return Type: Type of event... ENUM? For now will skip ENUM but I think it fits here
    
    # Possible event types: PURCHASE, ADJUSTMENT, CANCELLATION, or UNKNOWN
    retEventType = "NONE"

    # Get common vars
    stockCode = row["StockCode"]
    invoiceNumber = row["InvoiceNo"]
    price = row["UnitPrice"]


    # ADJUSTMENT: Check for non-inventory stock codes (`D`, `POST`, `M`, `BANK CHARGES`, etc.)
    if stockCode == "POST" or stockCode == "D" or stockCode == "M" or stockCode == "BANK CHARGES":
        retEventType = "ADJUSTMENT"
    elif invoiceNumber[0:1] == "C" and float(price) > 0:
        retEventType = "CANCELLATION"
    elif float(price) > 0 and stockCode != None:
        retEventType = "PURCHASE"
    else:
        retEventType = "UNKNOWN"
        print("Unknown event type... printing out row")
        print(json.dumps(row, indent=2)+"\n")

    return retEventType

if __name__ == "__main__":
    main()