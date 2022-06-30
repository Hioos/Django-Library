from django.db import models
from django.conf import settings

# Create your models here.
from django_countries.fields import CountryField


class Books(models.Model):
    book_id = models.IntegerField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    book_name = models.CharField(max_length=255)
    book_image = models.CharField(max_length=255)
    book_description = models.CharField(max_length=255)
    book_language = CountryField()
    book_publisher = models.ForeignKey('publisher.Publisher',on_delete=models.CASCADE,related_name='book_publisher')
    book_released = models.IntegerField()
    book_updatedAt = models.DateTimeField()
    book_createdAt = models.DateTimeField()
    book_createdBy = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='book_createdBy'
    )
    book_updatedBy = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='book_updatedBy'
    )
class BookThemes(models.Model):
    bookthemes_bookId = models.ForeignKey('Books',on_delete=models.CASCADE,related_name='book_Themes_bookId')
    bookthemes_themeId = models.ForeignKey('genre.Themes',on_delete=models.CASCADE,related_name='book_Themes_themeId')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['bookthemes_bookId', 'bookthemes_themeId'], name='book_themes_combination'
            )
        ]
class BookSubGenre(models.Model):
    booksubgenre_bookId = models.ForeignKey('Books',on_delete=models.CASCADE,related_name='book_Subgenre_bookId')
    booksubgenre_subgenreId = models.ForeignKey('genre.SubGenre',on_delete=models.CASCADE,related_name='book_Subgenre_subgenreId')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['booksubgenre_bookId', 'booksubgenre_subgenreId'], name='book_subgenre_combination'
            )
        ]
class BookAuthorship(models.Model):
    bookauthorship_bookId = models.ForeignKey('Books',on_delete=models.CASCADE,related_name='book_Authorship_bookId')
    bookauthorship_authorId = models.ForeignKey('authors.Authors',on_delete=models.CASCADE,related_name='book_Authorship_authorId')
    bookauthorship_authorRole = models.ForeignKey('authors.AuthorsRole',on_delete=models.CASCADE,related_name='book_Authorship_authorRole')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['bookauthorship_bookId', 'bookauthorship_authorId','bookauthorship_authorRole'], name='book_author_ship_combination'
            )
        ]
