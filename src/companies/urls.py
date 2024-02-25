from . import views
from rest_framework.permissions import AllowAny
from django.urls import path


urlpatterns = [
    path("register/", views.CompanyViewSet.as_view({"get": "list", "post": "create"})),
    path(
        "<int:pk>/",
        views.CompanyViewSet.as_view(
            {"get": "retrieve"}, permission_classes=[AllowAny]
        ),
    ),
    path(
        "request/",
        views.RequestCompanyViewSet.as_view({"get": "list", "post": "create"}),
    ),
    path(
        "request/verify",
        views.VerifyCompanyViewSet.as_view({"get": "list"}),
    ),
    path(
        "request/verify/<int:pk>/",
        views.VerifyCompanyViewSet.as_view({"patch": "partial_update"}),
    ),
]
