from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='indexOfUser'),
    path('book/<int:id>',views.bookInfo, name='userBookInfo'),
    path('genre/<int:id>',views.bookList,name='bookList'),
    path('theme/<int:id>',views.themeInfo,name='userTheme'),
    path('cart',views.cart,name='cart'),
    path('addToCart/<int:id>',views.addtoCart,name='addToCart'),
    path('clearCart',views.clearCart,name='clearCart'),
    path('deleteCart/<int:id>',views.deleteCart,name='deleteCart'),
    path('requestBook',views.requestBook,name='requestBook')
]