from django.contrib import admin

# Register your models here.
from apps.loan.models import loanStatus


class loanStatusAdmin (admin.ModelAdmin):
    list_display = ('loanStatus_name',)
admin.site.register(loanStatus,loanStatusAdmin)