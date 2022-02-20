import logging
import ssl
import bcrypt
import sendgrid

from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import views
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.urls.base import reverse
from django.utils.http import urlsafe_base64_decode
from django.template.loader import render_to_string
from django.views import generic

from base_user.forms import BaseRegistrationForm, MyUserLoginForm, PasswordResetForm
from base_user.tools.login_helper_view import AuthView
from base_user.tools.token import account_activation_token
from base_user.models import UserActivation

from sendgrid.helpers.mail import *
from chat_app.settings import SENDGRID_API_KEY, EMAIL_HOST_USER


User = get_user_model()
logr = logging.getLogger(__name__)

ssl._create_default_https_context = ssl._create_unverified_context


class AccountBaseLoginView(AuthView, views.LoginView):
    """
        Account Login View if user is login
        Return to dashboard view
    """

    template_name = "account/login.html"
    form_class = MyUserLoginForm

    def get_success_url(self):
        return reverse('core:index')

    def form_invalid(self, form, *args, **kwargs):
        """
            Check old password before returning error
        """
        return self.check_old_password_before_err(form)

    def check_old_password_before_err(self, form):
        """Check old db password"""
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = User.objects.filter(email=email).first()
        logr.debug("invalid user: %s" % user)

        if password and user is not None and user.old_psw_hash:

            # check if old password matches
            if bcrypt.checkpw(
                    password.encode("utf-8"), user.old_psw_hash.encode("utf-8")
            ):
                # set password as new password
                user.set_password(password)
                user.save()

                # login user
                auth_login(self.request, user)
                return HttpResponseRedirect(self.get_success_url())

        return super().form_invalid(form)


class AccountRegistrationView(AuthView, generic.CreateView):
    """
        Account Register View if user is login
        Return to dashboard view
    """

    template_name = "account/register.html"
    form_class = BaseRegistrationForm
    model = User
    success_url = reverse_lazy("account:register-done")
    user = None

    @staticmethod
    def __default_send_email(user, activation_link):
        mail_subject = "Activate your account"
        message_body = render_to_string(
            "email/email-activation.html",
            {"user": user, "activation_link": activation_link},
        )

        email_content = Content("text/html", message_body)
        message = Mail(
            from_email=Email(EMAIL_HOST_USER),
            subject=mail_subject,
            html_content=email_content)

        personalization = Personalization()
        personalization.add_to(Email(user.email))
        message.add_personalization(personalization)

        sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)
        response = sg.client.mail.send.post(request_body=message.get())

        return response

    def send_activation_mail(self, user):
        user_activation = user.useractivation
        activation_link = user_activation.full_activation_link

        self.__default_send_email(user, activation_link)

        user_activation.mail_sent = True
        user_activation.save()

    def form_valid(self, form):
        user = form.save()
        user.is_active = False

        user.save()

        # Create corresponding user activation instance once user created
        UserActivation.objects.create(user=user)

        self.send_activation_mail(user)
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class AccountRegistrationConfirmView(AuthView, generic.TemplateView):
    template_name = "account/register-confirm.html"
    user = None
    error = None

    @staticmethod
    def get_user(uidb64):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        return user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["error"] = self.error
        return context

    def get(self, request, *args, **kwargs):
        self.user = self.get_user(kwargs["uidb64"])
        if self.user:
            if account_activation_token.check_token(self.user, kwargs["token"]):
                self.user.is_active = True
                self.user.save()
            else:
                self.error = "Token failed"
        else:
            self.error = "user not found"

        return super().get(request, *args, **kwargs)


class AccountRegistrationDoneView(AuthView, generic.TemplateView):
    template_name = "account/register-success.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ref"] = self.request.GET.get("ref", None)
        return context


class ForgetPasswordView(AuthView, views.PasswordResetView):
    """
        Forget password view
    """

    template_name = "account/forgot-password.html"
    subject_template_name = "email/password_reset_subject.txt"
    email_template_name = "email/password_reset_email.html"
    success_url = reverse_lazy("account:forget-done")
    form_class = PasswordResetForm

    def get_context_data(self, **kwargs):
        context = super(ForgetPasswordView, self).get_context_data(**kwargs)
        return context


class ForgetPasswordDoneView(AuthView, views.PasswordResetDoneView):
    """
        Forget password view
    """

    template_name = "account/forgot-password-done.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ForgetPasswordResetConfirmView(AuthView, views.PasswordResetConfirmView):
    """
        Forget password view
    """

    template_name = "account/forgot-password-confirm.html"
    post_reset_login = True
    success_url = reverse_lazy("dashboard-page")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
