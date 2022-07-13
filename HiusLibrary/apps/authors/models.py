from django.db import models

# Create your models here.
from django.conf import settings

def get_author_image_filepath(self,filename):
    return f'images/authors/{self.pk}/{"authors_image.png"}'
def get_default_author_image():
    return f'images/authors/default.png'
class Authors(models.Model):
    author_id = models.IntegerField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    author_pseudonym=models.CharField(max_length=50)
    author_name = models.CharField(max_length=50)
    author_dateOfBirth = models.DateField()
    author_biography = models.TextField()
    author_imgUrl = models.ImageField(max_length=255,upload_to=get_author_image_filepath,null=True,blank=True,default=get_default_author_image)
    author_gender = models.BooleanField()
    def __str__(self):
        return self.author_name
    def has_module_perms(self,app_label):
        return True
    def get_authors_image_filename (self):
        return str(self.author_imgUrl)[str(self.author_imgUrl).index(f'images/authors/{self.pk}/'):]

