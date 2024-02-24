from rest_framework.routers import SimpleRouter
from . import views
from django.urls import path

router = SimpleRouter()

router.register("", views.UserViewSet)


urlpatterns = [
    path("verify/<str:token>", views.UserViewSet.as_view({"get": "verify_email"}))
]


urlpatterns += router.urls
