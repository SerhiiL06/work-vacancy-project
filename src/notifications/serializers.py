from rest_framework import serializers
from .models import Message
from src.vacancies.models import Vacancy
from src.vacancies.serializers import VacancyShortSerializer


class MessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["id", "text", "viewed"]

    def to_representation(self, instance):
        vacancy = Vacancy.objects.get(id=instance.respond_id.vacancy_id.id)

        representation = super().to_representation(instance)

        representation["vacancy"] = VacancyShortSerializer(vacancy, many=False).data

        return representation
