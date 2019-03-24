"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from datame.views import *
from authentication import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/login', obtain_jwt_token),
    path('api/v1/refresh',refresh_jwt_token),
    path('api/v1/bill/', Bill,name='bill'),
    path('api/v1/offer/', Offer ,name='offer'),
    path('api/v1/apply/', Apply,name='apply'),
    path('api/v1/contract/', Contract,name='contract'),
    path('api/v1/file/', File,name='file'),
    path('api/v1/helloworld', views.HelloWorld.as_view()),
    path('api/v1/cv/', CV,name='cv')

]
