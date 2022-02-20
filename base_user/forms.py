import re

from django import forms
from django.contrib.auth import (
    authenticate, get_user_model, )
from django.contrib.auth import forms as f
from django.contrib.auth.forms import AuthenticationForm
from django.template import loader

User = get_user_model()


class MyUserLoginForm(AuthenticationForm):

    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if email is not None and password:
            user = User.objects.filter(email=email).first()
            if user and not user.is_active:
                raise forms.ValidationError(
                    self.error_messages['inactive'],
                    code='inactive',
                )

            self.user_cache = authenticate(self.request, email=email, password=password)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get("username")
        user = User.objects.filter(email__iexact=username).first()
        if user:
            return user.email
        return username.lower()


class BaseRegistrationForm(forms.ModelForm):
    """
        A form that creates a user, with no privileges, from the given email and
        password.
        """

    error_messages = {
        "password_incorrect": "Incorrect Password",
        "password_mismatch": "Two passwords did not match",
        "short_password": "Passwords must be at least 6 characters long",
    }
    password1 = forms.CharField(label="Password *", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password Repeat *",
        widget=forms.PasswordInput,
        help_text="Please enter your password again",
    )

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "address",
            "email",
            "phone_prefix",
            "phone",
            'birth_date',
            'gender',
        )

        labels = {
            "first_name": "Ad *",
            "last_name": "Soyad *",
            "email": "Email *",
            "password": "Şifrə *",
            "phone": "Telefon *",
            "address": "Ş/V-ki ünvan *",
        }

        widgets = {
            "address": forms.TextInput(
                attrs={
                    "placeholder": "Ex: Baku, C.Kərimov str. 18. house 9",
                    "autocomplete": "off",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "autocomplete": "new-password",
                    "readonly": "",
                    "onfocus": "this.removeAttribute('readonly');",
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "maxlength": 7,
                    "title": "Please enter non-prefixed phone number",
                    "onkeypress": 'return event.charCode >= 48 && event.charCode <= 57'
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        required_fields = (
            "first_name",
            "last_name",
            "email",
            "phone_prefix",
            "phone",
            "address",
            "birth_date",
            "gender",

        )
        for field in required_fields:
            if field in self.fields and not self.fields[field].required:
                self.fields[field].required = True

        self.fields["phone_prefix"].empty_label = None

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        if len(password1) < 6:
            raise forms.ValidationError(self.error_messages["short_password"])
        else:
            return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages["password_mismatch"], code="password_mismatch",
            )
        return password2

    def clean_email(self):
        email = self.cleaned_data.get("email")
        return email.lower()

    def clean_phone(self):
        from base_user.models import MyUser

        phone = self.cleaned_data.get("phone")
        phone_prefix = self.cleaned_data.get("phone_prefix", None)

        user_list = MyUser.objects.filter(phone_prefix=phone_prefix, phone=phone)

        if user_list.count() > 0:
            raise forms.ValidationError("This number is already in use")

        pattern = '^[0-9]{7}$'
        if not re.match(pattern, phone):
            raise forms.ValidationError("Please enter last 7 digits of phone number")
        return phone

    def clean_first_name(self):
        isascii = lambda s: len(s) == len(s.encode())
        if not isascii(self.cleaned_data["first_name"]):
            raise forms.ValidationError("Only alphabetical characters are allowed")
        return self.cleaned_data["first_name"]

    def clean_last_name(self):
        isascii = lambda s: len(s) == len(s.encode())
        if not isascii(self.cleaned_data["last_name"]):
            raise forms.ValidationError("Only alphanumeric characters are allowed")

        return self.cleaned_data["last_name"]

    def save(self, commit=True):
        user = super(BaseRegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class PasswordResetForm(f.PasswordResetForm):

    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        """
        Send a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        subject = loader.render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)

        # TODO: Implement email send
