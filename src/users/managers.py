from typing import Any
from django.contrib.auth.models import UserManager


class CustomUserManager(UserManager):
    def _create_user(self, email: str, password: str, **extra_fields):
        if not email:
            raise ValueError("Email is required field")

        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(
        self, email: str | None, password: str | None, **extra_fields: Any
    ) -> Any:
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self._create_user(email, password, extra_fields)

    def create_user(self, email: str | None, password: str | None, **extra_fields: Any):
        extra_fields.setdefault("is_active", False)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        return self._create_user(email, password, extra_fields)
