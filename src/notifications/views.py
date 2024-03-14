from django.core.exceptions import PermissionDenied
from rest_framework import permissions, viewsets

from .models import Message
from .serializers import MessagesSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessagesSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get"]

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.recipient != request.user:
            raise PermissionDenied()
        return self.partial_update(request, viewed=True)

    def get_queryset(self):
        return Message.objects.filter(recipient=self.request.user)
