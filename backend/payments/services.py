import base64
import hashlib
import hmac
import requests

from django.conf import settings


class EsewaService:

    @staticmethod
    def generate_signature(message: str):
        secret = settings.ESEWA_SECRET_KEY.encode()

        signature = hmac.new(
            secret,
            message.encode(),
            hashlib.sha256,
        ).digest()

        return base64.b64encode(signature).decode()

    @staticmethod
    def create_payment_data(pending_payment):

        transaction_uuid = str(pending_payment.transaction_uuid)

        message = (
            f"total_amount={settings.CONSULTATION_FEE},"
            f"transaction_uuid={transaction_uuid},"
            f"product_code={settings.ESEWA_PRODUCT_CODE}"
        )

        signature = EsewaService.generate_signature(message)

        return {
            "amount": settings.CONSULTATION_FEE,
            "tax_amount": 0,
            "total_amount": settings.CONSULTATION_FEE,
            "transaction_uuid": transaction_uuid,
            "product_code": settings.ESEWA_PRODUCT_CODE,
            "product_service_charge": 0,
            "product_delivery_charge": 0,
            "success_url": settings.SUCCESS_URL,
            "failure_url": settings.FAILURE_URL,
            "signed_field_names": "total_amount,transaction_uuid,product_code",
            "signature": signature,
        }

    @staticmethod
    def verify_payment(transaction_uuid, total_amount):

        response = requests.get(
            settings.ESEWA_STATUS_URL,
            params={
                "product_code": settings.ESEWA_PRODUCT_CODE,
                "transaction_uuid": transaction_uuid,
                "total_amount": total_amount,
            },
            timeout=10,
        )

        response.raise_for_status()

        return response.json()