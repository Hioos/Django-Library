from django.contrib import admin

# Register your models here.
from apps.book.models import Books, Language, BookThemes, BookSubGenre, BookAuthorship, LoanedBook, Receipt, \
    DetailedBook

class BookAdmin(admin.ModelAdmin):
    list_display = ('book_name', 'book_released', 'book_publisher', 'book_language')


class LanguageAdmin(admin.ModelAdmin):
    list_display = ('language_name', 'language_code')


class BookThemesAdmin(admin.ModelAdmin):
    list_display = ('bookthemes_bookId', 'bookthemes_themeId')


class BookSubGenreAdmin(admin.ModelAdmin):
    list_display = ('booksubgenre_bookId', 'booksubgenre_subgenreId')


class BookAuthorshipAdmin(admin.ModelAdmin):
    list_display = ('bookauthorship_bookId', 'bookauthorship_authorId')


class ReceiptAdmin(admin.ModelAdmin):
    list_display = ('receipt_id', 'receipt_user', 'receipt_timestamp')


class DetailedBookAdmin(admin.ModelAdmin):
    list_display = ('detailed_id', 'detailed_book_id', 'detailed_book_percentage', 'detailed_book_note')
admin.site.register(DetailedBook, DetailedBookAdmin)
admin.site.register(Receipt, ReceiptAdmin)
admin.site.register(BookAuthorship, BookAuthorshipAdmin)
admin.site.register(BookSubGenre, BookSubGenreAdmin)
admin.site.register(Books, BookAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(BookThemes, BookThemesAdmin)
