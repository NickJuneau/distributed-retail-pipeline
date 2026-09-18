from services.replay.parser import classifyEvent, normalizeRow, toUTC

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

def test_null_customer_id():
    mock_row = {
        "InvoiceNo": "536365",
        "StockCode": "85123A",
        "Description": "WHITE HANGING HEART T-LIGHT HOLDER",
        "Quantity": "6",
        "InvoiceDate": "12/1/2010 9:41",
        "UnitPrice": "2.55",
        "CustomerID": "",
        "Country": "United Kingdom"
    }

    result = normalizeRow(mock_row)
    assert result["customer_id"] is None

def test_timestamp_formatting():
    raw_date = "12/1/2010 11:38"
    parsed_date = toUTC(raw_date)
    assert parsed_date == "2010-12-01T11:38:00+00:00"