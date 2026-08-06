from rest_framework import serializers

from consultations.models import Consultation


class ConsultationSerializer(serializers.ModelSerializer):

    consultation_id = serializers.CharField(read_only=True)

    appointment_id = serializers.CharField(
        source="appointment.appointment_id",
        read_only=True,
    )

    doctor = serializers.CharField(
        source="doctor.user.get_full_name",
        read_only=True,
    )

    patient = serializers.CharField(
        source="patient.user.get_full_name",
        read_only=True,
    )

    class Meta:
        model = Consultation
        fields = [
            "consultation_id",
            "appointment_id",
            "doctor",
            "patient",
            "medicines",
            "timing",
            "notes",
        ]