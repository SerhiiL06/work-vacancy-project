from . import views
from django.urls import path
from rest_framework.routers import SimpleRouter


router = SimpleRouter()
router.register("vacansies/", views.VacancyViewSet)
router.register("resumes", views.ResumeViewSet)

urlpatterns = router.urls
