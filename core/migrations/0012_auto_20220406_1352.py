# Generated by Django 3.2.12 on 2022-04-06 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_chatgroup_is_contact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatgroup',
            name='group_name',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='chatgroup',
            name='slug',
            field=models.SlugField(blank=True, max_length=40, null=True, unique=True),
        ),
    ]