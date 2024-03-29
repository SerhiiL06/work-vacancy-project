from django.urls import path
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register("jobseeker/vacansies", views.VacancyViewSet)
router.register("employeer/resumes", views.ResumeViewSet)
router.register("employeer/vacansies/responds", views.EmployeerRespondViewSet)


urlpatterns = [
    path(
        "jobseeker/vacansies/<int:pk>/respond",
        views.RespondViewSet.as_view({"post": "create"}),
    ),
    path(
        "jobseeker/vacansies/respondes/", views.RespondViewSet.as_view({"get": "list"})
    ),
    path("statistic/", views.StatisticViewSet.as_view({"get": "statistic"})),
]

urlpatterns += router.urls
