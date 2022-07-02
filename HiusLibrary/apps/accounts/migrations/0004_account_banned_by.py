# Generated by Django 4.0.5 on 2022-07-02 08:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_account_is_banned'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='banned_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_banned_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
