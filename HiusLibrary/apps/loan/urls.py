from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='loanIndex'),
    path('add/',views.add,name='loanAdd')
]