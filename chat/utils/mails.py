from django.core.mail import EmailMessage, get_connection
from django.conf import settings
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import HttpResponseRedirect



def send_email(request, recipient, username, password, template):
    with get_connection(
        host=settings.EMAIL_HOST,
        post=settings.EMAIL_PORT,
        username=settings.EMAIL_HOST_USER,
        password=settings.EMAIL_HOST_PASSWORD,
        user_tls=settings.EMAIL_USE_TLS
    ) as connection:
        subject = 'Activate your account'
        email_from = settings.EMAIL_HOST_USER
        # recipeint_list = [recipient]
        recipeint_list = ['just.box91@mail.ru']
        message = template
        
        emessage = EmailMessage(subject, message, email_from, recipeint_list,
                     connection=connection)
        emessage.send()
        messages.add_message(request, messages.SUCCESS, 'Email sent')