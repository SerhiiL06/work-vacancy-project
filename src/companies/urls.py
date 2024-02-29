from django.urls import path

from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()

router.register("companies", views.CompanyViewSet)


urlpatterns = [
    path("property-list/", views.CompanyViewSet.as_view({"get": "property_list"})),
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


urlpatterns += router.urls
