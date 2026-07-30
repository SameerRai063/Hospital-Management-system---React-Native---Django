from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from users.models import Doctor
from payments.models import PendingPayment
from payments.serializers import PaymentInitiateSerializer
from payments.services import KhaltiService

class PaymentInitiateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = PaymentInitiateSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        doctor_id = serializer.validated_data["doctor"]
        appointment_date = serializer.validated_data["appointment_date"]

        patient = request.user.patient_profile

        doctor = get_object_or_404(
        Doctor,
        id=doctor_id
)

        pending_payment = PendingPayment.objects.create(
            patient=patient,
            doctor=doctor,
            appointment_date=appointment_date,
        )

        response = KhaltiService.initiate_payment(
            pending_payment=pending_payment,
            customer_name=request.user.get_full_name(),
            customer_email=request.user.email,
            customer_phone=request.user.phone_number,
        )

        pending_payment.gateway_reference = response["pidx"]
        pending_payment.save()

        return Response(
            response,
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
from payments.services import KhaltiService
from users.models import Doctor


class PaymentVerifyAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = PaymentVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        pidx = serializer.validated_data["pidx"]

        # Verify payment with Khalti
        khalti_response = KhaltiService.verify_payment(pidx)

        if khalti_response.get("status") != "Completed":
            return Response(
                {
                    "detail": "Payment not completed."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get pending payment
        pending_payment = get_object_or_404(
            PendingPayment,
            gateway_reference=pidx,
            patient=request.user.patient_profile
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
                transaction_id=pidx,
                gateway="khalti",
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