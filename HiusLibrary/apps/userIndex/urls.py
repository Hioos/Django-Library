from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='indexOfUser'),
    path('book/<int:id>',views.bookInfo, name='userBookInfo'),
    path('genre/<int:id>',views.bookList,name='bookList'),
    path('theme/<int:id>',views.themeInfo,name='userTheme')
]