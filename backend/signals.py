from typing import Type
import json
import os

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver, Signal
from django_rest_passwordreset.signals import reset_password_token_created

from backend.models import ConfirmEmailToken, User

from backend.tasks import send_email

new_user_registered = Signal('user_id')

new_order = Signal('user_id')

def send_email(subject, message, from_email, to_email):
    msg = EmailMultiAlternatives(subject, message, from_email, [to_email])
    msg.send()


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, **kwargs):
    # """
    # Отправляем письмо с токеном для сброса пароля
    # When a token is created, an e-mail needs to be sent to the user
    # :param sender: View Class that sent the signal
    # :param instance: View Instance that sent the signal
    # :param reset_password_token: Token Model Object
    # :param kwargs:
    # :return:
    # """
    # # send an e-mail to the user

    # msg = EmailMultiAlternatives(
    #     # title:
    #     f"Password Reset Token for {reset_password_token.user}",
    #     # message:
    #     reset_password_token.key,
    #     # from:
    #     settings.EMAIL_HOST_USER,
    #     # to:
    #     [reset_password_token.user.email]
    # )
    # msg.send()
    subject = f'Токен для сброса пароля {reset_password_token.user}'
    message = reset_password_token.key
    from_email = settings.EMAIL_HOST_USER
    to_email = reset_password_token.user.email
    send_email.delay(subject, message, from_email, to_email)



@receiver(post_save, sender=User)
# def new_user_registered_signal(sender: Type[User], instance: User, created: bool, **kwargs):
    # """
    #  отправляем письмо с подтрердждением почты
    # """
    # if created and not instance.is_active:
    #     # send an e-mail to the user
    #     token, _ = ConfirmEmailToken.objects.get_or_create(user_id=instance.pk)

    #     msg = EmailMultiAlternatives(
    #         # title:
    #         f"Password Reset Token for {instance.email}",
    #         # message:
    #         token.key,
    #         # from:
    #         settings.EMAIL_HOST_USER,
    #         # to:
    #         [instance.email]
    #     )
    #     msg.send()
def new_user_registered_signal(user_id, **kwargs):
    token, _ = ConfirmEmailToken.objects.get_or_create(user_id=user_id)

    subject = f'Подтверждение регистрации {token.user.email}'
    message = token.key
    from_email = settings.EMAIL_HOST_USER
    to_email = token.user.email
    send_email.delay(subject, message, from_email, to_email)

@receiver(new_order)
def new_order_signal(user_id, **kwargs):
    # """
    # отправяем письмо при изменении статуса заказа
    # """
    # # send an e-mail to the user
    # user = User.objects.get(id=user_id)

    # msg = EmailMultiAlternatives(
    #     # title:
    #     f"Обновление статуса заказа",
    #     # message:
    #     'Заказ сформирован',
    #     # from:
    #     settings.EMAIL_HOST_USER,
    #     # to:
    #     [user.email]
    # )
    # msg.send()

    subject = f'Обновление статуса заказа'
    message = 'Заказ сформирован'
    from_email = settings.EMAIL_HOST_USER
    to_email = User.objects.get(id=user_id).email
    send_email.delay(subject, message, from_email, to_email)