from rest_framework import serializers
from .models import UserProfile
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    """Serializer for creating and managing users."""

    class Meta:
        model = UserProfile
        fields = (
            "id",
            "user_id",
            "username",
            "kana_name",
            "company",
            "role",
            "label",
            "group",
            "email",
            "password",
            "qrcode",
        )
        extra_kwargs = {
            "password": {"write_only": True},
            "qrcode": {"read_only": True},
        }

    def create(self, validated_data):
        """Create a new user with encrypted password."""
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """Update a user, ensuring password is encrypted if changed."""
        if "password" in validated_data:
            validated_data["password"] = make_password(validated_data["password"])
        return super().update(instance, validated_data)


class UserLoginSerializer(serializers.Serializer):
    """Serializer for user login."""

    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)
