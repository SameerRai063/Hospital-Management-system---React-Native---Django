from django.urls import path

from reviews.views import (
    ReviewCreateAPIView,
    ReviewDeleteAPIView,
    ReviewListAPIView,
    MyReviewAPIView,
    DoctorReviewAPIView,
)

urlpatterns = [

    path(
        "create/",
        ReviewCreateAPIView.as_view(),
        name="review-create",
    ),

    path(
        "",
        ReviewListAPIView.as_view(),
        name="review-list",
    ),

    path(
        "my/",
        MyReviewAPIView.as_view(),
        name="my-reviews",
    ),

    path(
        "doctor/",
        DoctorReviewAPIView.as_view(),
        name="doctor-reviews",
    ),

    path(
        "delete/<int:review_id>/",
        ReviewDeleteAPIView.as_view(),
        name="review-delete",
    ),
]