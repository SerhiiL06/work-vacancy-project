from django.urls import path
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()

router.register("", views.AuthViewSet)


urlpatterns = [
    path("verify/<str:token>", views.AuthViewSet.as_view({"get": "verify_email"})),
    path("admin/all", views.ProfileViewSet.as_view({"get": "users"})),
    path(
        "profile/",
        views.ProfileViewSet.as_view({"get": "profile", "patch": "update_profile"}),
    ),
    path("delete/<int:pk>", views.ProfileViewSet.as_view({"delete": "delete_profile"})),
]


urlpatterns += router.urls
