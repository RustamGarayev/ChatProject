# Generated by Django 3.2.12 on 2022-03-22 13:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base_user', '0005_auto_20220322_1716'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='has_accepted_transportation_rules',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='is_active_warehouse_modal_disabled',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='is_order_modal_disabled',
        ),
    ]
