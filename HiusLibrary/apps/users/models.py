from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

# Create your models here.
class Users(AbstractBaseUser):
    user_id = models.IntegerField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    user_name = models.CharField(max_length=50)
    user_address = models.CharField(max_length=50)
    user_email = models.CharField(max_length=50)
    user_phoneNumber = models.CharField(max_length=11)
    user_nationalIdentificationNumber = models.CharField(max_length=12)
    user_dateOfBirth = models.DateField()
    user_userName = models.CharField(max_length=50)
    user_password = models.CharField(max_length=255,default= '1')
    user_permission = models.BooleanField(default=True)
    user_createdAt = models.DateTimeField()
    user_updatedAt = models.DateTimeField()
    user_createdBy = models.ForeignKey('administrator.Administrator', on_delete=models.CASCADE,
                                             related_name='user_created_by')
    user_updatedBy = models.ForeignKey('administrator.Administrator', on_delete=models.CASCADE,
                                             related_name='user_updated_by')
    user_membershipStart = models.DateField()
    user_membershipEnd = models.DateField()

    USERNAME_FIELD = 'user_userName'
    PASSWORD_FIELD = 'user_password'