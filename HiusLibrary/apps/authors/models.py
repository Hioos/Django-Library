from django.db import models

# Create your models here.
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
    author_createdBy = models.ForeignKey('administrator.Administrator', on_delete=models.CASCADE,related_name='created_by')
    author_updatedBy = models.ForeignKey('administrator.Administrator', on_delete=models.CASCADE,related_name='updated_by')
