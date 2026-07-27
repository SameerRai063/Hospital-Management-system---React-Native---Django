from django.urls import path
from .views import DeletePatientAPIView,DeleteDoctorAPIView, DoctorCreateAPIView, DoctorDetailAPIView, DoctorListAPIView, PatientDetailView, PatientListView, PatientRegisterView

urlpatterns = [
    #Patients URLS-------------------------------------------------------------------------------------------------------
    path("patients/", PatientListView.as_view(), name="patient-list"),
     path(
        "patients/<str:user_id>/",
        PatientDetailView.as_view(),
        name="patient-detail",
    ),
    path("register/", PatientRegisterView.as_view(), name="patient-register"),
    path(
        "patients/<int:id>/delete/",
        DeletePatientAPIView.as_view(),
        name="delete-patient",
    ),
    #Doctors URLS-------------------------------------------------------------------------------------------------------
    path("doctors/create/", DoctorCreateAPIView.as_view(), name="doctor-create"),
    path(
        "doctors/<int:id>/",
        DoctorDetailAPIView.as_view(),
        name="doctor-detail",
    ),
    path( "doctors/",DoctorListAPIView.as_view(),name="doctor-list"),
    path(
        "doctors/<int:id>/delete/",
        DeleteDoctorAPIView.as_view(),
        name="delete-doctor",
    ),

]