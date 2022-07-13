from django.contrib import admin

# Register your models here.
from apps.publisher.models import Publisher


class PublisherAdmin (admin.ModelAdmin):
    list_display = ('publisher_name',)
admin.site.register(Publisher,PublisherAdmin)