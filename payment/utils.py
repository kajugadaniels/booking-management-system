import json
import requests
import logging

IREMBO_BASE_URL = "https://api.sandbox.irembopay.com"
IREMBO_SECRET_KEY = "pk_live_a780e931399b42f6a135dd09e897ec32"

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

    print("🔄 Creating Irembo Invoice...")
    print("📦 Payload:", json.dumps(payload, indent=2))
    print("🔐 Auth Header:", headers["Authorization"])

    response = requests.post(url, headers=headers, json=payload)

    try:
        data = response.json()
    except ValueError:
        data = {"error": "Invalid JSON response"}

    print(f"📡 IremboPay Response [{response.status_code}]:", data)

    return response.status_code, data