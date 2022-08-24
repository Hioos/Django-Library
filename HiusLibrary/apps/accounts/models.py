import datetime

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models


# Create your models here.
class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, name, date_joined, phone_number, address, birth_date, expired_date,
                    national_id, created_by, profile_image, password=None):
        if not email:
            raise ValueError("User must have an Email")
        if not username:
            raise ValueError("User must have User Name")
        if profile_image == 'NULL':
            user = self.model(
                email=email,
                username=username,
                password=password,
                name=name,
                date_joined=date_joined,
                phone_number=phone_number,
                address=address,
                birth_date=birth_date,
                expired_date=expired_date,
                national_id=national_id,
                created_by=Account(pk=created_by)
            )
        else:
            user = self.model(
                email=email,
                username=username,
                password=password,
                name=name,
                date_joined=date_joined,
                phone_number=phone_number,
                address=address,
                birth_date=birth_date,
                expired_date=expired_date,
                national_id=national_id,
                profile_image=profile_image,
                created_by=Account(pk=created_by)
            )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.model(
            email=email,
            username=username,
            password=password,
        )
        user.set_password(password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self.db)
        return user

    def create_staff(self, email, username, name, date_joined, phone_number, address, birth_date, national_id,
                     created_by, profile_image, is_admin, is_staff, password=None):
        if profile_image == 'NULL':
            user = self.model(
                email=email,
                username=username,
                password=password,
                name=name,
                date_joined=date_joined,
                phone_number=phone_number,
                address=address,
                birth_date=birth_date,
                national_id=national_id,
                is_admin=is_admin,
                is_staff=is_staff,
                created_by=Account(pk=created_by)
            )
        else:
            user = self.model(
                email=email,
                username=username,
                password=password,
                name=name,
                date_joined=date_joined,
                phone_number=phone_number,
                address=address,
                birth_date=birth_date,
                national_id=national_id,
                is_admin=is_admin,
                is_staff=is_staff,
                profile_image=profile_image,
                created_by=Account(pk=created_by)
            )
        user.set_password(password)
        user.save(using=self._db)
        return user


def get_profile_image_filepath(self, filename):
    return f'images/{self.pk}/{"profile_image.png"}'


def get_default_profile_image():
    return f'images/default.png'


class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=30)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    phone_number = models.CharField(max_length=10, unique=True)
    address = models.CharField(max_length=50)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    birth_date = models.DateField(default=datetime.date.today)
    expired_date = models.DateField(default=datetime.date.today)
    national_id = models.CharField(max_length=12, unique=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    linkedIn = models.CharField(max_length=255, blank=True, null=True)
    twitter = models.CharField(max_length=255, blank=True, null=True)
    instagram = models.CharField(max_length=255, blank=True, null=True)
    facebook = models.CharField(max_length=255, blank=True, null=True)
    created_by = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE,
                                   related_name="user_created_by")
    banned_by = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE,
                                  related_name="user_banned_by")
    profile_image = models.ImageField(max_length=255, upload_to=get_profile_image_filepath, null=True, blank=True,
                                      default=get_default_profile_image)
    objects = MyAccountManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def get_profile_image_filename(self):
        return str(self.profile_image)[str(self.profile_image).index(f'images/{self.pk}/'):]

def get_pricing_image_filepath(self, filename):
    return f'images/pricing/{self.pk}/{"pricing_image.png"}'


def get_default_pricing_image():
    return f'images/pricing/default.png'

class Pricing(models.Model):
    pricing_id = models.IntegerField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    pricing_name = models.TextField()
    pricing_price = models.FloatField()
    pricing_days = models.IntegerField(default=7)
    pricing_image = models.ImageField(max_length=255, upload_to=get_pricing_image_filepath, null=True, blank=True,
                                      default=get_default_pricing_image)
    def __str__(self):
        return self.pricing_name
    def get_default_pricing_image(self):
        return str(self.pricing_image)[str(self.pricing_image).index(f'images/pricing/{self.pk}/'):]
class PaymentHistory(models.Model):
    history_Id = models.IntegerField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    user_id = models.ForeignKey('Account', on_delete=models.CASCADE, related_name='user_id')
    pricing = models.ForeignKey('Pricing', on_delete=models.CASCADE, related_name='pricing')
    history_timestamp = models.DateTimeField(verbose_name="history_timestamp", auto_now_add=True)
    old_expired_date = models.DateField(default=datetime.date.today)
    new_expired_date = models.DateField(default=datetime.date.today)