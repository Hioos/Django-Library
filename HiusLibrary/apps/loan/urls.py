from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='loanIndex'),
    path('add/',views.add,name='loanAdd'),
    path('loanEdit/<int:id>',views.loanEdit,name='loanEdit'),
    path('pricing/',views.pricing,name='pricing'),
    path('addpricing/',views.addpricing,name='addpricing'),
    path('pricingEdit/<int:id>',views.pricingEdit,name='pricingEdit'),
    path('editPricing/<int:id>',views.editPricing,name='editPricing')
]