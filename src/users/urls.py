from django.urls import path
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()

router.register("", views.AuthViewSet)


urlpatterns = [
    path(
        "users/verify/<str:token>", views.AuthViewSet.as_view({"get": "verify_email"})
    ),
    path("admin/users", views.ProfileViewSet.as_view({"get": "users"})),
    path(
        "users/profile/",
        views.ProfileViewSet.as_view(
            {"get": "profile", "patch": "update_profile", "delete": "delete_profile"}
        ),
    ),
]


urlpatterns += router.urls
