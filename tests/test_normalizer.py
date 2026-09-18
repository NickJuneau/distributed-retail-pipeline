from services.replay.parser import classifyEvent

def test_classify_purchase():
    mock_row = {
        "InvoiceNo": "536365",
        "StockCode": "85123A",
        "UnitPrice": "2.55",
        "Quantity": "6"
    }

    result = classifyEvent(mock_row)
    assert result == "PURCHASE"

def test_classify_cancellation():
    mock_row = {
        "InvoiceNo": "C536391",
        "StockCode": "22556",
        "UnitPrice": "1.65",
        "Quantity": "-12"
    }

    result = classifyEvent(mock_row)
    assert result == "CANCELLATION"

def test_classify_adjustment():
    mock_row1 = {
        "InvoiceNo": "536370",
        "StockCode": "POST",
        "UnitPrice": "18",
        "Quantity": "3"
    }

    result1 = classifyEvent(mock_row1)
    assert result1 == "ADJUSTMENT"

    mock_row2 = {
        "InvoiceNo": "536370",
        "StockCode": "82486",
        "UnitPrice": "0",
        "Quantity": "-23"
    }

    result2 = classifyEvent(mock_row2)
    assert result2 == "ADJUSTMENT"

def test_classify_promotion():
    mock_row = {
        "InvoiceNo": "536370",
        "StockCode": "82486",
        "UnitPrice": "0",
        "Quantity": "10"
    }

    result = classifyEvent(mock_row)
    assert result == "PROMOTION"


"""In order to complete both null customer and timestamp test 
   I will have to first refactor parser.py and create normalizeRow() 
   function to handle creating a row and assigning values
"""
# TODO Implement null customer id test 
# def test_classify_null_customer_id():

    

# TODO Implement timestamp test
