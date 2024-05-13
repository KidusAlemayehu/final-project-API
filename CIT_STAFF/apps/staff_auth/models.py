from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from .email_templates import EmailTemplates
from django.conf import settings

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    password_url = "http://localhost:3000/forgot-password-confirm/"
    reset_link= "{}?token={}".format(password_url,reset_password_token.key)
    email_plaintext_message = EmailTemplates.PASSWORD_RESET_EMAIL_MESSAGE_TEXT.format(reset_password_token.user.first_name, reset_link, "CIT Staff Management System IT Team")    
    print(email_plaintext_message)
    send_mail(
        EmailTemplates.PASSWORD_RESET_EMAIL_SUBJECT_TEXT.format("CIT Staff Management"),
        email_plaintext_message,
        settings.DEFAULT_FROM_EMAIL,
        [reset_password_token.user.email]
    )