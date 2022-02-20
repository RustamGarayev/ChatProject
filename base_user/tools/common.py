import string
from time import time

from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string


def get_user_profile_photo_file_name(instance, filename):
    return "profile/%s_%s" % (str(time()).replace(".", "_"), filename)


GENDER = ((1, "Kişi"), (2, "Qadın"))

PHONE_PREFIX = (
    ("+99450", "+99450"),
    ("+99451", "+99451"),
    ("+99455", "+99455"),
    ("+99470", "+99470"),
    ("+99477", "+99477"),
)


def client_code_generator(size=6, chars=string.digits):
    User = get_user_model()

    # create random tracking code
    def get_client_code():
        random_str = get_random_string(size, allowed_chars=chars)
        if not User.objects.filter(client_code=random_str).exists():
            return "66" + random_str
        else:
            return get_client_code()

    return get_client_code()


def phone_check():
    User = get_user_model()
    users = list(User.objects.all())
    print(users)
    print(len(users))

    for user in users:
        print('prefix=', user.phone_prefix, 'phone=', user.phone)
        if user.phone_prefix and len(user.phone) > 7:
            print(user.phone, 'last')
            user.phone = user.phone[-7:]
            user.save()
            print(user.phone)
        if not user.phone_prefix:
            print('PREFIX YOXDUR')
