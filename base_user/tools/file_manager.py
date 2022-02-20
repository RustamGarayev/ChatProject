import os
from django.urls import reverse
from django.http import QueryDict
from django.core.exceptions import ValidationError
from django.utils import timezone
from time import time
from django.conf import settings


def reverse_with_params(*args, **kwargs):
    params = kwargs.pop("params", {})
    url = reverse(*args, **kwargs)
    if not params:
        return url

    qdict = QueryDict("", mutable=True)
    for k, v in params.items():
        if type(v) is list:
            qdict.setlist(k, v)
        else:
            qdict[k] = v

    return url + "?" + qdict.urlencode()


def get_attachment_path(instance, filename):
    """
    :param instance:
    :param filename:
    :return:
    """
    return "mails/{date}/{random}_{filename}".format(
        random=str(time()).replace(".", "_"),
        filename=filename,
        date=timezone.now().date().strftime("%Y/%m/%d"),
    )


def get_signature_path(instance, filename):
    return "users/%d/signatures/%s" % (instance.user.id, filename)


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = [
        ".xls",
    ]
    if not ext.lower() in valid_extensions:
        raise ValidationError(
            u"Unsupported file extension. Only supported file types are: "
            + ", ".join(valid_extensions)
        )


def get_domain_with_protocol(for_static=False):
    try:
        DEVELOPMENT = settings.DEBUG
        PROD = settings.PROD
    except AttributeError:
        DEVELOPMENT = False

    from core.models import Setting

    s = Setting.objects.last()
    domain = "bringly.az"
    if s:
        domain = s.site.domain

    protocol = "http" if DEVELOPMENT else "https"

    return "%s://%s" % (protocol, domain)
