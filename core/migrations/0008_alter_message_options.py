# Generated by Django 3.2.12 on 2022-03-09 07:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_chatgroup_slug'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ('timestamp',)},
        ),
    ]
