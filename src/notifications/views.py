from rest_framework import viewsets
from .models import Message
from adrf.viewsets import ViewSet


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    http_method_names = ["get"]
