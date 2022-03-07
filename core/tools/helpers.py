from time import time
import pycountry
from unidecode import unidecode

COUNTRIES = [(x.alpha_2, x.name) for x in pycountry.countries]


def get_group_icon(instance, filename):
    if "." in filename:
        return "group/icon/%s_%s" % (
            str(time()).replace(".", "_"),
            unidecode(filename.rsplit(".", 1)[0])
            + ".{}".format(filename.rsplit(".", 1)[1]),
        )
    else:
        return "group/icon/%s_%s" % (
            str(time()).replace(".", "_"),
            unidecode(filename),
        )
