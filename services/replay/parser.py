import csv
import json
from datetime import datetime, timezone

""" Parses retail dataset by row and assigns an event type.


    Output: JSON format of all datapoints from the table along with the given event type.
"""
def main():

    count = 0
    # If read all is true, ROWS_TO_READ will not matter. ROWS_TO_READ is for testing code only
    ROWS_TO_READ = 10000
    READ_ALL = True

    purchaseCount = 0
    adjustmentCount = 0
    cancellationCount = 0
    promotionCount = 0
    unknownCount = 0
    
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
                "sourceEventTime": toUTC(row["InvoiceDate"]), 
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
            # If user wants to read all rows, set READ_ALL to True
            if count == ROWS_TO_READ and READ_ALL == False:
                break

        print(f"Purchases: {purchaseCount}\nAdjustments: {adjustmentCount}\nCancellations: {cancellationCount}\nPromotions: {promotionCount}\nUnknowns: {unknownCount}")

            
""" Helper function to classify which type of event took place in each transaction

    Args:
        row: The row being observed and passed by the main method

    Returns: 
        Event type of the following options: PURCHASE, ADJUSTMENT, CANCELLATION, PROMOTION, and UNKNOWN. 
        UNKNOWN is a catch all however nothing shall fall into unknown
"""
def classifyEvent(row) -> str:
    # TODO Return Type: Type of event... ENUM? For now will skip ENUM but I think it fits here
    
    # Possible event types: PURCHASE, ADJUSTMENT, CANCELLATION, PROMOTION, and UNKNOWN (Unknown should never happen but is for anomalies not caught)
    retEventType = "NONE"

    # Get common vars
    stockCodeClean = row["StockCode"].strip().upper()
    invoiceNumber = row["InvoiceNo"]
    price = row["UnitPrice"]
    quantity = row["Quantity"]


    # ADJUSTMENT: Checks for non-inventory stock codes (`D`, `POST`, `M`, `BANK CHARGES`, `B` etc.)
    NON_INVENTORY_CODES = {"POST", "D", "M", "BANK CHARGES", "B"}

    # Second case accounts for internal store write-offs for damaged, lost, or expired stock
    if stockCodeClean in NON_INVENTORY_CODES or (float(price) == 0 and int(quantity) < 0): 
        retEventType = "ADJUSTMENT"

    # Cancellations (or Returns)
    elif invoiceNumber[0:1] == "C" and float(price) > 0:
        retEventType = "CANCELLATION"

    elif (float(price) > 0 and stockCodeClean != ""): 
        retEventType = "PURCHASE"

    elif float(price) == 0 and int(quantity) > 0:
        retEventType = "PROMOTION"

    #Catches all uncaught events for debugging (VALUE SHOULD BE ZERO IF USER WANTS TYPES FOR ALL)
    else:
        retEventType = "UNKNOWN"
        print("Unknown event type... printing out row")
        print(json.dumps(row, indent=2)+"\n")

    return retEventType

""" Helper function to translate the given date and time to standard ISO-8601 

    Args:
        date: The raw date and time string from the dataset column.

    Returns:
        The formatted ISO-8601 UTC timestamp
"""
def toUTC(date) -> str:
    dt = datetime.strptime(date.strip(), "%m/%d/%Y %H:%M")
    return dt.replace(tzinfo=timezone.utc).isoformat()

if __name__ == "__main__":
    main()