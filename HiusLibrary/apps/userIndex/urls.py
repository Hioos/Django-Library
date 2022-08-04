from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='indexOfUser'),
    path('book/<int:id>',views.bookInfo, name='userBookInfo'),
    path('genre/<int:id>',views.bookList,name='bookList'),
    path('theme/<int:id>',views.themeInfo,name='userTheme'),
    path('cart',views.cart,name='cart'),
    path('addToCart',views.addtoCart,name='addToCart'),
    path('clearCart',views.clearCart,name='clearCart'),
    path('deleteCart/<int:id>',views.deleteCart,name='deleteCart'),
    path('requestBook',views.requestBook,name='requestBook'),
    path('allBook',views.allBook,name='allBook'),
    path('information',views.information,name='information'),
    path('history',views.history,name='history'),
    path('extend',views.extend,name='extend'),
    path('extend/<int:id>',views.extendInfo,name='extendInfo'),
    path('extendMember/<int:id>',views.extendMember,name='extendMember')
]