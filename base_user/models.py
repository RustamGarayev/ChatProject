from base_user.tools.common import GENDER, get_user_profile_photo_file_name
from base_user.tools.token import account_activation_token
from base_user.tools.file_manager import get_signature_path, get_domain_with_protocol
from base_user.utils.mixins import MyUserMixin
from django.conf import settings
from django.contrib.admin.models import LogEntry
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.contrib.contenttypes.models import ContentType
from django.db.models import JSONField
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import ugettext_lazy as _


USER_MODEL = settings.AUTH_USER_MODEL


class MyUserManager(UserManager):

    def _create_user(self, email, password, **extra_fields):
        """
            Create and save a user with the given username, email, and password.
        """
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class MyUser(AbstractBaseUser, PermissionsMixin, MyUserMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username, password and email are required. Other fields are optional.
    """

    first_name = models.CharField(_("first name"), max_length=255, blank=True)
    last_name = models.CharField(_("last name"), max_length=255, blank=True)
    email = models.EmailField(
        _("email address"), max_length=255, unique=True, db_index=True
    )
    profile_picture = models.ImageField(
        upload_to=get_user_profile_photo_file_name, null=True, blank=True
    )
    phone_prefix = models.ForeignKey(
        "core.PhonePrefix",
        related_name="subscribers",
        blank=True,
        null=True,
        on_delete=models.DO_NOTHING,
    )
    phone = models.CharField(
        blank=True,
        null=True,
        max_length=30,
        help_text="Nömrənin prefixsiz halını daxil edin, məsələn +994503144847, prefiksiz halı 3144847")
    address = models.CharField(blank=True, null=True, max_length=100)
    gender = models.IntegerField(
        choices=GENDER, verbose_name="cinsi", default=0, null=True, blank=True
    )
    client_code = models.CharField(
        db_index=True, unique=True, blank=True, null=True, max_length=30, editable=False
    )

    # legacy fields
    birth_date = models.DateField(blank=True, null=True)
    current_sign_in_ip = models.GenericIPAddressField(blank=True, null=True)
    last_sign_in_ip = models.GenericIPAddressField(blank=True, null=True)
    sign_in_count = models.IntegerField(default=0)

    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin " "site."),
        db_index=True,
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as "
            "active. Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    last_activity = models.DateTimeField(_("last activity"), blank=True, null=True)

    extra = JSONField(blank=True, null=True)

    """
        Important non-field stuff
    """
    objects = MyUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def save(self, *args, **kwargs):
        # Setting unique client code once the user is created
        self.__set_client_code__()

        return super().save(*args, **kwargs)

    def __str__(self):
        return "{client_code} – {full_name}".format(
            client_code=self.client_code,
            full_name=self.get_full_name(),
            email=self.get_username(),
        )

    def get_full_name(self):
        """
            Returns the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
            Returns the short name for the user.
        """
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def get_phone(self):
        if self.phone_prefix:
            return "{0}{1}".format(self.phone_prefix.prefix, self.phone)
        return self.phone

    def get_normalized_phone(self):
        """
        Clear phone number musk
        :return:
        """
        import re

        return "{}".format(re.sub(r"-|\+|\s|\(|\)", "", self.get_phone()))

    def get_user_info(self):
        return "{} | {}".format(self.client_code, self.get_full_name())

    def unmask_input(self):
        return "".join([str(s) for s in self.phone if s.isdigit()])


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    is_order_modal_disabled = models.BooleanField(default=False)
    is_active_warehouse_modal_disabled = models.BooleanField(default=False)
    has_accepted_transportation_rules = models.BooleanField(default=False)

    signature = models.ImageField(blank=True, upload_to=get_signature_path)

    # moderation
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Profile: {}".format(self.user)

    @property
    def has_signature(self):
        return bool(self.signature)


class UserAudience(models.Model):
    title = models.CharField(max_length=100)
    query = models.CharField(max_length=1000, editable=False)
    anon_users = models.BooleanField(
        default=False, help_text=_("Include anonymous users")
    )

    # moderation
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_users(self, queryset=None):

        from django.contrib.auth import get_user_model
        from django.utils import timezone

        # from fulfillment.models import Declaration, Order, Courier

        now = timezone.now()

        if not queryset:
            User = get_user_model()
            users = User.objects.all()
        else:
            users = queryset

        return eval("users%s" % self.query)


class UserActivation(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, primary_key=True, on_delete=models.CASCADE
    )
    mail_sent = models.BooleanField(default=False)
    activation_link = models.CharField(max_length=500, blank=True)

    # moderation
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user}"

    def _get_tokens(self):
        return {
            "uid": urlsafe_base64_encode(force_bytes(self.user.pk)),
            "token": account_activation_token.make_token(self.user),
        }

    def _get_activation_link(self):
        tokens = self._get_tokens()
        activation_link = "{url}".format(
            url=reverse_lazy(
                "account:register-confirm",
                kwargs={"uidb64": tokens["uid"], "token": tokens["token"]},
            )
        )
        return activation_link

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    @property
    def full_activation_link(self):
        protocol_and_domain = get_domain_with_protocol()
        if not self.activation_link:
            self.activation_link = self._get_activation_link()
            self.save()
        full_path = f"{protocol_and_domain}{self.activation_link}"
        return full_path
