# Generated by Django 4.0.5 on 2022-06-29 08:05

import apps.accounts.models
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('email', models.EmailField(max_length=60, unique=True, verbose_name='email')),
                ('username', models.CharField(max_length=30, unique=True)),
                ('name', models.CharField(max_length=30)),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('phone_number', models.CharField(max_length=10, unique=True)),
                ('address', models.CharField(max_length=50)),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='last login')),
                ('birth_date', models.DateField(default=datetime.date.today)),
                ('expired_date', models.DateField(default=datetime.date.today)),
                ('national_id', models.CharField(max_length=12, unique=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('profile_image', models.ImageField(blank=True, default=apps.accounts.models.get_default_profile_image, max_length=255, null=True, upload_to=apps.accounts.models.get_profile_image_filepath)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_created_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
