"""HiusLibrary URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('apps.home.urls')),
    path('administrator/',include('apps.administrator.urls')),
    path('genre/',include('apps.genre.urls')),
    path('authors/', include('apps.authors.urls')),
    path('loan/',include('apps.loan.urls')),
    path('user/',include('apps.users.urls')),
    path('login/',include('apps.authentication.urls'))
]
