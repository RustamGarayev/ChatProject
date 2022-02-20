from django.contrib import admin
from core.models import *


@admin.register(PhonePrefix)
class PhonePrefixAdmin(admin.ModelAdmin):
    pass


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    pass
