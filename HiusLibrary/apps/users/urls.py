from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='userIndex'),
    path('add/',views.add,name='userAdd'),
    path('addNew/',views.addNewMember,name='userAddNew'),
    path('extend/<int:id>',views.extend,name='extend'),
    path('block/<int:id>',views.block,name='block')
    ]