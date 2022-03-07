from django.db import models
from core.tools.helpers import COUNTRIES, get_group_icon
from django.contrib.sites.models import Site
from django.contrib.auth import get_user_model

User = get_user_model()


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_messages")
    group = models.ForeignKey('ChatGroup', on_delete=models.CASCADE, related_name="group_messages")
    message = models.TextField(default="")
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-timestamp',)

    def __str__(self):
        return "%s" % self.user.get_full_name()

    def last_10_messages(self):
        return Message.objects.filter(group=self.group)[:10]


class ChatGroup(models.Model):
    group_name = models.CharField(max_length=20)
    icon = models.ImageField(upload_to=get_group_icon, blank=True, default="client/assets/group_icon.png")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


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
