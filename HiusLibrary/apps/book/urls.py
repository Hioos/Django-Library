from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='booksIndex'),
    path('add',views.add,name='booksAdd'),
    path('addNew',views.addBook,name='addBook'),
    path('edit/<int:id>',views.edit,name='editBook'),
    path('update/<int:id>',views.update,name='updateBook'),
    path('language/',views.languageIndex,name='languageIndex'),
    path('language/add',views.addLanguageProc,name='languageAdd'),
    path('lending',views.lendingPage,name='lendingPage'),
    path('lending/addNew',views.lendingAdd,name='lendingAdd'),
    path('lending/lendingAddProcess',views.lendingAddProcess,name='lendingAddProcess'),
    path('lending/acceptAll/<int:id>',views.acceptAll,name='acceptAll'),
    path('lending/denyAll/<int:id>',views.denyAll,name='denyAll')
    ]