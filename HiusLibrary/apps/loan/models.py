from django.db import models

# Create your models here.
class loanStatus(models.Model):
    loanStatus_id = models.IntegerField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    loanStatus_name = models.CharField(max_length=50)
    loanStatus_createdAt = models.DateTimeField()
    loanStatus_updatedAt = models.DateTimeField()
    loanStatus_createdBy = models.ForeignKey('administrator.Administrator', on_delete=models.CASCADE,related_name='loan_created_by')
    loanStatus_updatedBy = models.ForeignKey('administrator.Administrator', on_delete=models.CASCADE,related_name='loan_updated_by')