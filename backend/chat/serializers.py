from rest_framework import serializers

from .models import Conversation, Message


class ConversationSerializer(serializers.ModelSerializer):

    admin_name = serializers.CharField(
        source="admin.get_full_name",
        read_only=True,
    )

    patient_name = serializers.CharField(
        source="patient.user.get_full_name",
        read_only=True,
    )

    class Meta:
        model = Conversation
        fields = [
            "id",
            "admin",
            "admin_name",
            "patient",
            "patient_name",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "admin",
            "created_at",
            "updated_at",
        ]


class MessageSerializer(serializers.ModelSerializer):

    sender_name = serializers.CharField(
        source="sender.get_full_name",
        read_only=True,
    )

    class Meta:
        model = Message
        fields = [
            "id",
            "conversation",
            "sender",
            "sender_name",
            "message",
            "created_at",
            "is_read",
        ]

        read_only_fields = [
            "sender",
            "created_at",
        ]