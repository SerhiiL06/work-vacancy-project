from rest_framework import serializers

from .models import Company, Country, ScoreOfActivity, VerifyRequest
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


class ShortCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["id", "name"]


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


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerifyRequest
        fields = "__all__"


class ApproveRequestSerializer(serializers.Serializer):
    RESULT_CHOICE = (("accept", "accept"), ("cancel", "cancel"))
    request_id = serializers.IntegerField()
    result = serializers.ChoiceField(RESULT_CHOICE)
