# payments/services.py

import requests
import uuid

from django.conf import settings


class KhaltiService:

    @staticmethod
    def initiate_payment(
        pending_payment,
        customer_name,
        customer_email,
        customer_phone,
    ):

        headers = {
            "Authorization": f"Key {settings.KHALTI_SECRET_KEY}",
            "Content-Type": "application/json",
        }

        payload = {
            "return_url": settings.KHALTI_RETURN_URL,
            "website_url": settings.WEBSITE_URL,
            "amount": settings.CONSULTATION_FEE * 100,  # Paisa
            "purchase_order_id": str(uuid.uuid4()),
            "purchase_order_name": "Doctor Appointment",

            "customer_info": {
                "name": customer_name,
                "email": customer_email,
                "phone": customer_phone,
            }
        }

        response = requests.post(
            settings.KHALTI_INITIATE_URL,
            json=payload,
            headers=headers,
            timeout=30,
        )

        response.raise_for_status()

        return response.json()

@staticmethod
def verify_payment(pidx):

    headers = {
        "Authorization": f"Key {settings.KHALTI_SECRET_KEY}",
        "Content-Type": "application/json",
    }

    response = requests.post(
        settings.KHALTI_VERIFY_URL,
        json={
            "pidx": pidx
        },
        headers=headers,
        timeout=30,
    )

    response.raise_for_status()

    return response.json()