import json
import requests
import logging
from datetime import datetime, timedelta

IREMBO_BASE_URL = "https://api.sandbox.irembopay.com"
IREMBO_SECRET_KEY = "sk_live_0dfc743de0684ab29df884a8c36d8da9"  # ✅ YOUR secret key here

def createInvoiceOnIremboPay(invoiceNumber, amount, description, callbackUrl):
    """
    Creates a valid invoice on IremboPay using proper headers and payload.
    """

    url = f"{IREMBO_BASE_URL}/payments/invoices"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "irembopay-secretKey": IREMBO_SECRET_KEY  # ✅ Correct header
    }

    # Dummy data for required fields — adapt to real values if available
    payload = {
        "transactionId": invoiceNumber,
        "paymentAccountIdentifier": "TST-RWF",  # ✅ For testing/sandbox
        "customer": {
            "email": "user@email.com",  # ❗️ Replace with real user email
            "phoneNumber": "0780000001",  # ❗️ Optional if not required
            "name": "John Doe"  # ❗️ Replace with user full name
        },
        "paymentItems": [
            {
                "unitAmount": int(float(amount) * 1300),  # Convert USD → RWF approx
                "quantity": 1,
                "code": "PC-aaf751b73f"  # ❗️ Must be a valid product code from Irembo dashboard
            }
        ],
        "description": description,
        "expiryAt": (datetime.now() + timedelta(hours=1)).isoformat(),
        "language": "EN"
    }

    print("🔄 Creating Irembo Invoice...")
    print("📦 Payload:", json.dumps(payload, indent=2))
    print("🔐 Headers:", headers)

    response = requests.post(url, headers=headers, json=payload)

    try:
        data = response.json()
    except ValueError:
        data = {"error": "Invalid JSON response"}

    print(f"📡 IremboPay Response [{response.status_code}]:", json.dumps(data, indent=2))

    return response.status_code, data
