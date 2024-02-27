from rest_framework import serializers
from .models import Vacancy

from src.companies.serializers import (
    ScoreOfActivitiesSerializer,
    ShortCompanySerializer,
)


class CreateVacancySerializer(serializers.ModelSerializer):
    activity_scope = serializers.IntegerField(required=False)

    class Meta:
        model = Vacancy
        fields = ["title", "description", "company", "activity_scope"]


class VacancyUpdateSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    is_active = serializers.BooleanField(required=False)

    class Meta:
        model = Vacancy
        fields = ["title", "description", "is_active"]


class VacancyListSerializer(serializers.ModelSerializer):
    activity_scope = ScoreOfActivitiesSerializer(many=False)
    company = ShortCompanySerializer(many=False)

    class Meta:
        model = Vacancy
        fields = ["title", "description", "created_at", "company", "activity_scope"]
