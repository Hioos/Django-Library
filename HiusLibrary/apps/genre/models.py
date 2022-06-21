from django.db import models

# Create your models here.
class Genre(models.Model):
    genre_name = models.CharField(max_length=50)
    genre_description = models.TextField(max_length=1000)
    genre_code= models.CharField(max_length=10)
    genre_updatedAt = models.DateTimeField()
    genre_createdAt = models.DateTimeField()
    genre_createdBy = models.ForeignKey('administrator.Administrator', on_delete=models.CASCADE,related_name='genre_created_by')
    genre_updatedBy = models.ForeignKey('administrator.Administrator', on_delete=models.CASCADE,related_name='genre_updated_by')
class SubGenre(models.Model):
    subgenre_name = models.CharField(max_length=50)
    subgenre_description = models.TextField(max_length=1000)
    subgenre_code = models.CharField(max_length=10)
    subgenre_updatedAt = models.DateTimeField()
    subgenre_createdAt = models.DateTimeField()
    subgenre_ofGenre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    subgenre_createdBy = models.ForeignKey('administrator.Administrator', on_delete=models.CASCADE,related_name='subgenre_created_by')
    subgenre_updatedBy = models.ForeignKey('administrator.Administrator', on_delete=models.CASCADE,related_name='subgenre_updated_by')
class Themes(models.Model):
    theme_id = models.IntegerField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    theme_name = models.CharField(max_length=50)
    theme_description = models.CharField(max_length=255)
    theme_createdAt = models.DateTimeField()
    theme_updatedAt = models.DateTimeField()
    theme_createdBy = models.ForeignKey('administrator.Administrator', on_delete=models.CASCADE,related_name='theme_created_by')
    theme_updatedBy = models.ForeignKey('administrator.Administrator', on_delete=models.CASCADE,related_name='theme_updated_by')