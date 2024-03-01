from django.db import models
from src.vacancies.models import Respond


class Message(models.Model):
    text = models.TextField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    viewed = models.BooleanField(default=False)
    respond_id = models.ForeignKey(
        Respond, on_delete=models.CASCADE, related_name="respond"
    )
