from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

# Create your models here.
from django.conf import settings


class Publisher(models.Model):
    publisher_id = models.IntegerField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    publisher_name = models.CharField(max_length=50)


    def __str__(self):
        return self.publisher_name