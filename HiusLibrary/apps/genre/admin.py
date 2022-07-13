from django.contrib import admin

# Register your models here.
from apps.genre.models import Genre, SubGenre, Themes


class GenreAdmin (admin.ModelAdmin):
    list_display = ('genre_name','genre_code')
class SubGenreAdmin (admin.ModelAdmin):
    list_display = ('subgenre_name','subgenre_code','subgenre_ofGenre')
class ThemesAdmin (admin.ModelAdmin):
    list_display = ('theme_name',)
admin.site.register(Genre,GenreAdmin)
admin.site.register(SubGenre,SubGenreAdmin)
admin.site.register(Themes,ThemesAdmin)