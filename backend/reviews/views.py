from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Review
from .serializer import (
    ReviewCreateSerializer,
    ReviewSerializer,
)
from users.models import Doctor


class ReviewCreateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = ReviewCreateSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        doctor = get_object_or_404(
            Doctor,
            id=serializer.validated_data["doctor"].id,
        )

        patient = request.user.patient_profile

        review = Review.objects.create(
            doctor=doctor,
            patient=patient,
            rating=serializer.validated_data["rating"],
            comment=serializer.validated_data["comment"],
        )

        return Response(
            ReviewSerializer(review).data,
            status=status.HTTP_201_CREATED,
        )
class ReviewListAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        reviews = Review.objects.all()

        serializer = ReviewSerializer(
            reviews,
            many=True,
        )

        return Response(serializer.data)
class MyReviewAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        patient = request.user.patient_profile

        reviews = Review.objects.filter(
            patient=patient
        )

        serializer = ReviewSerializer(
            reviews,
            many=True,
        )

        return Response(serializer.data)
class ReviewDeleteAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request, review_id):

        patient = request.user.patient_profile

        review = get_object_or_404(
            Review,
            id=review_id,
            patient=patient,
        )

        review.delete()

        return Response(
            {
                "message": "Review deleted successfully."
            },
            status=status.HTTP_200_OK,
        )
class DoctorReviewAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        doctor = request.user.doctor_profile

        reviews = Review.objects.filter(
            doctor=doctor
        )

        serializer = ReviewSerializer(
            reviews,
            many=True,
        )

        return Response(serializer.data)