from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .models import Company, Respond, Resume, ScoreOfActivity, Vacancy
from .permissions import VacancyObjPermission, VacancyPermissions
from .serializers import (CreateRespondSerializer, CreateResumeSerializer,
                          CreateVacancySerializer, ListResumeSerializer,
                          RespondSerializer, VacancyListSerializer,
                          VacancyUpdateSerializer)


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
    permission_classes = [permissions.AllowAny]

    @action(
        methods=["get"],
        detail=False,
        url_path="my",
        permission_classes=[permissions.IsAuthenticated()],
    )
    def my_resumes(self, request, *args, **kwargs):
        query = Resume.objects.filter(owner=request.user)

        serializer = ListResumeSerializer(query, many=True)
        return Response({"resumes": serializer.data}, 200)

    def perform_create(self, serializer):
        if self.request.user.is_staff:
            raise ValidationError({"error": "admin cannot create resume"})
        serializer.save(owner=self.request.user)

    def get_serializer_class(self):
        if self.action == "create":
            return super().get_serializer_class()
        if self.action == "list":
            return ListResumeSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return super().get_permissions()
        return [permissions.IsAuthenticated()]


class RespondViewSet(viewsets.ModelViewSet):
    queryset = Respond.objects.all()
    serializer_class = RespondSerializer
    http_method_names = ["get", "post"]

    def create(self, request, *args, **kwargs):
        data = CreateRespondSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        respond_check = Respond.objects.filter(
            resume_id=data.validated_data.get("resume_id"),
            vacancy_id=kwargs.get("pk"),
            viewed=False,
        )

        if respond_check.first():
            return Response({"error": "u can send maximum one respond"})

        current_vacancy = get_object_or_404(Vacancy, id=kwargs.get("pk"))
        current_resume = get_object_or_404(
            Resume, id=data.validated_data.get("resume_id")
        )
        if current_resume.owner != request.user:
            raise PermissionDenied()
        Respond.objects.create(
            resume_id=current_resume,
            vacancy_id=current_vacancy,
        )
        return Response({"message": "respond was sent"}, 204)

    def get_queryset(self):
        if self.action == "list":
            return Respond.objects.filter(
                resume_id__owner=self.request.user
            ).prefetch_related("resume_id")
        return super().get_queryset()
