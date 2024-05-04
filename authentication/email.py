from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def activation_email(uid, token, email, username):
    subject = "Verify Your Email Address - Action Required"
    html_body = render_to_string("activation.html", {
        'username': username,
        'company_name': settings.SITE_NAME,
        'host_email': settings.EMAIL_HOST_USER,
        'uid': uid,
        'token': token,
    })

    msg = EmailMultiAlternatives(
        subject=subject, from_email=settings.EMAIL_HOST_USER, to=[email])
    msg.attach_alternative(html_body, "text/html")
    msg.send()


def reset_password_confirmation(uid, token, email, username):
    subject = "Reset Password Confirmation - Action Required"
    html_body = render_to_string("reset_password_confirmation.html", {
        'username': username,
        'company_name': settings.SITE_NAME,
        'host_email': settings.EMAIL_HOST_USER,
        'uid': uid,
        'token': token,
    })

    msg = EmailMultiAlternatives(
        subject=subject, from_email=settings.EMAIL_HOST_USER, to=[email])
    msg.attach_alternative(html_body, "text/html")
    msg.send()


def reset_email_confirmation(uid, token, email, username):
    subject = "Reset Email Confirmation - Action Required"
    html_body = render_to_string("reset_email_confirmation.html", {
        'username': username,
        'company_name': settings.SITE_NAME,
        'host_email': settings.EMAIL_HOST_USER,
        'uid': uid,
        'token': token,
    })

    msg = EmailMultiAlternatives(
        subject=subject, from_email=settings.EMAIL_HOST_USER, to=[email])
    msg.attach_alternative(html_body, "text/html")
    msg.send()
