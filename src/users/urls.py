from rest_framework.routers import SimpleRouter
from . import views
from django.urls import path

router = SimpleRouter()

router.register("", views.UserViewSet)


urlpatterns = [
    path("verify/<str:token>", views.UserViewSet.as_view({"get": "verify_email"})),
    path(
        "profile/",
        views.ProfileViewSet.as_view({"get": "profile", "patch": "update_profile"}),
    ),
    path("delete/<int:pk>", views.ProfileViewSet.as_view({"delete": "delete_profile"})),
]


urlpatterns += router.urls
