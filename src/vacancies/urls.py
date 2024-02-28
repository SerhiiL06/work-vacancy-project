from . import views
from django.urls import path
from rest_framework.routers import SimpleRouter


router = SimpleRouter()
router.register("jobseeker/vacansies", views.VacancyViewSet)
router.register("employeer/resumes", views.ResumeViewSet)


urlpatterns = [
    path(
        "jobseeker/vacansies/<int:pk>/respond",
        views.RespondViewSet.as_view({"post": "create"}),
    ),
    path(
        "jobseeker/vacansies/respondes/", views.RespondViewSet.as_view({"get": "list"})
    ),
]

urlpatterns += router.urls
