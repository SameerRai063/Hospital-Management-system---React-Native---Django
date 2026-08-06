from rest_framework import serializers

from appointments.models import Appointment


class AppointmentSerializer(serializers.ModelSerializer):

    doctor = serializers.CharField(
        source="doctor.user.get_full_name",
        read_only=True,
    )

    patient = serializers.CharField(
        source="patient.user.get_full_name",
        read_only=True,
    )

    class Meta:
        model = Appointment
        fields = [
            "id",
            "doctor",
            "patient",
            "appointment_date",
            "status",
            "notes",
            "created_at",
            "updated_at",
        ]