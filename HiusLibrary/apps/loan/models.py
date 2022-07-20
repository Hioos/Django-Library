from django.db import models

# Create your models here.
from django.conf import settings

class loanStatus(models.Model):
    loanStatus_id = models.IntegerField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    loanStatus_name = models.CharField(max_length=50)
    def __str__(self):
        return self.loanStatus_name