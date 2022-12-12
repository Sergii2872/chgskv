"""chgskv URL Configuration

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

# blok1 - домашняя страница(верх,основа,футер), основное меню, меню регистрации пользователей(jqury,метод ajax),
#         верификация по email, модель(база данных) пользователей(встроенная user плюс дополнительная profile свои поля)

# blok2 - кабинет пользователя(просмотр,редактирование,удаление данных пользователя), администратора(просмотр,
#         редактирование,удаление справочников сайта), все модели(базы данных) сайта кроме пользователей(blok1)

# blok3 - главная страница обмена, новости, весь функционал


from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static

# для таблицы плагина datatables
from rest_framework.routers import DefaultRouter
from blok2.views import MarketExchange_ViewSet, NameCurrency_ViewSet, FiatWallet_ViewSet, PricesCurrency_ViewSet, BalanceCurrency_ViewSet, News_ViewSet, NewsImage_ViewSet, ExchangeList_ViewSet  #NameCurrencyTrading_ViewSet
router = DefaultRouter()

# табл БД Market_Exchange в blok2/models.py, MarketExchange_ViewSet класс для обмена данными
# методом ajax c скриптом js/table_market_exchange.js
router.register('Market_Exchange', MarketExchange_ViewSet)

# табл БД Name_Currency в blok2/models.py, NameCurrency_ViewSet класс для обмена данными
# методом ajax c скриптом js/table_name_currency.js
router.register('Name_Currency', NameCurrency_ViewSet)

# табл БД Fiat_Wallet в blok2/models.py, FiatWallet_ViewSet класс для обмена данными
# методом ajax c скриптом js/table_fiat_wallet.js
router.register('Fiat_Wallet', FiatWallet_ViewSet)

# табл БД Prices_Currency в blok2/models.py, PricesCurrency_ViewSet класс для обмена данными
# методом ajax c скриптом js/table_prices_currency.js
router.register('Prices_Currency', PricesCurrency_ViewSet)

# табл БД Balance_Currency в blok2/models.py, BalanceCurrency_ViewSet класс для обмена данными
# методом ajax c скриптом js/table_balance_currency.js
router.register('Balance_Currency', BalanceCurrency_ViewSet)

# табл БД News в blok2/models.py, News_ViewSet класс для обмена данными
# методом ajax c скриптом js/table_news.js
router.register('News', News_ViewSet)

# табл БД NewsImage в blok2/models.py, NewsImage_ViewSet класс для обмена данными
# методом ajax c скриптом js/table_newsimage.js
router.register('NewsImage', NewsImage_ViewSet)

# табл БД Exchange_List в blok2/models.py, ExchangeList_ViewSet класс для обмена данными
# методом ajax c скриптом js/table_exchange_list.js
router.register('Exchange_List', ExchangeList_ViewSet)

# этот справочник стал не нужен так как изменилась логика загрузки курсов валют
# табл БД Name_Currency_Trading в blok2/models.py, NameCurrencyTrading_ViewSet класс для обмена данными
# методом ajax c скриптом js/table_name_currency_trading.js
#router.register('Name_Currency_Trading', NameCurrencyTrading_ViewSet)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blok1.urls')),
    path('Kabinet/', include('blok2.urls')),
    path('api/', include(router.urls)), # для таблицы плагина datatables, api фрэмворка rest framework
    path('Obmen/', include('blok3.urls')),
    path('Poloniex/', include('blok4.urls')),
    re_path('celery-progress/', include('celery_progress.urls')), # для celeri progressbar

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
                 + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# Поиск медиа файлов по путям заданным в переменных STATIC_URL,STATIC_ROOT,MEDIA_URL,MEDIA_ROOT файла settings.py
