from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='publisherIndex'),
    path('add/',views.add,name='publisherAdd'),
    path('edit/<int:id>',views.edit,name='publisherEdit')
]