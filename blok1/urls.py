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
from blok1 import views

urlpatterns = [
    path('', views.Home, name='Home'),
    re_path('Registration/', views.Registration, name='Registration'),
    re_path('Verify/(?P<uuid>[a-z0-9\-]+)/', views.Verify, name='Verify'),
    re_path('list_currencies_sell/', views.list_currencies_sell, name='list_currencies_sell'),
    re_path('form_exchange/(?P<currence_purchase_id>[\w-]+)/(?P<currence_sell_id>[\w-]+)', views.form_exchange, name='form_exchange'),
    re_path('Exchange_currency_result/(?P<currency_by_id>[\w-]+)/(?P<currency_sell_id>[\w-]+)', views.Exchange_currency_result, name='Exchange_currency_result'),
    re_path('Exchange_currency_select_by/', views.Exchange_currency_select_by, name='Exchange_currency_select_by'),
    re_path('Exchange_currency_bid/(?P<currency_by_id>[\w-]+)/(?P<currency_sell_id>[\w-]+)', views.Exchange_currency_bid, name='Exchange_currency_bid'),
    re_path('Exchange_currency_bid_info/(?P<request_id>[\w-]+)/(?P<market>[\w-]+)/(?P<name_bank_buy>[\w-]+)', views.Exchange_currency_bid_info, name='Exchange_currency_bid_info'),
    re_path('Exchange_currency_pay/(?P<request_id>[\w-]+)', views.Exchange_currency_pay, name='Exchange_currency_pay'),
    re_path('Exchange_request_del/', views.Exchange_request_del, name='Exchange_request_del'),
    re_path('Site_maintenance_check/', views.Site_maintenance_check, name='Site_maintenance_check'),
    re_path('Site_maintenance_active/', views.Site_maintenance_active, name='Site_maintenance_active'),
    re_path('Site_maintenance_deactivate/', views.Site_maintenance_deactivate, name='Site_maintenance_deactivate'),


]