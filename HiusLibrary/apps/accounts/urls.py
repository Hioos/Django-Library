from django.urls import path
from . import views

urlpatterns = [
    path('logIn',views.login_user,name="LogInAdmin"),
    path('logOut',views.logout_user,name="LogOutAdmin"),
    path('account/user',views.userIndex,name="userIndex"),
    path('account/user/add',views.add,name="userAdd"),
    path('account/user/adding',views.addUser,name="addUser")
    ]