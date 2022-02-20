import requests
from django.db.models.signals import post_save
from django.dispatch import receiver
from base_user.tools.file_manager import get_domain_with_protocol
from django.contrib.auth import get_user_model
from .models import UserActivation

from django_rest_passwordreset.signals import reset_password_token_created

User = get_user_model()


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    protocol_and_domain = get_domain_with_protocol()
    link = f"{protocol_and_domain}/az/account/forget/"
    client = requests.session()
    client.get(link)
    csrftoken = client.cookies['csrftoken']
    data = dict(email=reset_password_token.user.email, csrfmiddlewaretoken=csrftoken, next='/')
    req = client.post(link, data=data, headers=dict(Referer=link))
    return req

