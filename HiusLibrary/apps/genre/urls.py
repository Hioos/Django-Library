from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='genreIndex'),
    path('add/',views.add, name='genreAdd'),
    path('add/addNewGenre/',views.addNewGenre, name ="addNewGenre"),
    path('update/<int:id>',views.update,name='genreUpdate'),
    path('update/updategenre/<int:id>',views.updateGenreProcess,name='updateGenreProcess'),
    path('<int:id>/subgenre/',views.subGenre,name='subgenre'),
    path('<int:id>/subgenre/add',views.subGenreAdd,name='subGenreAdd'),
    path('<int:id>subgenre/add/addNewSubGenre',views.addNewSubGenre,name='addNewSubGenre'),
    path('update/subgenre/<int:id>',views.subGenreUpdate,name='subGenreUpdate'),
    path('update/subgenre/updatesubgenre/<int:id>',views.updateSubGenreProcess,name ='updateSubGenreProcess'),
    path('themes/',views.themes,name='themes'),
    path('themes/add',views.themeAdd,name='themeAdd'),
    path('themes/addNewTheme',views.addNewTheme,name='addNewTheme'),
    path('themes/editTheme/<int:id>',views.editTheme,name='editTheme'),
    path('themes/updateTheme/<int:id>',views.updateTheme,name='updateTheme')
]