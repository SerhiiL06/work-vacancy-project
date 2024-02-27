from django.db import models
from src.companies.models import Company, ScoreOfActivity
from src.users.models import User
from .validators import calary_validator


class Vacancy(models.Model):
    FORMAT_OR_WORK = (("remote", "remote"), ("hybrid", "hubrid"), ("office", "office"))
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    format_work = models.CharField(choices=FORMAT_OR_WORK, default="office")
    calary = models.CharField(
        validators=[calary_validator], null=True, blank=True, default="0"
    )
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    activity_scope = models.ForeignKey(ScoreOfActivity, on_delete=models.CASCADE)


class Resume(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    activity_scope = models.ForeignKey(
        ScoreOfActivity, on_delete=models.SET_NULL, null=True
    )


class Respond(models.Model):
    resume_id = models.ForeignKey(Resume, on_delete=models.CASCADE)
    vacancy_id = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    viewed = models.BooleanField(default=False)
