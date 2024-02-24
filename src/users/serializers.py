from rest_framework import serializers
from rest_framework.validators import ValidationError
from rest_framework import status
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def create(self, validated_data):
        password1 = validated_data.pop("password1")
        password2 = validated_data.pop("password2")
        if password1 != password2:
            raise ValidationError(
                detail={"password": ["Password must be the same"]},
                code=status.HTTP_400_BAD_REQUEST,
            )
        return User.objects.create_user(**validated_data, password=password1)

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "password1", "password2"]
