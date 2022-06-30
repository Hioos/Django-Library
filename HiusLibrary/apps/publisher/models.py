from django.db import models

# Create your models here.
from django.conf import settings

class Publisher(models.Model):
    publisher_id = models.IntegerField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    publisher_name = models.CharField(max_length=50)
    publisher_createdAt = models.DateTimeField()
    publisher_updatedAt = models.DateTimeField()
    publisher_createdBy = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="publisher_createdBy"
    )
    publisher_updatedBy = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="publisher_updatedBy"
    )