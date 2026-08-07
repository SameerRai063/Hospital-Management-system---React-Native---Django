from rest_framework import serializers

from backend.payments.models import Payment


class PaymentInitiateSerializer(serializers.Serializer):

    doctor = serializers.IntegerField()

    appointment_date = serializers.DateTimeField()

class PaymentVerifySerializer(serializers.Serializer):
    transaction_uuid = serializers.CharField()
class PaymentSerializer(serializers.ModelSerializer):

    appointment_id = serializers.CharField(
        source="appointment.appointment_id",
        read_only=True,
    )

    patient = serializers.CharField(
        source="appointment.patient.user.get_full_name",
        read_only=True,
    )

    doctor = serializers.CharField(
        source="appointment.doctor.user.get_full_name",
        read_only=True,
    )

    class Meta:
        model = Payment
        fields = [
            "transaction_id",
            "appointment_id",
            "patient",
            "doctor",
            "gateway",
            "amount",
            "paid_at",
        ]