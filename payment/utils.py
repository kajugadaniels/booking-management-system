import requests
import logging

IREMBO_BASE_URL = "https://api.sandbox.irembopay.com"
IREMBO_SECRET_KEY = "sk_live_0dfc743de0684ab29df884a8c36d8da9"

def createInvoiceOnIremboPay(invoiceNumber, amount, description, callbackUrl):
    """
    Creates an invoice on IremboPay via their REST API.
    """
    url = f"{IREMBO_BASE_URL}/payments/invoices"

    headers = {
        "Authorization": f"Bearer {IREMBO_SECRET_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "invoiceNumber": invoiceNumber,
        "amount": str(amount),  # Irembo expects a string
        "currency": "RWF",
        "description": description,
        "callbackUrl": callbackUrl
    }

    response = requests.post(url, headers=headers, json=payload)

    try:
        data = response.json()
    except ValueError:
        data = {"error": "Invalid JSON response"}

    logging.info(f"IremboPay Invoice Response: {response.status_code} - {data}")
    return response.status_code, data
