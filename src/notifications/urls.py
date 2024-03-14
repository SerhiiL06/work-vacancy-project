from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()

router.register("", views.NotificationViewSet)


urlpatterns = []


urlpatterns += router.urls
