from django.db import models
from django.core.validators import MaxLengthValidator
from src.users.models import User
from src.users.validators import validate_phone_number
from .utils import STAFF_QUANTITY


class ScoreOfActivity(models.Model):
    title = models.CharField(unique=True)


class Country(models.Model):
    title = models.CharField(unique=True)


class Company(models.Model):

    name = models.CharField(unique=True)
    description = models.TextField(validators=[MaxLengthValidator(5000)])
    logo = models.ImageField(upload_to="company/", null=True, blank=True)
    staff = models.CharField(choices=STAFF_QUANTITY)
    verify = models.BooleanField(default=False)

    work_phone_number = models.CharField(
        validators=[validate_phone_number], null=True, blank=True
    )
    work_email = models.EmailField(unique=True)
    site_address = models.URLField(null=True, blank=True)

    activity_scope = (
        models.ForeignKey(
            ScoreOfActivity,
            on_delete=models.SET_NULL,
            null=True,
        ),
    )
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)


class VerifyRequest(models.Model):
    STATUS_CHOICE = (
        ("send", "send"),
        ("accept", "accept"),
        ("cancel", "cancel"),
    )
    company = models.OneToOneField(Company, on_delete=models.CASCADE)
    request_text = models.TextField(max_length=500)
    status = models.CharField(choices=STATUS_CHOICE, max_length=10, default="send")
    created_at = models.DateTimeField(auto_now_add=True)
