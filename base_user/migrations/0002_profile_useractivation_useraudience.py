# Generated by Django 3.2.12 on 2022-02-13 19:34

import base_user.tools.file_manager
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base_user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserActivation',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='base_user.myuser')),
                ('mail_sent', models.BooleanField(default=False)),
                ('activation_link', models.CharField(blank=True, max_length=500)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserAudience',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('query', models.CharField(editable=False, max_length=1000)),
                ('anon_users', models.BooleanField(default=False, help_text='Include anonymous users')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_order_modal_disabled', models.BooleanField(default=False)),
                ('is_active_warehouse_modal_disabled', models.BooleanField(default=False)),
                ('has_accepted_transportation_rules', models.BooleanField(default=False)),
                ('signature', models.ImageField(blank=True, upload_to=base_user.tools.file_manager.get_signature_path)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
