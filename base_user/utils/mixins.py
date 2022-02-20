from django.contrib.auth import get_user_model


class MyUserMixin:
    def __set_client_code__(self):
        from django.utils.crypto import get_random_string
        from core.models import Setting
        from string import digits

        User = get_user_model()
        client_prefix = Setting.objects.first().client_prefix

        if not self.client_code:
            random_str = "{prefix}{random}".format(
                prefix=client_prefix,
                random=get_random_string(7, allowed_chars=digits),
            )

            if User.objects.filter(client_code=random_str).exists():
                self.__set_client_code__()
            else:
                self.client_code = random_str
