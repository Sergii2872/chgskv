"""test_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path, include, re_path
from blok3 import views

urlpatterns = [
    re_path('NewsFeed/', views.NewsFeed, name='NewsFeed'),
    re_path('News_Image_View/(?P<image_id>\w+)/', views.News_Image_View, name='News_Image_View'),
    re_path('Regulations/', views.Regulations, name='Regulations'),
    re_path('Contact/', views.Contact, name='Contact'),
    re_path('Terms/', views.Terms, name='Terms'),



]