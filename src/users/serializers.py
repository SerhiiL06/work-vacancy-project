from datetime import datetime

from django.utils.timesince import timesince
from rest_framework import serializers, status
from rest_framework.validators import ValidationError

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


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "birthday"]


class FullProfileSerializer(ProfileSerializer):
    class Meta(ProfileSerializer.Meta):
        fields = ProfileSerializer.Meta.fields + ["is_active", "join_at", "last_login"]


class UserInlineSerializer(serializers.ModelSerializer):
    birthday = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["first_name", "last_name", "birthday"]

    def get_birthday(self, obj):
        if not obj.birthday:
            return None

        return timesince(obj.birthday)


class UpdateProfileSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    birthday = serializers.DateField(required=False)
