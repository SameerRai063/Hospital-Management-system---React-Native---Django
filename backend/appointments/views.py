from django.shortcuts import render
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from appointments.models import Appointment
from appointments.serializer import AppointmentSerializer

class AppointmentListAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        appointments = Appointment.objects.all()

        serializer = AppointmentSerializer(
            appointments,
            many=True,
        )

        return Response(serializer.data)
class MyAppointmentAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        patient = request.user.patient_profile

        appointments = Appointment.objects.filter(
            patient=patient
        )

        serializer = AppointmentSerializer(
            appointments,
            many=True,
        )

        return Response(serializer.data)
class DoctorAppointmentAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        doctor = request.user.doctor_profile

        appointments = Appointment.objects.filter(
            doctor=doctor
        )

        serializer = AppointmentSerializer(
            appointments,
            many=True,
        )

        return Response(serializer.data)
class AppointmentDeleteAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request, appointment_id):

        if request.user.role == "patient":

            appointment = get_object_or_404(
                Appointment,
                id=appointment_id,
                patient=request.user.patient_profile,
            )

        elif request.user.role == "doctor":

            appointment = get_object_or_404(
                Appointment,
                id=appointment_id,
                doctor=request.user.doctor_profile,
            )

        else:

            return Response(
                {
                    "detail": "You are not allowed to delete appointments."
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        appointment.delete()

        return Response(
            {
                "message": "Appointment deleted successfully."
            },
            status=status.HTTP_200_OK,
        )