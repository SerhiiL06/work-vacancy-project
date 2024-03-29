from adrf.viewsets import ViewSet
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets
from rest_framework.authentication import (BasicAuthentication,
                                           SessionAuthentication)
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from src.notifications.models import Message

from .logic import check_respond_permission, generate_statistic
from .models import Company, Respond, Resume, ScoreOfActivity, Vacancy
from .permissions import VacancyObjPermission, VacancyPermissions
from .serializers import (CreateRespondSerializer, CreateResumeSerializer,
                          CreateVacancySerializer, ListResumeSerializer,
                          RespondSerializer, RetrieveRespondSerializer,
                          RetrieveResumeSerializer, VacancyCountSerializer,
                          VacancyListSerializer, VacancyShortSerializer,
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

    def list(self, request, *args, **kwargs):
        if not cache.get("vacancies"):
            response = super().list(request, *args, **kwargs)
            cache.set("vacancies", response.data, 60)
            return response
        return Response(cache.get("vacancies"))

    def retrieve(self, request, *args, **kwargs):
        obj = Vacancy.objects.get(id=kwargs.get("pk"))
        serialzier = VacancyListSerializer(obj, many=False)
        context = {"vacancy": serialzier.data}
        if request.user.is_authenticated:
            check = Respond.objects.filter(
                vacancy_id=obj.id, resume_id__owner=request.user
            )
            last_sended = check.first().created_at.date() if check.first() else None
            context["last_sended"] = last_sended
        return Response(context, 200)

    @action(
        methods=["get"],
        detail=False,
        url_path="my",
        permission_classes=[permissions.IsAuthenticated],
    )
    def user_vacancies(self, request, *args, **kwargs):
        query = Company.objects.raw(
            "SELECT id FROM companies_company WHERE companies_company.owner_id = %s",
            [request.user.id],
        )

        list = Vacancy.objects.filter(company__in=query)
        serializer = VacancyListSerializer(list, many=True)
        return Response({"user vacancies": serializer.data})

    @action(methods=["get"], detail=False, url_path="by-category")
    def vacancies_by_category(self, request, *args, **kwargs):

        if not cache.get("vacancy_count"):
            query = Vacancy.objects.raw(
                """ SELECT 1 as id, companies_scoreofactivity.title, 
                    COUNT(*) as activity_count FROM vacancies_vacancy
                    JOIN companies_scoreofactivity ON companies_scoreofactivity.id=vacancies_vacancy.activity_scope_id
                    GROUP BY vacancies_vacancy.activity_scope_id, companies_scoreofactivity.title
                    ORDER BY activity_count DESC
                    """
            )
            serializer = VacancyCountSerializer(query, many=True)
            cache.set("vacancy_count", serializer.data, 3600)
            return Response({"vacancies": serializer.data})
        return Response({"vacancies": cache.get("vacancy_count")})

    def get_serializer_class(self):
        if self.action in "list":
            return VacancyShortSerializer
        if self.action == "retrieve":
            return VacancyListSerializer
        if self.action == "partial_update":
            return VacancyUpdateSerializer
        return super().get_serializer_class()


class ResumeViewSet(viewsets.ModelViewSet):
    queryset = Resume.objects.filter(is_active=True).prefetch_related("owner")
    serializer_class = RetrieveResumeSerializer
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

    def retrieve(self, request, *args, **kwargs):
        key = request.session.session_key
        cache_key = f"resume:'{kwargs.get('pk')}:{key}"
        if not cache.get(cache_key):
            obj = self.get_object()
            serializer = RetrieveResumeSerializer(instance=obj, many=False)
            cache.set(cache_key, serializer.data, 180)
            return Response(serializer.data, 200)

        return Response(data=cache.get(cache_key), status=200)

    def get_serializer_class(self):
        if self.action == "list":
            return ListResumeSerializer
        if self.action == "create":
            return CreateResumeSerializer
        if self.action == "retrieve":
            return super().get_serializer_class()

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return super().get_permissions()
        return [permissions.IsAuthenticated()]


class RespondViewSet(viewsets.ModelViewSet):
    queryset = Respond.objects.all()
    serializer_class = RespondSerializer
    permission_classes = [permissions.IsAuthenticated]
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
        if (
            current_resume.owner != request.user
            or current_vacancy.company.owner == request.user
        ):
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


class EmployeerRespondViewSet(viewsets.ModelViewSet):
    queryset = Respond.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "post"]
    serializer_class = RespondSerializer

    def retrieve(self, request, *args, **kwargs):
        check_respond_permission(request.user, kwargs.get("pk"))
        obj = Respond.objects.get(id=kwargs.get("pk"))
        serializer = RetrieveRespondSerializer(obj, many=False)
        obj.viewed = True
        obj.save()
        return Response({"respond": serializer.data})

    @action(methods=["post"], detail=True, url_path="answer", url_name="answer")
    def answer_to_respond(self, request, *args, **kwargs):
        answer = request.data.get("answer")

        error_block = {}

        if answer is None or len(answer) < 5:
            return error_block.update({"error": "incorrect answer"})
        respond = Respond.objects.get(id=kwargs.get("pk"))
        vacancy = Vacancy.objects.get(id=respond.vacancy_id.id)
        resume = Resume.objects.get(id=respond.resume_id.id)
        if vacancy.company.owner != request.user:
            raise PermissionDenied()

        get, new_message = Message.objects.get_or_create(
            text=answer,
            respond_id=respond,
            sender=request.user,
            recipient=resume.owner,
        )
        if new_message:
            return Response({"message": get.id})
        return Response({"erorr": "message to this respond already exists"})

    def get_queryset(self):
        ids = Vacancy.objects.filter(company__owner=self.request.user)
        return Respond.objects.filter(vacancy_id__in=ids)


class StatisticViewSet(viewsets.GenericViewSet):
    queryset = Vacancy.objects.filter(is_active=True)

    @action(methods=["get"], detail=False)
    def statistic(self, request, *args, **kwargs):
        if not cache.get("statistic"):
            statictic = generate_statistic()
            cache.set("statistic", statictic, 86400)
            return Response({"avg_calary": statictic})
        return Response({"avg_calary": cache.get("statistic")})
