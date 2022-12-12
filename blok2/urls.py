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
from blok2 import views






urlpatterns = [
    path('', views.Account, name='Account'),
    re_path('Account_user/', views.Account_user, name='Account_user'),
    re_path('Account_user_pass/', views.Account_user_pass, name='Account_user_pass'),
    re_path('MarketExchange/', views.MarketExchange, name='MarketExchange'),
    re_path('NameCurrency/', views.NameCurrency, name='NameCurrency'),
    re_path('FiatWallet/', views.FiatWallet, name='FiatWallet'),
    re_path('BalanceCurrency/', views.BalanceCurrency, name='BalanceCurrency'),
    re_path('PricesCurrency/', views.PricesCurrency, name='PricesCurrency'),
    re_path('FNews/', views.FNews, name='FNews'),
    re_path('FNewsImage/', views.FNewsImage, name='FNewsImage'),
    re_path('ExchangeList/', views.ExchangeList, name='ExchangeList'),
    re_path('Users_clients/', views.Users_clients, name='Users_clients'),
    re_path('Users_clients_active/', views.Users_clients_active, name='Users_clients_active'),
    re_path('Users_clients_deactivate/', views.Users_clients_deactivate, name='Users_clients_deactivate'),
    re_path('Exchange_operations/', views.Exchange_operations, name='Exchange_operations'),
    re_path('Exchange_operations_client/', views.Exchange_operations_client, name='Exchange_operations_client'),

    #re_path('NameCurrencyTrading/', views.NameCurrencyTrading, name='NameCurrencyTrading'),



#    re_path('Print_report/', views.Print_report, name='Print_report'),
#    re_path('Print_pdf/', views.Print_pdf, name='Print_pdf'),



]