from django.shortcuts import render

# Create your views here.
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from backend.users.permissions import IsAdmin
from backend.users.serializer import PatientRegisterSerializer
from .models import Doctor, Patient
from .serializer import DoctorCreateSerializer, DoctorSerializer, PatientListSerializer, UpdateDoctorSerializer, UpdatePatientSerializer
from .permissions import IsAdmin,IsAdminOrDoctorOwner, IsAdminOrPatientOwner
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

class DeletePatientAPIView(DestroyAPIView):
    queryset = Patient.objects.select_related("user")
    permission_classes = [IsAdmin]
    lookup_field = "id"

    def destroy(self, request, *args, **kwargs):
        patient = self.get_object()
        patient.user.delete()  

        return Response(
            {"message": "Patient deleted successfully."},
            status=status.HTTP_200_OK
        )
class UpdatePatientAPIView(UpdateAPIView):
    queryset = Patient.objects.select_related("user")
    serializer_class = UpdatePatientSerializer
    permission_classes = [IsAuthenticated, IsAdminOrPatientOwner]
    lookup_field = "id"

#Doctor Views------------------------------------------------------------------------------------------------------
class DoctorCreateAPIView(CreateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorCreateSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

class DoctorListAPIView(ListAPIView):
    queryset = Doctor.objects.select_related("user").all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

class DoctorDetailAPIView(RetrieveAPIView):
    queryset = Doctor.objects.select_related("user").all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    lookup_field = "id"

class DeleteDoctorAPIView(DestroyAPIView):
    queryset = Doctor.objects.select_related("user")
    permission_classes = [IsAdmin]
    lookup_field = "id"

    def destroy(self, request, *args, **kwargs):
        doctor = self.get_object()
        doctor.user.delete()  # Deletes both User and Doctor (CASCADE)

        return Response(
            {"message": "Doctor deleted successfully."},
            status=status.HTTP_200_OK
        )

class UpdateDoctorAPIView(UpdateAPIView):
    queryset = Doctor.objects.select_related("user")
    serializer_class = UpdateDoctorSerializer
    permission_classes = [IsAdminOrDoctorOwner]
    lookup_field = "id"