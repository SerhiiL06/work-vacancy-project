from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework import status
from .models import Company, Country, ScoreOfActivity, VerifyRequest
from .serializers import (
    CreateCompanySerializer,
    ListOfCountriesSerializer,
    ScoreOfActivitiesSerializer,
    RetrieveCompanySerializer,
    ShortCompanySerializer,
    RequestSerializer,
    ApproveRequestSerializer,
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


class RequestCompanyViewSet(ModelViewSet):
    queryset = VerifyRequest.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        query = Company.objects.filter(owner=request.user)

        serializer = ShortCompanySerializer(query, many=True)

        return Response({"list": serializer.data})

    def create(self, request, *args, **kwargs):
        data = RequestSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        company = data.validated_data.get("company")
        if company.owner != request.user:
            return Response(
                {"message": "u don't permission for this"}, status.HTTP_400_BAD_REQUEST
            )
        check_request = VerifyRequest.objects.filter(company=company.id)

        if check_request.first():
            return Response({"error": "u cannot send more than one request"})

        new_request = data.save()
        return Response({"request": new_request.id}, status.HTTP_201_CREATED)


class VerifyCompanyViewSet(ModelViewSet):
    queryset = VerifyRequest.objects.filter(status="send")
    http_method_names = ["get", "post", "patch"]
    permission_classes = [permissions.IsAdminUser]
    serializer_class = RequestSerializer

    def partial_update(self, request, *args, **kwargs):
        data = ApproveRequestSerializer(data=request.data)

        data.is_valid(raise_exception=True)

        verification_request = get_object_or_404(
            VerifyRequest, id=data.validated_data.get("request_id")
        )
        if verification_request.status != "send":
            return Response(
                {"error": "u cannot to approve the close request"},
                status.HTTP_400_BAD_REQUEST,
            )

        if data.validated_data.get("result") == "cancel":
            verification_request.status = "cancel"
            verification_request.save()
            return Response(
                {"message": "request is correct cancel"}, status.HTTP_202_ACCEPTED
            )

        company = Company.objects.get(id=verification_request.company.id)
        company.verify = True
        company.save()
        verification_request.status = "accept"
        verification_request.save()

        return Response({"message": "accept complete"}, status.HTTP_200_OK)
