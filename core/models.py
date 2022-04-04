from django.db import models
from django.contrib.sites.models import Site

from core.tools.helpers import COUNTRIES, get_group_icon
from core.utils.mixins import ChatGroupMixin

from base_user.models import MyUser


class Message(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name="user_messages")
    group = models.ForeignKey('ChatGroup', on_delete=models.CASCADE, related_name="group_messages")
    message = models.TextField(default="")
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('timestamp',)

    def __str__(self):
        return "%s" % self.user.get_full_name()

    @staticmethod
    def last_10_messages(group_name):
        return Message.objects.filter(group__slug=group_name)[:10]


class ChatGroup(models.Model, ChatGroupMixin):
    users = models.ManyToManyField(MyUser, related_name="group_users", blank=True)
    group_name = models.CharField(max_length=20)
    slug = models.SlugField(max_length=20, unique=True, null=True, blank=True)
    icon = models.ImageField(upload_to=get_group_icon, blank=True, default="client/assets/group_icon.png")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.group_name

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cache_group_name = self.group_name

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        # Set unique slug when object is created or its group name is changed
        self.__set_slug__()

        return super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
        )

    def get_last_message(self):
        if self.group_messages.last():
            return self.group_messages.last().message
        else:
            return "No message to display"


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
    site = models.OneToOneField(Site, on_delete=models.CASCADE, related_name="settings")
    client_prefix = models.CharField(max_length=3, default="CTA", blank=True)

    is_user_status_enabled = models.BooleanField(default=False)
    is_user_social_accounts_enabled = models.BooleanField(default=False)
    is_multi_user_group_creation_enabled = models.BooleanField(default=False)
    is_group_update_enabled = models.BooleanField(default=False)

    def __str__(self):
        return "Setting of: {}".format(self.site)
