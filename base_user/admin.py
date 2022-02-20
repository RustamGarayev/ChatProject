from django.contrib import admin

from base_user.models import *


@admin.register(MyUser)
class MyUserAdmin(admin.ModelAdmin):
    pass


@admin.register(UserActivation)
class UserActivationAdmin(admin.ModelAdmin):
    pass
