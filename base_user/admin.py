from django.contrib import admin

from base_user import models


@admin.register(models.MyUser)
class MyUserAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(models.UserActivation)
class UserActivationAdmin(admin.ModelAdmin):
    pass
