from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .models import Account, Pricing


class AccountAdmin (UserAdmin):
    list_display = ('email','username','date_joined','last_login','is_admin','is_staff')
    search_fields = ('email','username')
    readonly_fields = ('id','date_joined','last_login')
    filter_horizontal=()
    list_filter=()
    fieldsets = ()
class PricingAdmin (admin.ModelAdmin):
    list_display = ('pricing_name', 'pricing_price')
admin.site.register(Pricing,PricingAdmin)
admin.site.register(Account,AccountAdmin)