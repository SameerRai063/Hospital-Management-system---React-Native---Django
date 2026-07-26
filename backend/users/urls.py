from django.urls import path
from .views import PatientDetailView, PatientListView

urlpatterns = [
    path("patients/", PatientListView.as_view(), name="patient-list"),
     path(
        "patients/<str:user_id>/",
        PatientDetailView.as_view(),
        name="patient-detail",
    ),
    
]