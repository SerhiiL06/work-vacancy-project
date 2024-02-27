from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import permissions
from .models import Vacancy, Company, ScoreOfActivity, Resume
from .serializers import (
    CreateVacancySerializer,
    VacancyListSerializer,
    VacancyUpdateSerializer,
    CreateResumeSerializer,
    ListResumeSerializer,
)
from django.core.exceptions import PermissionDenied
from .permissions import VacancyPermissions, VacancyObjPermission
from rest_framework.decorators import action


class VacancyViewSet(viewsets.ModelViewSet):
    queryset = Vacancy.objects.filter(is_active=True)
    http_method_names = ["get", "post", "patch", "delete"]
    serializer_class = CreateVacancySerializer
    permission_classes = [VacancyPermissions | VacancyObjPermission]

    def create(self, request, *args, **kwargs):
        serializer = CreateVacancySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        company = serializer.validated_data.get("company")

        if company.owner != request.user:
            raise PermissionDenied("error")

        activity_scope_id = serializer.validated_data.pop("activity_scope")
        serializer.validated_data["activity_scope"] = ScoreOfActivity.objects.get(
            id=activity_scope_id
        )

        new = serializer.save()
        return Response({"ok": new.id}, 201)

    @action(methods=["get"], detail=False)
    def my(self, request, *args, **kwargs):
        query = Company.objects.raw(
            "SELECT id FROM companies_company WHERE companies_company.owner_id = %s",
            [request.user.id],
        )

        list = Vacancy.objects.filter(company__in=query)
        serializer = VacancyListSerializer(list, many=True)
        return Response({"user vacancies": serializer.data})

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return VacancyListSerializer
        if self.action == "partial_update":
            return VacancyUpdateSerializer
        return super().get_serializer_class()


class ResumeViewSet(viewsets.ModelViewSet):
    queryset = Resume.objects.filter(is_active=True)
    serializer_class = CreateResumeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.is_staff:
            raise ValidationError({"error": "admin cannot create resume"})
        serializer.save(owner=self.request.user)

    def get_serializer_class(self):
        if self.action == "create":
            return super().get_serializer_class()
        if self.action == "list":
            return ListResumeSerializer
