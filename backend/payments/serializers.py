from rest_framework import serializers


class PaymentInitiateSerializer(serializers.Serializer):

    doctor = serializers.IntegerField()

    appointment_date = serializers.DateTimeField()

class PaymentVerifySerializer(serializers.Serializer):
    pidx = serializers.CharField()