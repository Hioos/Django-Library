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
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('adminControlPanel/', admin.site.urls),
    path('admin/authenticate/', include('django.contrib.auth.urls')),
    path('admin/authenticate/',include('apps.accounts.urls')),
    path('admin/',include('apps.home.urls')),
    path('',include('apps.userIndex.urls')),
    path('admin/genre/',include('apps.genre.urls')),
    path('admin/authors/', include('apps.authors.urls')),
    path('admin/loan/',include('apps.loan.urls')),
    path('admin/publisher/',include('apps.publisher.urls')),
    path('admin/book/',include('apps.book.urls'))
] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
