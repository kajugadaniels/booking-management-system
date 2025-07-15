import os
import json
import requests
import logging
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

IREMBO_BASE_URL = os.getenv("IREMBO_BASE_URL", "https://api.sandbox.irembopay.com")
IREMBO_SECRET_KEY = os.getenv("IREMBO_SECRET_KEY")
PAYMENT_ACCOUNT_IDENTIFIER = "PI-3631756955"
PRODUCT_CODE = "PC-cbcb0ba1e3"

def createInvoiceOnIremboPay(invoiceNumber, amount, description, callbackUrl, customerEmail, customerName, customerPhone="0780000001"):
    url = f"{IREMBO_BASE_URL}/payments/invoices"

    payload = {
        "transactionId": invoiceNumber,
        "paymentAccountIdentifier": PAYMENT_ACCOUNT_IDENTIFIER,
        "customer": {
            "email": customerEmail,
            "phoneNumber": customerPhone,
            "name": customerName,
        },
        "paymentItems": [
            {
                "unitAmount": int(amount),
                "quantity": 1,
                "code": PRODUCT_CODE
            }
        ],
        "description": description,
        "expiryAt": (datetime.now() + timedelta(hours=1)).isoformat(),
        "language": "EN"
    }

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "PlutoBookingApp",
        "irembopay-secretKey": IREMBO_SECRET_KEY
    }

    print("🔄 Creating Irembo Invoice...")
    print("📦 Payload:", json.dumps(payload, indent=2))
    print("🔐 Headers:", headers)

    try:
        response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
        data = response.json()
    except ValueError:
        data = {"error": "Invalid JSON response"}
    except requests.RequestException as e:
        logging.error(f"🔌 Network error: {e}")
        return 500, {"error": "Network error"}

    print(f"📡 IremboPay Response [{response.status_code}]:", json.dumps(data, indent=2))
    return response.status_code, data
