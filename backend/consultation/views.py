from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from consultation.models import Consultation
from consultation.serializer import ConsultationSerializer
from users.permissions import IsDoctor, IsPatient

class ConsultationListAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        consultations = Consultation.objects.all()

        serializer = ConsultationSerializer(
            consultations,
            many=True,
        )

        return Response(serializer.data)

class MyConsultationAPIView(APIView):

    permission_classes = [IsAuthenticated,IsPatient]

    def get(self, request):

        consultations = Consultation.objects.filter(
            patient=request.user.patient_profile
        )

        serializer = ConsultationSerializer(
            consultations,
            many=True,
        )

        return Response(serializer.data)

class DoctorConsultationAPIView(APIView):

    permission_classes = [IsAuthenticated, IsDoctor]

    def get(self, request):

        consultations = Consultation.objects.filter(
            doctor=request.user.doctor_profile
        )

        serializer = ConsultationSerializer(
            consultations,
            many=True,
        )

        return Response(serializer.data)

class ConsultationUpdateAPIView(APIView):

    permission_classes = [IsAuthenticated, IsDoctor]

    def put(self, request, consultation_id):

        consultation = get_object_or_404(
            Consultation,
            consultation_id=consultation_id,
            doctor=request.user.doctor_profile,
        )

        serializer = ConsultationSerializer(
            consultation,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

class ConsultationDeleteAPIView(APIView):

    permission_classes = [IsAuthenticated, IsDoctor,IsPatient]

    def delete(self, request, consultation_id):

        consultation = get_object_or_404(
            Consultation,
            consultation_id=consultation_id,
            doctor=request.user.doctor_profile,
        )

        consultation.delete()

        return Response(
            {
                "message": "Consultation deleted successfully."
            },
            status=status.HTTP_200_OK,
        )