from django.http import response
from django.shortcuts import render

# Create your views here.
import uuid

from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from users.models import Doctor
from payments.models import PendingPayment
from payments.serializers import PaymentInitiateSerializer
from payments.services import EsewaService

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
from django.conf import settings
from django.db import transaction
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from appointments.models import Appointment
from payments.models import Payment, PendingPayment
from payments.serializers import PaymentVerifySerializer
from payments.services import EsewaService
from users.models import Doctor


class PaymentVerifyAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = PaymentVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        transaction_uuid = serializer.validated_data["transaction_uuid"]

        # Verify payment with Esewa
        esewa_response = EsewaService.verify_payment(transaction_uuid)

        if esewa_response["status"] != "COMPLETE":
            return Response(
                {
                    "detail": "Payment not completed."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get pending payment
        pending_payment.gateway_reference = response["transaction_uuid"]
        pending_payment.save()

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
                # TODO: Refund payment
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
                transaction_id=transaction_uuid,
                gateway="esewa",
                amount=settings.CONSULTATION_FEE,
            )

            # Remove temporary booking
            pending_payment.delete()

        return Response(
            {
                "message": "Appointment booked successfully.",
                "appointment_id": appointment.id
            },
            status=status.HTTP_201_CREATED
        )