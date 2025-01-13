from account import hooks

from django.core.mail import send_mail
from django.template.loader import render_to_string

from account.conf import settings

def custom_send_email_confirmation(to, ctx):
    print("Custom send_email_confirmation called!")
    subject = render_to_string("account/email/email_confirmation_subject.txt", ctx)
    subject = "".join(subject.splitlines())  # remove superfluous line breaks
    message = render_to_string("account/email/email_confirmation_messageHTML.html", ctx)
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, to)

# Monkey-patching
hooks.send_email_confirmation = custom_send_email_confirmation