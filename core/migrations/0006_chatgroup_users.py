# Generated by Django 3.2.12 on 2022-03-07 09:46

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0005_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatgroup',
            name='users',
            field=models.ManyToManyField(blank=True, null=True, related_name='group_users', to=settings.AUTH_USER_MODEL),
        ),
    ]
