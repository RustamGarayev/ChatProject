from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from base_user import views

app_name = "account"

urlpatterns = [
    # Authentication Login Register urls here
    path("login/", views.AccountBaseLoginView.as_view(), name="login"),
    path("register/", views.AccountRegistrationView.as_view(), name="register"),
    path(
        "register/done",
        views.AccountRegistrationDoneView.as_view(),
        name="register-done",
    ),
    path(
        "register/<uidb64>/<token>/",
        views.AccountRegistrationConfirmView.as_view(),
        name="register-confirm",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(next_page=reverse_lazy("core:index")),
        name="logout",
    ),
    path(
        "account/", views.AccountUpdateView.as_view(), name="account-update"
    ),
    # Account forgot password
    path("forget/", views.ForgetPasswordView.as_view(), name="forget"),
    path("forget/done/", views.ForgetPasswordDoneView.as_view(), name="forget-done"),
    path(
        "forget/<uidb64>/<token>/",
        views.ForgetPasswordResetConfirmView.as_view(),
        name="forget-reset-confirm",
    ),
]
