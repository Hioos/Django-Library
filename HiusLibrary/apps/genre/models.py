from django.db import models

# Create your models here.
from django.conf import settings


class Genre(models.Model):
    genre_name = models.CharField(max_length=50)
    genre_description = models.TextField(max_length=1000)
    genre_code= models.CharField(max_length=10)
    genre_updatedAt = models.DateTimeField()
    genre_createdAt = models.DateTimeField()
    genre_createdBy = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='genre_createdBy'
    )
    genre_updatedBy = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='genre_updatedBy'
    )
class SubGenre(models.Model):
    subgenre_name = models.CharField(max_length=50)
    subgenre_description = models.TextField(max_length=1000)
    subgenre_code = models.CharField(max_length=10)
    subgenre_updatedAt = models.DateTimeField()
    subgenre_createdAt = models.DateTimeField()
    subgenre_ofGenre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    subgenre_createdBy = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='subGenre_createdBy'
    )
    subgenre_updatedBy = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='subGenre_UpdatedBy'
    )
class Themes(models.Model):
    theme_id = models.IntegerField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    theme_name = models.CharField(max_length=50)
    theme_description = models.CharField(max_length=255)
    theme_createdAt = models.DateTimeField()
    theme_updatedAt = models.DateTimeField()
    theme_createdBy = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='theme_createdBy'
    )
    theme_updatedBy = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='theme_updatedBy'
    )