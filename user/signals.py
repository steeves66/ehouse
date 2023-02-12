
from django.db.models.signals import post_save
from django.dispatch import receiver
from django import dispatch

from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from .models import User

from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site

from django.http import HttpResponseRedirect



#from django.contrib.auth import get_user_model
#User = get_user_model()


user_password_reset_email = dispatch.Signal(['user', 'request'])

@receiver(user_password_reset_email)
def my_code_done(sender, user, request, **kwargs):
    print(user.full_name(), request.POST["email"], "send email -------------------------------------------")
    # Reset password email
    current_site = get_current_site(request)
    mail_subject = 'Reset Your Password'
    message = render_to_string('user/email/reset_password_email.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user)
    })
    to_email = user.email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()
    print('Password Reset Email sended-------------------------------------------------------------------')


@receiver(post_save, sender=User)
def send_confirm_register_email(sender, instance, created, **kwargs):
    if created:
        request = instance.request
        current_site = get_current_site(request)
        mail_subject = 'Please activate your account' 
        context = {
            'user': instance,
            'domain': current_site,                
            'uid': urlsafe_base64_encode(force_bytes(instance.pk)),
            'token': default_token_generator.make_token(instance)
        }
        message = render_to_string('user/email/confirm_register_email.html', context)
        to_email = instance.email
        send_email = EmailMessage(mail_subject, message, to=[to_email]) 
        send_email.send()
        print('Email sended-------------------------------------------------------------------')