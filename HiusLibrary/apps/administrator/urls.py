from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='adminIndex'),
    path('add/',views.add, name='adminAdd'),
    path('add/addNewAdministrator/',views.addNewAdministrator, name='addNewAdministrator'),
    path('changeRole/<int:id>',views.changeRole,name = "adminChangeRole"),
]