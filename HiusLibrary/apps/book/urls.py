from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='booksIndex'),
    path('add',views.add,name='booksAdd'),
    path('addNew',views.addBook,name='addBook'),
    path('language/',views.languageIndex,name='languageIndex'),
    path('language/add',views.addLanguageProc,name='languageAdd')
    ]