# Generated by Django 4.0.5 on 2022-07-20 02:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre_name', models.CharField(max_length=50)),
                ('genre_description', models.TextField(max_length=1000)),
                ('genre_code', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Themes',
            fields=[
                ('theme_id', models.IntegerField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('theme_name', models.CharField(max_length=50)),
                ('theme_description', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='SubGenre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subgenre_name', models.CharField(max_length=50)),
                ('subgenre_description', models.TextField(max_length=1000)),
                ('subgenre_code', models.CharField(max_length=10)),
                ('subgenre_ofGenre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='genre.genre')),
            ],
        ),
    ]