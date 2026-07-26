from django.shortcuts import render

# Create your views here.
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from backend.users.permissions import IsAdmin
from backend.users.serializer import PatientRegisterSerializer
from .models import Doctor, Patient
from .serializer import DoctorCreateSerializer, DoctorSerializer, PatientListSerializer
from .permissions import IsAdmin
#Patient Views
class PatientRegisterView(CreateAPIView):
    serializer_class = PatientRegisterSerializer

class PatientListView(ListAPIView):
    queryset = Patient.objects.select_related("user").all()
    serializer_class = PatientListSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

class PatientDetailView(RetrieveAPIView):
    queryset = Patient.objects.select_related("user")
    serializer_class = PatientListSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    lookup_field = "user__user_id"
    lookup_url_kwarg = "user_id"

#Doctor Views------------------------------------------------------------------------------------------------------
class DoctorCreateAPIView(CreateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorCreateSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

class DoctorListAPIView(ListAPIView):
    queryset = Doctor.objects.select_related("user").all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated, IsAdmin]