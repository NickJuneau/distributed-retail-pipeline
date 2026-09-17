import csv
import json
from datetime import datetime, timezone

""" Parses retail dataset by row and assigns an event type.


    Output: JSON format of all datapoints from the table along with the given event type.
"""
def main():

    count = 0
    ROWS_TO_READ = 541910

    purchaseCount = 0
    adjustmentCount = 0
    cancellationCount = 0
    promotionCount = 0
    unknownCount = 0
    
    with open(file='data/online-retail-dataset.csv', mode='r', encoding='utf-8-sig') as file:
        
        MAX_ROWS = sum(1 for line in file)

        # Checks edgecase if ROWS_TO_READ is longer than csv file inputed
        if ROWS_TO_READ > MAX_ROWS:
            ROWS_TO_READ = MAX_ROWS


        # Resets the pointer back to top of file
        file.seek(0)

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
            elif eventDict["eventType"] == "PROMOTION":
                promotionCount += 1
            elif eventDict["eventType"] == "UNKNOWN":
                unknownCount += 1
            
            # print(jsonString)

            count += 1
            if count == ROWS_TO_READ: # This loop will read ROWS_TO_READ amount of rows
                break

        print(f"Purchases: {purchaseCount}\nAdjustments: {adjustmentCount}\nCancellations: {cancellationCount}\nPromotions: {promotionCount}\nUnknowns: {unknownCount}")

            
""" Helper function to classify which type of event took place in each transaction

    Args:
        row: The row being observed and passed by the main method

    Returns: 
        String of event type of the following options: PURCHASE, ADJUSTMENT, CANCELLATION, PROMOTION, and UNKNOWN. 
        UNKNOWN is a catch all however nothing shall fall into unknown
"""
def classifyEvent(row):
    # TODO Return Type: Type of event... ENUM? For now will skip ENUM but I think it fits here
    
    # Possible event types: PURCHASE, ADJUSTMENT, CANCELLATION, PROMOTION, and UNKNOWN (Unknown should never happen but is for anomalies not caught)
    retEventType = "NONE"

    # Get common vars
    stockCode = row["StockCode"]
    invoiceNumber = row["InvoiceNo"]
    price = row["UnitPrice"]
    quantity = row["Quantity"]


    # ADJUSTMENT: Checks for non-inventory stock codes (`D`, `POST`, `M`, `BANK CHARGES`, `B` etc.)
    # Second case accounts for internal store write-offs for damaged, lost, or expired stock
    if (stockCode == "POST" or stockCode == "D" or stockCode == "M" or stockCode == "BANK CHARGES" or stockCode == "B") or (float(price) == 0 and int(quantity) < 0): 
        retEventType = "ADJUSTMENT"

    # Cancellations (or Returns)
    elif invoiceNumber[0:1] == "C" and float(price) > 0:
        retEventType = "CANCELLATION"

    elif (float(price) > 0 and stockCode != ""): 
        retEventType = "PURCHASE"

    elif float(price) == 0 and int(quantity) > 0:
        retEventType = "PROMOTION"

    #Catches all uncaught events for debugging (VALUE SHOULD BE ZERO IF USER WANTS TYPES FOR ALL)
    else:
        retEventType = "UNKNOWN"
        print("Unknown event type... printing out row")
        print(json.dumps(row, indent=2)+"\n")

    return retEventType

if __name__ == "__main__":
    main()