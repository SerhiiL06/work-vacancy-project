from django.urls import path
from rest_framework.permissions import AllowAny

from . import views

urlpatterns = [
    path("", views.CompanyViewSet.as_view({"get": "list"})),
    path(
        "register/",
        views.CompanyViewSet.as_view({"post": "create"}),
    ),
    path("property-list/", views.CompanyViewSet.as_view({"get": "property_list"})),
    path(
        "<int:pk>/",
        views.CompanyViewSet.as_view({"get": "retrieve", "delete": "destroy"}),
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
        views.VerifyCompanyViewSet.as_view(
            {"get": "retrieve", "patch": "partial_update"}
        ),
    ),
]
