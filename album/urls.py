"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf.urls.static import static
from django.urls import path, re_path, include
from django.conf.urls import handler404

from album.settings import local

from applications.home import views

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path('', include("applications.user.urls")),
    re_path('', include("applications.home.urls")),
    
] + static(local.MEDIA_URL, document_root = local.MEDIA_ROOT)


handler404 = views.Error404TemplateView.as_view()