from django.contrib import admin
from core import models


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ChatGroup)
class ChatGroupAdmin(admin.ModelAdmin):
    pass


@admin.register(models.PhonePrefix)
class PhonePrefixAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Setting)
class SettingAdmin(admin.ModelAdmin):
    pass
