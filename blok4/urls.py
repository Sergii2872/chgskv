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
from blok4 import views

urlpatterns = [
    #re_path('main/', views.main, name='main'),
    re_path('Load_Poloniex_NameCurrency/', views.Load_Poloniex_NameCurrency, name='Load_Poloniex_NameCurrency'),
    re_path('Load_Poloniex_Currencies/', views.Load_Poloniex_Currencies, name='Load_Poloniex_Currencies'),
    #re_path('Load_Poloniex_PairCurrency/', views.Load_Poloniex_PairCurrency, name='Load_Poloniex_PairCurrency'), не использую так как изменилась логика курсов валют
    #re_path('Load_Poloniex_Pair_Currencies/', views.Load_Poloniex_Pair_Currencies, name='Load_Poloniex_Pair_Currencies'), не использую так как изменилась логика курсов валют
    re_path('Load_Poloniex_KursCurrency/', views.Load_Poloniex_KursCurrency, name='Load_Poloniex_KursCurrency'),
    re_path('Load_Poloniex_Kurs_Currencies/', views.Load_Poloniex_Kurs_Currencies, name='Load_Poloniex_Kurs_Currencies'),
    re_path('Load_Poloniex_SynchronCurrency/', views.Load_Poloniex_SynchronCurrency, name='Load_Poloniex_SynchronCurrency'),
    re_path('Load_Poloniex_Synchron_Currencies/', views.Load_Poloniex_Synchron_Currencies, name='Load_Poloniex_Synchron_Currencies'),
    re_path('OrderProcessing/', views.OrderProcessing, name='OrderProcessing'),
    re_path('Order_processing_check/', views.Order_processing_check, name='Order_processing_check'),
    re_path('Order_processing_del/', views.Order_processing_del, name='Order_processing_del'),
    re_path('Order_processing_buy/', views.Order_processing_buy, name='Order_processing_buy'),
    re_path('Order_processing_perform/', views.Order_processing_perform, name='Order_processing_perform'),



]