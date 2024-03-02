from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message
from django.core.mail import send_mail
from django.conf import settings


@receiver(post_save, sender=Message)
def send_email_about_message(sender, instance, created, **kwargs):
    if created:
        subject = "New message"
        message = f"{instance.respond_id.vacancy_id.title} answer for your respond"
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[instance.recipient.email],
            fail_silently=True,
        )
