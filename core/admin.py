from django.contrib import admin
from core.models import *


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    pass


@admin.register(ChatGroup)
class ChatGroupAdmin(admin.ModelAdmin):
    pass


@admin.register(PhonePrefix)
class PhonePrefixAdmin(admin.ModelAdmin):
    pass


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    pass
