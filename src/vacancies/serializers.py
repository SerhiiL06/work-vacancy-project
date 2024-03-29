import math

from rest_framework import serializers

from src.companies.serializers import (ScoreOfActivitiesSerializer,
                                       ShortCompanySerializer)
from src.users.serializers import UserInlineSerializer

from .models import Respond, Resume, Vacancy


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


class VacancyShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacancy
        fields = ["id", "title", "description", "calary"]


class ListResumeSerializer(serializers.ModelSerializer):
    owner = UserInlineSerializer(many=False)

    class Meta:
        model = Resume
        fields = ["id", "title", "owner"]


class InlineResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ["id", "title"]


class CreateResumeSerializer(serializers.ModelSerializer):
    owner = serializers.IntegerField(required=False, write_only=True)

    def create(self, validated_data):
        return super().create(validated_data)

    class Meta:
        model = Resume
        fields = "__all__"


class RetrieveResumeSerializer(serializers.ModelSerializer):
    owner = UserInlineSerializer(many=False)
    format_work = serializers.CharField(required=False)

    class Meta:
        model = Resume
        fields = ["id", "title", "description", "calary", "format_work", "owner"]


class CreateRespondSerializer(serializers.Serializer):
    resume_id = serializers.IntegerField()


class RespondSerializer(serializers.ModelSerializer):
    vacancy_id = VacancyShortSerializer(many=False)
    resume_id = InlineResumeSerializer(many=False)

    class Meta:
        model = Respond
        fields = ["id", "viewed", "vacancy_id", "resume_id"]


class RetrieveRespondSerializer(serializers.ModelSerializer):
    vacancy_title = serializers.SerializerMethodField(source="vacancy_id")

    class Meta:
        model = Respond
        fields = ["id", "viewed", "vacancy_title"]

    def get_vacancy_title(self, obj):
        return obj.vacancy_id.title

    def to_representation(self, instance):
        resume = Resume.objects.get(id=instance.resume_id.id)

        representation = super().to_representation(instance)

        representation["resume"] = ListResumeSerializer(resume, many=False).data
        return representation


class VacancyCountSerializer(serializers.Serializer):
    title = serializers.CharField()
    activity_count = serializers.IntegerField()


class ByCategorySerializer(serializers.Serializer):
    title = serializers.CharField()
    avg_calary = serializers.IntegerField()


class StatisticSerializer(serializers.Serializer):
    avg_calary = serializers.IntegerField()
    category = ByCategorySerializer(many=True)
