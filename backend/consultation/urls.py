from django.urls import path

from consultation.views import (
    ConsultationListAPIView,
    MyConsultationAPIView,
    DoctorConsultationAPIView,
    ConsultationUpdateAPIView,
    ConsultationDeleteAPIView,
)

urlpatterns = [

    path(
        "",
        ConsultationListAPIView.as_view(),
        name="consultation-list",
    ),

    path(
        "my/",
        MyConsultationAPIView.as_view(),
        name="my-consultations",
    ),

    path(
        "doctor/",
        DoctorConsultationAPIView.as_view(),
        name="doctor-consultations",
    ),

    path(
        "update/<str:consultation_id>/",
        ConsultationUpdateAPIView.as_view(),
        name="consultation-update",
    ),

    path(
        "delete/<str:consultation_id>/",
        ConsultationDeleteAPIView.as_view(),
        name="consultation-delete",
    ),
]