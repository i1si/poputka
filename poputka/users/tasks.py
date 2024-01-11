from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_email(subject: str, text: str, recipient_list: list[str]):
    send_mail(subject, text, None, recipient_list)
