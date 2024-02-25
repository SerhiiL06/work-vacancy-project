from itsdangerous import URLSafeSerializer
from datetime import datetime, timedelta
from django.conf import settings
from django.core.mail import send_mail
from .models import User


class VerificationService:
    def __init__(self):
        self.token = URLSafeSerializer(settings.SECRET_KEY, "activate")

    def send_verification_email(self, email):

        exp_time = str(datetime.now() + timedelta(days=1))
        token = self.token.dumps({"email": email, "exp": exp_time})
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

    def activate_user(self, token):
        token_data = self.token.loads(token)
        exp_time = datetime.strptime(token_data.get("exp"), "%Y-%m-%d %H:%M:%S.%f")
        if exp_time < datetime.now():
            return False

        current_user = User.objects.filter(
            email=token_data.get("email"), is_active=False
        ).first()

        if not current_user:
            return False
        current_user.is_active = True
        current_user.save()
