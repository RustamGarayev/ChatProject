# Generated by Django 3.2.12 on 2022-03-07 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_chatgroup_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatgroup',
            name='slug',
            field=models.SlugField(blank=True, max_length=20, null=True, unique=True),
        ),
    ]
