from rest_framework import serializers
from .models import Company, Country, ScoreOfActivity
from .utils import STAFF_QUANTITY


class ListOfCountriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ["id", "title"]


class ScoreOfActivitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScoreOfActivity
        fields = ["id", "title"]


class CreateCompanySerializer(serializers.ModelSerializer):
    staff = serializers.ChoiceField(STAFF_QUANTITY)

    class Meta:
        model = Company
        exclude = ["owner"]


class RetrieveCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = [
            "name",
            "description",
            "logo",
            "work_email",
            "work_phone_number",
            "country",
        ]
