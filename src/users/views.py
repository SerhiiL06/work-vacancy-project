from rest_framework import viewsets
from rest_framework.decorators import action
from .serializers import RegisterSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import User
from .serializers import RegisterSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

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
        print(result)
        return Response({"create": f"User id {result.id}"}, status.HTTP_201_CREATED)
