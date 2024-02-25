from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework import status
from .models import Company, Country, ScoreOfActivity
from .serializers import (
    CreateCompanySerializer,
    ListOfCountriesSerializer,
    ScoreOfActivitiesSerializer,
    RetrieveCompanySerializer,
)


class CompanyViewSet(ModelViewSet):
    queryset = Company.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CreateCompanySerializer

    def list(self, request):
        countries = Country.objects.all()
        activities = ScoreOfActivity.objects.all()
        list_country = ListOfCountriesSerializer(countries, many=True)
        list_of_activities = ScoreOfActivitiesSerializer(activities, many=True)

        context_response = {
            "countries": list_country.data,
            "activities": list_of_activities.data,
        }
        return Response(context_response, status.HTTP_200_OK)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return super().get_serializer_class()
        if self.action == "retrieve":
            return RetrieveCompanySerializer
