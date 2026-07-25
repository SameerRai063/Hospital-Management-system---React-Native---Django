from django.shortcuts import render

# Create your views here.
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from backend.users.permissions import IsAdmin
from backend.users.serializer import PatientRegisterSerializer
from .models import Patient
from .serializer import PatientListSerializer
from .permissions import IsAdmin

class PatientRegisterView(CreateAPIView):
    serializer_class = PatientRegisterSerializer

class PatientListView(ListAPIView):
    queryset = Patient.objects.select_related("user").all()
    serializer_class = PatientListSerializer
    permission_classes = [IsAuthenticated, IsAdmin]