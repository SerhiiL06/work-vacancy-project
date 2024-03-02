from django.db import models
from src.vacancies.models import Respond
from src.users.models import User


class Message(models.Model):
    text = models.TextField(max_length=250)

    viewed = models.BooleanField(default=False)
    respond_id = models.OneToOneField(
        Respond, on_delete=models.CASCADE, related_name="respond"
    )
    sender = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="send_messages"
    )
    recipient = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="recieve_messages"
    )
    created_at = models.DateTimeField(auto_now_add=True)
