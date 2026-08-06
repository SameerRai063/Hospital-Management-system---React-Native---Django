from rest_framework import serializers

from reviews.models import Review


class ReviewCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = [
            "doctor",
            "rating",
            "comment",
        ]
    def validate_rating(self, value):

        if value < 1 or value > 5:
            raise serializers.ValidationError(
                "Rating must be between 1 and 5."
            )

        return value


class ReviewSerializer(serializers.ModelSerializer):

    doctor = serializers.CharField(
        source="doctor.user.get_full_name",
        read_only=True,
    )

    patient = serializers.CharField(
        source="patient.user.get_full_name",
        read_only=True,
    )

    class Meta:
        model = Review
        fields = [
            "id",
            "doctor",
            "patient",
            "rating",
            "comment",
            "created_at",
        ]