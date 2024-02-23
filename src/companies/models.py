from django.db import models
from django.core.validators import MaxLengthValidator
from src.users.models import User
from src.users.validators import validate_phone_number


class ScoreOfActivity(models.Model):
    title = models.CharField(unique=True)


class Country(models.Model):
    title = models.CharField(unique=True)


class Company(models.Model):

    STAFF_QUANTITY = (
        ("1-10", "1-10"),
        ("11-50", "11-50"),
        ("51-100", "51-100"),
        ("101-1000", "101-1000"),
        ("1000+", "1000+"),
    )

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
