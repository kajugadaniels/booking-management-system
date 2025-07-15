import os
import json
import requests
import logging
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

IREMBO_BASE_URL = os.getenv("IREMBO_BASE_URL", "https://api.sandbox.irembopay.com")
IREMBO_SECRET_KEY = os.getenv("IREMBO_SECRET_KEY")
IREMBO_PAYMENT_ACCOUNT_ID = os.getenv("IREMBO_PAYMENT_ACCOUNT_ID", "PI-3631756955")
IREMBO_PRODUCT_CODE = os.getenv("IREMBO_PRODUCT_CODE", "PC-cbcb0ba1e3")


def createInvoiceOnIremboPay(invoiceNumber, amount, description, callbackUrl, customerEmail, customerName, customerPhone="0780000001"):
    """
    Creates a valid invoice on IremboPay using their API.
    """

    url = f"{IREMBO_BASE_URL}/payments/invoices"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "irembopay-secretKey": IREMBO_SECRET_KEY
    }

    payload = {
        "transactionId": invoiceNumber,
        "paymentAccountIdentifier": IREMBO_PAYMENT_ACCOUNT_ID,
        "customer": {
            "email": customerEmail,
            "phoneNumber": customerPhone,
            "name": customerName
        },
        "paymentItems": [
            {
                "unitAmount": int(float(amount)),  # already in RWF
                "quantity": 1,
                "code": IREMBO_PRODUCT_CODE
            }
        ],
        "description": description,
        "expiryAt": (datetime.now() + timedelta(hours=1)).isoformat(),
        "language": "EN"
    }

    # Log request for debugging
    print("🔄 Creating Irembo Invoice...")
    print("📦 Payload:", json.dumps(payload, indent=2))
    print("🔐 Headers:", headers)

    try:
        response = requests.post(url, headers=headers, json=payload)
        data = response.json()
    except ValueError:
        data = {"error": "Invalid JSON response"}
    except requests.RequestException as e:
        logging.error(f"🔌 Network error: {e}")
        return 500, {"error": "Network error"}

    print(f"📡 IremboPay Response [{response.status_code}]:", json.dumps(data, indent=2))
    return response.status_code, data
