from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

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

        doctor = Doctor.objects.get(id=doctor_id)

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