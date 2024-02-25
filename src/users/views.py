from rest_framework import viewsets
from rest_framework.decorators import action
from .serializers import RegisterSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import User
from .serializers import RegisterSerializer
from .logic import VerificationService


class UserViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    verification = VerificationService()

    @action(
        methods=["post"],
        detail=False,
        url_path="register",
        serializer_class=RegisterSerializer,
        permission_classes=[permissions.AllowAny],
    )
    def register_user(self, request, *args, **kwargs):
        data = RegisterSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        result = data.save()
        self.verification.send_verification_email(result.email)
        return Response({"create": f"User id {result.id}"}, status.HTTP_201_CREATED)

    @action(
        methods=["get"],
        detail=False,
        permission_classes=[permissions.AllowAny],
    )
    def verify_email(self, request, *args, **kwargs):
        activation_process = self.verification.activate_user(kwargs.get("token"))

        if activation_process is False:
            return Response({"error": "token was expired or incorrect"}, status=400)
        return Response({"message": "user was activated"}, status=200)
