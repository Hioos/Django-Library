from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='authorsIndex'),
    path('add/',views.add,name='authorsAdd'),
    path('add/addNewAuthor',views.addNewAuthor,name='authorsAddNew'),
    path('update/<int:id>',views.update,name='updateAuthor'),
    path('update/updateProcess/<int:id>',views.updateProcess,name='updateProcess')
]