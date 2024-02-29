from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .logic import VerificationService
from .models import User
from .serializers import (FullProfileSerializer, ProfileSerializer,
                          RegisterSerializer, UpdateProfileSerializer)


class AuthViewSet(viewsets.GenericViewSet):
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


class ProfileViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(
        methods=["get"],
        detail=False,
    )
    def users(self, request, *args, **kwargs):
        if not request.user.is_staff:

            raise PermissionDenied()

        if not cache.get("user_list"):
            serializer = FullProfileSerializer(
                instance=self.get_queryset().order_by("-join_at"), many=True
            )
            cache.set("user_list", serializer.data, 60)
        return Response({"users": cache.get("user_list")}, 200)

    @action(methods=["get"], detail=False)
    def profile(self, request, *args, **kwargs):
        serializer = ProfileSerializer(request.user, many=False)
        return Response({"current_user": serializer.data})

    @action(methods=["patch"], detail=False, url_path="profile")
    def update_profile(self, request, *args, **kwargs):
        data_to_update = UpdateProfileSerializer(data=request.data)

        data_to_update.is_valid(raise_exception=True)
        for k, v in data_to_update.validated_data.items():
            setattr(request.user, k, v)

        request.user.save()

        return Response({"update_success": data_to_update.data}, status.HTTP_200_OK)

    @action(methods=["delete"], detail=False)
    def delete_profile(self, request, *args, **kwargs):
        user_to_delete = request.data.get("user_id")
        if not request.user.is_staff:
            raise PermissionDenied()
        User.objects.get(id=user_to_delete).delete()
        return Response({"message": "user success delete"})
