from django.urls import path
from .views import PaymentInitiateAPIView, PaymentVerifyAPIView,PaymentSuccessAPIView

urlpatterns = [
    path("initiate/",PaymentInitiateAPIView.as_view(),name="payment-initiate",),
    path("success/", PaymentSuccessAPIView.as_view(), name="payment-success"),
    #path("failure/", PaymentFailureAPIView.as_view(), name="payment-failure"),
    
]