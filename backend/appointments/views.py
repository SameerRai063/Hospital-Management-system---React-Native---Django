from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from appointments.models import Appointment
from appointments.serializer import AppointmentSerializer
from users.permissions import IsDoctor


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
                appointment_id=appointment_id,
                patient=request.user.patient_profile,
            )

        elif request.user.role == "doctor":

            appointment = get_object_or_404(
                Appointment,
                appointment_id=appointment_id,
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


class AppointmentCompleteAPIView(APIView):

    permission_classes = [IsAuthenticated, IsDoctor]

    def put(self, request, appointment_id):

        appointment = get_object_or_404(
            Appointment,
            appointment_id=appointment_id,
            doctor=request.user.doctor_profile,
        )

        if appointment.status == "completed":

            return Response(
                {
                    "detail": "Appointment is already completed."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        appointment.status = "completed"
        appointment.save()

        return Response(
            {
                "message": "Appointment marked as completed.",
                "appointment": AppointmentSerializer(appointment).data,
            },
            status=status.HTTP_200_OK,
        )