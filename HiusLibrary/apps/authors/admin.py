from django.contrib import admin

# Register your models here.
from apps.authors.models import Authors


class AuthorAdmin (admin.ModelAdmin):
    list_display = ('author_name','author_pseudonym','author_dateOfBirth')
admin.site.register(Authors,AuthorAdmin)