from django.urls import path

from appointments.views import (
    AppointmentListAPIView,
    MyAppointmentAPIView,
    DoctorAppointmentAPIView,
    AppointmentDeleteAPIView,
)

urlpatterns = [

    path(
        "",
        AppointmentListAPIView.as_view(),
        name="appointment-list",
    ),

    path(
        "my/",
        MyAppointmentAPIView.as_view(),
        name="my-appointments",
    ),

    path(
        "doctor/",
        DoctorAppointmentAPIView.as_view(),
        name="doctor-appointments",
    ),

    path(
    "delete/<str:appointment_id>/",
    AppointmentDeleteAPIView.as_view(),
    name="appointment-delete",
),


]