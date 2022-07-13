from django.db import models

# Create your models here.
from django.conf import settings


class Genre(models.Model):
    genre_name = models.CharField(max_length=50)
    genre_description = models.TextField(max_length=1000)
    genre_code= models.CharField(max_length=10)
    def __str__(self):
        return self.genre_name
class SubGenre(models.Model):
    subgenre_name = models.CharField(max_length=50)
    subgenre_description = models.TextField(max_length=1000)
    subgenre_code = models.CharField(max_length=10)
    subgenre_ofGenre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    def __str__(self):
        return self.subgenre_name
class Themes(models.Model):
    theme_id = models.IntegerField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    theme_name = models.CharField(max_length=50)
    theme_description = models.CharField(max_length=255)
    def __str__(self):
        return self.theme_name