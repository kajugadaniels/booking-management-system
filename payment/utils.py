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

def createInvoiceOnIremboPay(invoiceNumber, amount, description, callbackUrl):
    """
    Creates a valid invoice on IremboPay using proper headers and payload structure.
    """

    url = f"{IREMBO_BASE_URL}/payments/invoices"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "irembopay-secretKey": IREMBO_SECRET_KEY
    }

    # Dummy customer info for now; should be passed in dynamically for production
    payload = {
        "transactionId": invoiceNumber,
        "paymentAccountIdentifier": "TST-RWF",  # Replace with real ID from Irembo dashboard
        "customer": {
            "email": "user@email.com",           # Replace with request.user.email
            "phoneNumber": "0780000001",         # Optional unless required
            "name": "John Doe"                   # Replace with request.user.get_full_name()
        },
        "paymentItems": [
            {
                "unitAmount": int(float(amount) * 1300),  # USD → RWF approx
                "quantity": 1,
                "code": "PC-aaf751b73f"  # Replace with real product code
            }
        ],
        "description": description,
        "expiryAt": (datetime.now() + timedelta(hours=1)).isoformat(),
        "language": "EN"
    }

    # Debug logging
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
