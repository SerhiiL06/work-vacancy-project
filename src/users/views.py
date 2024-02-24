from rest_framework import viewsets
from rest_framework.decorators import action
from .serializers import RegisterSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import User
from .serializers import RegisterSerializer
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from itsdangerous import URLSafeSerializer
from datetime import datetime, timedelta


class UserViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    # serializer_class = RegisterSerializer

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
        self._send_verification_email(result.email)
        return Response({"create": f"User id {result.id}"}, status.HTTP_201_CREATED)

    @action(
        methods=["get"],
        detail=False,
        # url_path="verify/<str:token>",
        # url_name="verify",
        permission_classes=[permissions.AllowAny],
    )
    def verify_email(self, request, token, *args, **kwargs):
        return Response({"hello": "man"})

    @classmethod
    def _send_verification_email(cls, email):
        gen_token = URLSafeSerializer(settings.SECRET_KEY, "activate")
        exp_time = str(datetime.now() + timedelta(days=1))
        token = gen_token.dumps({"email": email, "exp": exp_time})
        link = f"http://127.0.0.1:8000/users/verify/{token}"
        subject = "Hello from out site!"
        message = f"If you're register in our site please click link for verification your email address {link}"
        send_mail(
            subject,
            message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=True,
        )
