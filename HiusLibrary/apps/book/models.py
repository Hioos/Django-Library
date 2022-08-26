import datetime

from django.db import models
from django.conf import settings

# Create your models here.
from django_countries.fields import CountryField
from apps.accounts.models import Account


def get_language_image_filepath(self, filename):
    return f'images/language/{self.pk}/{"language_image.png"}'


def get_default_language_image():
    return f'images/language/default.png'


def get_profile_image_filepath(self, filename):
    return f'images/book/{self.pk}/{"book_image.png"}'


def get_default_profile_image():
    return f'images/book/default.png'


class Books(models.Model):
    book_id = models.IntegerField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    book_name = models.CharField(max_length=255)
    book_image = models.ImageField(max_length=255, upload_to=get_profile_image_filepath, null=True, blank=True,
                                   default=get_default_profile_image)
    book_description = models.TextField()
    book_language = models.ForeignKey('Language', on_delete=models.CASCADE, related_name='book_language')
    book_publisher = models.ForeignKey('publisher.Publisher', on_delete=models.CASCADE, related_name='book_publisher')
    book_released = models.IntegerField()
    book_pages = models.IntegerField()
    book_price = models.FloatField()

    class Meta:
        get_latest_by = ['book_id']

    def __str__(self):
        return self.book_name

    def has_module_perms(self, app_label):
        return True

    def get_profile_image_filename(self):
        return str(self.book_image)[str(self.book_image).index(f'images/book/{self.pk}/'):]


class Language(models.Model):
    language_id = models.IntegerField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    language_name = models.CharField(max_length=255, unique=True)
    language_code = models.CharField(max_length=5, unique=True)
    language_image = models.ImageField(max_length=255, upload_to=get_language_image_filepath, null=True, blank=True,
                                       default=get_default_language_image)

    def __str__(self):
        return self.language_name

    def has_module_perms(self, app_label):
        return True

    def get_language_image_filename(self):
        return str(self.language_image)[str(self.language_image).index(f'images/language/{self.pk}/'):]


class BookThemes(models.Model):
    bookthemes_bookId = models.ForeignKey('Books', on_delete=models.CASCADE, related_name='book_Themes_bookId')
    bookthemes_themeId = models.ForeignKey('genre.Themes', on_delete=models.CASCADE, related_name='book_Themes_themeId')

    def __str__(self):
        return self.bookthemes_bookId

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['bookthemes_bookId', 'bookthemes_themeId'], name='book_themes_combination'
            )
        ]


class BookSubGenre(models.Model):
    booksubgenre_bookId = models.ForeignKey('Books', on_delete=models.CASCADE, related_name='book_Subgenre_bookId')
    booksubgenre_subgenreId = models.ForeignKey('genre.SubGenre', on_delete=models.CASCADE,
                                                related_name='book_Subgenre_subgenreId')

    def __str__(self):
        return self.booksubgenre_bookId

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['booksubgenre_bookId', 'booksubgenre_subgenreId'], name='book_subgenre_combination'
            )
        ]


class BookAuthorship(models.Model):
    bookauthorship_bookId = models.ForeignKey('Books', on_delete=models.CASCADE, related_name='book_Authorship_bookId')
    bookauthorship_authorId = models.ForeignKey('authors.Authors', on_delete=models.CASCADE,
                                                related_name='book_Authorship_authorId')

    def __str__(self):
        return self.bookauthorship_bookId

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['bookauthorship_bookId', 'bookauthorship_authorId'], name='book_author_ship_combination'
            )
        ]


class Receipt(models.Model):
    receipt_id = models.IntegerField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    receipt_user = models.ForeignKey('accounts.Account', on_delete=models.CASCADE, related_name='receipt_user')
    receipt_timestamp = models.DateTimeField(verbose_name="receipt_timestamp", auto_now_add=True)

    class Meta:
        get_latest_by = ['receipt_id']

    def __str__(self):
        return self.receipt_user


class LoanedBook(models.Model):
    loanedBook_id = models.IntegerField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    loanedBook_book = models.ForeignKey('DetailedBook', on_delete=models.CASCADE, related_name='loanedBook_bookId')
    loanedBook_receipt = models.ForeignKey('Receipt', on_delete=models.CASCADE, related_name='loanedBook_receipt')
    loanedBook_startDate = models.DateField(blank=True, null=True)
    loanedBook_dueDate = models.DateField(blank=True, null=True)
    loanedBook_returnedDate = models.DateField(blank=True, null=True)
    loanedBook_statusId = models.ForeignKey('loan.loanStatus', on_delete=models.CASCADE,
                                            related_name='loanedBook_loanStatus')
    loanedBook_receive = models.ForeignKey('accounts.Account', on_delete=models.CASCADE,
                                            related_name='loanedBook_receive',blank=True,null=True)
    loanedBook_confirm = models.ForeignKey('accounts.Account', on_delete=models.CASCADE,
                                           related_name='loanedBook_confirm', blank=True, null=True)
    loanedBook_returnedStatus = models.IntegerField(blank=True,null=True)
    loanedBook_fee = models.FloatField(blank=True,null=True)
    class Meta:
        get_latest_by = ['loanedBook_id']
class DetailedBook(models.Model):
    detailed_id = models.IntegerField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    detailed_book_id = models.ForeignKey('Books', on_delete=models.CASCADE,related_name='id_of_book')
    detailed_book_percentage = models.IntegerField()
    detailed_book_note = models.TextField(blank=True,null=True)
    detailed_returned = models.BooleanField(default=True)
    detailed_importDate = models.DateField(blank=True, null=True)
    def __str__(self):
        return str(self.detailed_id)