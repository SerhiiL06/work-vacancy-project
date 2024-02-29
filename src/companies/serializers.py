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
    phone = serializers.CharField(source="work_phone_number", required=False)
    email = serializers.CharField(source="work_email")
    site = serializers.CharField(source="site_address")
    staff = serializers.ChoiceField(STAFF_QUANTITY)

    class Meta:
        model = Company
        fields = [
            "name",
            "description",
            "staff",
            "phone",
            "email",
            "site",
            "activity_scope",
            "country",
        ]

    def to_representation(self, instance):
        response = {
            "company": {
                "name": instance.name,
                "description": instance.description,
                "owner": instance.owner.id,
            }
        }
        return response


class ShortCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["id", "name", "verify"]


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
