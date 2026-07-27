from rest_framework import serializers
from .models import Doctor, User, Patient


class PatientRegisterSerializer(serializers.ModelSerializer):
    # User fields
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = Patient
        fields = [
            # User fields
            "first_name",
            "last_name",
            "username",
            "email",
            "password",
            "phone_number",
            "profile_picture",

            # Patient fields
            "date_of_birth",
            "address",
            "emergency_contact",
        ]

    phone_number = serializers.CharField(source="user.phone_number")
    profile_picture = serializers.ImageField(
        source="user.profile_picture",
        required=False,
        allow_null=True,
    )

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")
        return value

    def create(self, validated_data):
        user_data = validated_data.pop("user")

        user = User.objects.create_user(
            username=validated_data.pop("username"),
            email=validated_data.pop("email"),
            first_name=validated_data.pop("first_name"),
            last_name=validated_data.pop("last_name"),
            password=validated_data.pop("password"),
            role="patient",
            **user_data,
        )

        patient = Patient.objects.create(
            user=user,
            **validated_data,
        )

        return patient
class PatientListSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(source="user.user_id", read_only=True)
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)
    phone_number = serializers.CharField(source="user.phone_number", read_only=True)
    profile_picture = serializers.ImageField(source="user.profile_picture", read_only=True)

    class Meta:
        model = Patient
        fields = [
            "user_id",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "profile_picture",
            "date_of_birth",
            "address",
            "emergency_contact",
        ]

#Doctor Serializer----------------------------------------------------------------------------------------------------------
class DoctorCreateSerializer(serializers.ModelSerializer):
    # User fields
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField(required=False)
    password = serializers.CharField(write_only=True, min_length=8)
    phone_number = serializers.CharField(required=False)

    class Meta:
        model = Doctor
        fields = [
            "username",
            "password",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "specialization",
            "license_number",
        ]

    def create(self, validated_data):
        password = validated_data.pop("password")

        user = User.objects.create_user(
            username=validated_data.pop("username"),
            first_name=validated_data.pop("first_name"),
            last_name=validated_data.pop("last_name"),
            email=validated_data.pop("email", ""),
            phone_number=validated_data.pop("phone_number", ""),
            role="doctor",
        )

        user.set_password(password)
        user.save()

        doctor = Doctor.objects.create(
            user=user,
            **validated_data
        )

        return doctor

class DoctorSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(source="user.user_id", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)
    phone_number = serializers.CharField(source="user.phone_number", read_only=True)
    profile_picture = serializers.ImageField(source="user.profile_picture", read_only=True)
    role = serializers.CharField(source="user.role", read_only=True)

    class Meta:
        model = Doctor
        fields = [
            "id",
            "user_id",
            "username",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "profile_picture",
            "role",
            "specialization",
            "license_number",
        ]
class UpdateDoctorSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name", required=False)
    last_name = serializers.CharField(source="user.last_name", required=False)
    email = serializers.EmailField(source="user.email", required=False)
    phone_number = serializers.CharField(source="user.phone_number", required=False)

    class Meta:
        model = Doctor
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "specialization",
            "license_number",
        ]

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", {})

        # Update User fields
        user = instance.user
        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()

        # Update Doctor fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance