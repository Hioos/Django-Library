# Generated by Django 4.0.5 on 2022-06-29 08:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthorsRole',
            fields=[
                ('authorRole_id', models.IntegerField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('authorRole_name', models.CharField(max_length=50, unique=True)),
                ('authorRole_createdAt', models.DateTimeField()),
                ('authorRole_updatedAt', models.DateTimeField()),
                ('authorRole_createdBy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='authorRole_createdBy', to=settings.AUTH_USER_MODEL)),
                ('authorRole_updatedBy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='authorRole_updatedBy', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Authors',
            fields=[
                ('author_id', models.IntegerField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author_name', models.CharField(max_length=50)),
                ('author_dateOfBirth', models.DateField()),
                ('author_biography', models.TextField()),
                ('author_imgUrl', models.TextField()),
                ('author_nationalImgUrl', models.TextField()),
                ('author_createdAt', models.DateTimeField()),
                ('author_updatedAt', models.DateTimeField()),
                ('author_gender', models.BooleanField()),
                ('author_createdBy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author_createdBy', to=settings.AUTH_USER_MODEL)),
                ('author_updatedBy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author_updatedBy', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
