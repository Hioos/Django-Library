from django.contrib import admin

# Register your models here.
from apps.book.models import Books, Language


class BookAdmin (admin.ModelAdmin):
    list_display = ('book_name','book_released','book_publisher','book_language')
class LanguageAdmin (admin.ModelAdmin):
    list_display = ('language_name','language_code')
admin.site.register(Books,BookAdmin)
admin.site.register(Language,LanguageAdmin)