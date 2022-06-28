from django.db import models

# Create your models here.
from django.conf import settings


class Authors(models.Model):
    author_id = models.IntegerField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    author_name = models.CharField(max_length=50)
    author_dateOfBirth = models.DateField()
    author_biography = models.TextField()
    author_imgUrl = models.TextField()
    author_nationalImgUrl = models.TextField()
    author_createdAt = models.DateTimeField()
    author_updatedAt = models.DateTimeField()
    author_gender = models.BooleanField()
    author_createdBy = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='author_createdBy'
    )
    author_updatedBy = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='author_updatedBy'
    )
class AuthorsRole(models.Model):
    authorRole_id = models.IntegerField(auto_created=True,primary_key=True, serialize=False, verbose_name='ID')
    authorRole_name = models.CharField(max_length=50,unique=True)
    authorRole_createdAt = models.DateTimeField()
    authorRole_updatedAt = models.DateTimeField()
    authorRole_createdBy = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='authorRole_createdBy'
    )
    authorRole_updatedBy = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='authorRole_updatedBy'
    )



