from django.urls import path
from .views import MyPaymentAPIView, PaymentDeleteAPIView, PaymentInitiateAPIView, PaymentListAPIView,PaymentSuccessAPIView

urlpatterns = [
    path("initiate/",PaymentInitiateAPIView.as_view(),name="payment-initiate",),
    path("success/", PaymentSuccessAPIView.as_view(), name="payment-success"),
    #path("failure/", PaymentFailureAPIView.as_view(), name="payment-failure"),
     path("",PaymentListAPIView.as_view(),name="payment-list",),
    path("my/",MyPaymentAPIView.as_view(),name="my-payments" ),
    path("delete/<str:transaction_id>/",PaymentDeleteAPIView.as_view(),name="payment-delete",),
    
]