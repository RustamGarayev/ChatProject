from django.db import models
from core.tools.helpers import COUNTRIES
from django.contrib.sites.models import Site


class PhonePrefix(models.Model):
    # information
    country = models.CharField(choices=COUNTRIES, max_length=3, default="AZ")
    prefix = models.CharField(max_length=10, unique=True)
    order = models.IntegerField(default=0)

    # moderation
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}".format(self.prefix)


class Setting(models.Model):
    # information
    site = models.OneToOneField(Site, on_delete=models.CASCADE, related_name="settings")
    client_prefix = models.CharField(max_length=3, default="CTA", blank=True)

    def __str__(self):
        return "Setting of: {}".format(self.site)
