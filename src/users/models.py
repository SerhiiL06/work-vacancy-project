from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from .managers import CustomUserManager
from .validators import validate_phone_number


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(primary_key=True)
    phone_number = models.CharField(null=True, validators=[validate_phone_number])
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    is_active = models.BooleanField()
    is_staff = models.BooleanField()
    is_superuser = models.BooleanField()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"

    REQUIRED_FIELDS = []

    objects = CustomUserManager()
