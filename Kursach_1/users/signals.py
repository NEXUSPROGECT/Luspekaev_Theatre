from django.core.mail import send_mail
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

@receiver(user_logged_in)
def send_welcome_email(sender, request, user, **kwargs):
    print("send_welcome_email")
    # Отправляем письмо после входа пользователя
    subject = _('Добро пожаловать!')
    message = _('Здравствуйте, {}! Вы успешно вошли в свой аккаунт.'.format(user.username))
    recipient_list = [user.email]

    send_mail(subject, message, None, recipient_list)