from django.db import models

# Create your models here.
class Administrator(models.Model):
    administrator_name = models.CharField(max_length=50)
    administrator_username = models.CharField(max_length=50)
    administrator_password = models.CharField(max_length=255)
    administrator_email = models.EmailField(max_length=50)
    administrator_dateOfBirth = models.DateField()
    administrator_nationalIdentificationNumber = models.CharField(max_length=12)
    administrator_updatedAt = models.DateTimeField()
    administrator_role = models.SmallIntegerField()
    administrator_status = models.BooleanField(default=False)
    administrator_createdAt = models.DateTimeField()
    administrator_lastLogin = models.DateTimeField()
