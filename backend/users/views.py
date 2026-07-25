from django.shortcuts import render

# Create your views here.
from rest_framework.generics import CreateAPIView

from backend.users.serializer import PatientRegisterSerializer

class PatientRegisterView(CreateAPIView):
    serializer_class = PatientRegisterSerializer