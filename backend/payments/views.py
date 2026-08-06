import base64
import json
import uuid
from django.conf import settings
from django.db import transaction
from django.shortcuts import get_object_or_404, render
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from appointments.models import Appointment
from payments.models import Payment, PendingPayment
from payments.serializers import PaymentInitiateSerializer
from payments.services import EsewaService
from users.models import Doctor

class PaymentInitiateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = PaymentInitiateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        patient = request.user.patient_profile

        doctor = get_object_or_404(
            Doctor,
            id=serializer.validated_data["doctor"]
        )

        appointment_date = serializer.validated_data["appointment_date"]

        transaction_uuid = uuid.uuid4()
        try:
            pending_payment = PendingPayment.objects.create(
                patient=patient,
                doctor=doctor,
                appointment_date=appointment_date,
                transaction_uuid=transaction_uuid,
            )

            payment_data = EsewaService.create_payment_data(
                pending_payment
            )
        except Exception:
            pending_payment.delete()
            raise

        return Response(
            payment_data,
            status=status.HTTP_200_OK
        )


class PaymentSuccessAPIView(APIView):

    permission_classes = []

    def get(self, request):

        encoded_data = request.GET.get("data")

        if not encoded_data:
            return Response(
                {"detail": "No payment data received."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            decoded_data = base64.b64decode(encoded_data).decode("utf-8")
            payment_data = json.loads(decoded_data)
            transaction_uuid = payment_data["transaction_uuid"]

            pending_payment = get_object_or_404(
            PendingPayment,
            transaction_uuid=transaction_uuid,
)
            esewa_response = EsewaService.verify_payment(
            transaction_uuid=transaction_uuid,
            total_amount=settings.CONSULTATION_FEE,
)

            if esewa_response.get("status") != "COMPLETE":
                return Response(
        {"detail": "Payment verification failed."},
        status=status.HTTP_400_BAD_REQUEST,
    )
            with transaction.atomic():

    # Lock doctor row
                Doctor.objects.select_for_update().get(
                id=pending_payment.doctor_id
    )

    # Check if slot is still available
                appointment_exists = Appointment.objects.filter(
                doctor=pending_payment.doctor,
                appointment_date=pending_payment.appointment_date,
    ).exists()

                if appointment_exists:
                    raise ValidationError(
                        "Appointment slot is already booked."
        )

    # Create appointment
                appointment = Appointment.objects.create(
                    doctor=pending_payment.doctor,
                    patient=pending_payment.patient,
                    appointment_date=pending_payment.appointment_date,
    )

    # Create payment
                Payment.objects.create(
                    appointment=appointment,
                    transaction_id=payment_data["transaction_code"],
                    gateway="esewa",
                    amount=settings.CONSULTATION_FEE,
    )

    # Delete temporary payment
                pending_payment.delete()

        except Exception:
                        return Response(
                            {"detail": "Invalid payment data."},
                status=status.HTTP_400_BAD_REQUEST,
                        )

        return Response(
    {
        "message": "Appointment booked successfully.",
        "appointment_id": appointment.appointment_id,
    },
    status=status.HTTP_201_CREATED,
)