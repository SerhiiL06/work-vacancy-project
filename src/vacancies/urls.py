from . import views
from django.urls import path
from rest_framework.routers import SimpleRouter


router = SimpleRouter()
router.register("", views.VacancyViewSet)

urlpatterns = router.urls
