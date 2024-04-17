import json

from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Send an email with a password and link to the app"  # python manage.py sendpasswords

    def handle(self, *args, **kwargs):
        with open("apps/users/fixtures/teste.json", "r") as f:
            users = json.load(f)

        for user in users:
            email = user["fields"]["email"]
            password = user["fields"]["password"]
            message = f"""
            Olá, sua senha é: {password}, use seu e-email para realizar o login.
            Acesse o app em https://gimi-requisitions.vercel.app/
            """
            send_mail(
                "Acesso ao App de Requisições Gimi",
                message,
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            self.stdout.write(self.style.SUCCESS(f"Email successfully sent to {email}"))
