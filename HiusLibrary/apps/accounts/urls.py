from django.urls import path
from . import views

urlpatterns = [
    path('logIn',views.login_user,name="LogInAdmin"),
    path('logOut',views.logout_user,name="LogOutAdmin")
    ]