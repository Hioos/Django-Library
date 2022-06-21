from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='login'),
    path('process/',views.login_user,name='loginProcess')
]