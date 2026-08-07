from django.shortcuts import get_object_or_404
from users.models import Patient
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Conversation, Message
from .serializers import (
    ConversationSerializer,
    MessageSerializer,
)
from users.models import User
class MyConversationAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        if request.user.role != "patient":
            return Response(
                {
                    "detail": "Only patients can access this endpoint."
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        patient = request.user.patient_profile

        conversation = Conversation.objects.filter(
            patient=patient
        ).first()

        if not conversation:
            return Response(
                {
                    "detail": "Conversation does not exist."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = ConversationSerializer(conversation)

        return Response(serializer.data)
class AdminConversationListAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        if request.user.role != "admin":
            return Response(
                {
                    "detail": "Only admins can access this endpoint."
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        conversations = Conversation.objects.filter(
            admin=request.user
        ).select_related(
            "patient__user"
        )

        serializer = ConversationSerializer(
            conversations,
            many=True,
        )

        return Response(serializer.data)
class ConversationCreateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        if request.user.role != "admin":
            return Response(
                {
                    "detail": "Only admins can create conversations."
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        patient_id = request.data.get("patient_id")

        if not patient_id:
            return Response(
                {
                    "detail": "patient_id is required."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        patient = get_object_or_404(
        Patient,
        id=patient_id,
)

        conversation, created = Conversation.objects.get_or_create(
            patient=patient,
            defaults={
                "admin": request.user
            }
        )

        serializer = ConversationSerializer(conversation)

        return Response(
            serializer.data,
            status=(
                status.HTTP_201_CREATED
                if created
                else status.HTTP_200_OK
            ),
        )
class ConversationMessagesAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, conversation_id):

        conversation = get_object_or_404(
            Conversation,
            id=conversation_id,
        )

        if request.user.role == "patient":

            if conversation.patient != request.user.patient_profile:
                return Response(
                    {
                        "detail": "You are not allowed to access this conversation."
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

        elif request.user.role == "admin":

            if conversation.admin != request.user:
                return Response(
                    {
                        "detail": "You are not allowed to access this conversation."
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

        else:

            return Response(
                {
                    "detail": "You are not allowed to access chat."
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        messages = conversation.messages.select_related(
            "sender"
        ).all()

        serializer = MessageSerializer(
            messages,
            many=True,
        )

        return Response(serializer.data)