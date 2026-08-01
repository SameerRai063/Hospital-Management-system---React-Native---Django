from django.urls import path

from consultation import views
from .views import PaymentInitiateAPIView, PaymentVerifyAPIView

urlpatterns = [
    path(
        "initiate/",
        PaymentInitiateAPIView.as_view(),
        name="payment-initiate",
    ),
    path(
        "verify/",
        PaymentVerifyAPIView.as_view(),
        name="payment-verify",
    ),
    path("success/", views.payment_success, name="payment-success"),
]