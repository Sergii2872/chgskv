from django.db import models

from django.db.models import Q
from model_utils import Choices

# Create your models here.
# Справочники валют для заполнения администратором
# Справочник торговых площадок(Бирж)
# Справочник наименования валют
# Справочник курсов валют
# Справочник остатков валют
# Справочник новостей
# Справочник фотографий(картинок) для новостей
# Справочник связей покупки-продажи валют

# для таблицы плагина datatables

#-----------------------------------------------------------------------------------------------------------------------
# сортировка колонок таблицы БД Market_Exchange
# выбор из списка по первому параметру значения второго параметра(изначально сортировка по полю ключа 1) для таблицы БД Name_Currency
ORDER_COLUMN_CHOICES_MarketExchange = Choices(
    ('0', ""),
    ('1', 'id'),
    ('2', 'market'),
    ('3', 'is_active'),
    ('4', 'created'),
    ('5', 'updated')
)

class Market_Exchange(models.Model):
    market = models.CharField(max_length=30, blank=True, null=True, default=None)  # название площадки(биржи)(здесь 1-Poloniex,2-Binance,3-Nomarket[фиатные валюты])
    is_active = models.BooleanField(default=False)  # Поле для включения(отключения) отображения записи
    created = models.DateTimeField(auto_now_add=True, auto_now=False)  # время создания записи
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)  # время изменения записи

# функция для класса MarketExchange_ViewSet и функции list в blok2/views.py
def query_market_exchange_by_args(**kwargs):
    draw = int(kwargs.get('draw', None)[0])
    length = int(kwargs.get('length', None)[0])
    start = int(kwargs.get('start', None)[0])
    search_value = kwargs.get('search[value]', None)[0]
    order_column = kwargs.get('order[0][column]', None)[0]
    order = kwargs.get('order[0][dir]', None)[0]

    order_column = ORDER_COLUMN_CHOICES_MarketExchange[order_column]
    #print("Значение kwargs order_column model1: ", order_column)
    # django orm '-' -> desc
    if order == 'desc':
        order_column = '-' + order_column

    queryset = Market_Exchange.objects.all()
    total = queryset.count()
    # класс Q применяется для использования логических элементов
    # & - логическое И (приоритет 2);
    # | - логическое ИЛИ (приоритет 3);
    # ~ - логическое НЕ (приоритет 1).
    # фильтрация таблицы по заданному поиску Search
    if search_value:
        queryset = queryset.filter(Q(id__icontains=search_value) |
                                   Q(market__icontains=search_value) |
                                   Q(is_active__icontains=search_value) |
                                   Q(created__icontains=search_value) |
                                   Q(updated__icontains=search_value))

    #print("Данные для таблицы отфильтрованные по поиску Search model2: ", queryset)
    #print("Поиск по: ", search_value)
    count = queryset.count()
    queryset = queryset.order_by(order_column)[start:start + length]
    #print("Данные для таблицы обработанные сериалайзером model3: ", queryset)
    return {
        'items': queryset,
        'count': count,
        'total': total,
        'draw': draw
    }

#-----------------------------------------------------------------------------------------------------------------------
# сортировка колонок таблицы БД Name_Currency
# выбор из списка по первому параметру значения второго параметра(изначально сортировка по полю ключа 1) для таблицы БД Name_Currency
ORDER_COLUMN_CHOICES_NameCurrency = Choices(
    ('0', ""),
    ('1', 'id'),
    ('2', 'market_exchange__market'),
    ('3', 'id_market'),
    ('4', 'currency'),
    ('5', 'symbol'),
    ('6', 'image_currency'),
    ('7', 'wallet'),
    ('8', 'is_active'),
    ('9', 'created'),
    ('10', 'updated')
)

class Name_Currency(models.Model):
    market_exchange = models.ForeignKey(Market_Exchange, on_delete=models.CASCADE, blank=True, null=True, default=None)  # Связка(ссылка) на таблицу БД справочника торговых площадок
    id_market = models.IntegerField(default=0)  # записываем в поле id валюты из торговой площадки(биржи)) (здесь 1-Poloniex,2-Binance,3-Nomarket[фиатные валюты])
    currency = models.CharField(max_length=50, blank=True, null=True, default=None)  # название валюты
    symbol = models.CharField(max_length=10, blank=True, null=True, default=None)  # тикер валюты(символ)
    image_currency = models.ImageField(upload_to='image_currency/', blank=True, null=True, max_length=255) # графич символ валюты
    wallet = models.CharField(max_length=80, blank=True, null=True, default=None)  # кошелек(счет) валюты
    is_active = models.BooleanField(default=False)  # Поле для включения(отключения) отображения записи
    created = models.DateTimeField(auto_now_add=True, auto_now=False)  # время создания записи
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)  # время изменения записи """

# функция для класса NameCurrency_ViewSet и функции list в blok2/views.py
def query_name_currency_by_args(**kwargs):
    draw = int(kwargs.get('draw', None)[0])
    length = int(kwargs.get('length', None)[0])
    start = int(kwargs.get('start', None)[0])
    search_value = kwargs.get('search[value]', None)[0]
    order_column = kwargs.get('order[0][column]', None)[0]
    order = kwargs.get('order[0][dir]', None)[0]

    order_column = ORDER_COLUMN_CHOICES_NameCurrency[order_column]
    #print("Значение kwargs order_column model1: ", order_column)
    # django orm '-' -> desc
    if order == 'desc':
        order_column = '-' + order_column

    queryset = Name_Currency.objects.all()
    total = queryset.count()
    # класс Q применяется для использования логических элементов
    # & - логическое И (приоритет 2);
    # | - логическое ИЛИ (приоритет 3);
    # ~ - логическое НЕ (приоритет 1).
    # фильтрация таблицы по заданному поиску Search
    if search_value:
        queryset = queryset.filter(Q(id__icontains=search_value) |
                                   Q(market_exchange__market__icontains=search_value) |
                                   Q(id_market__icontains=search_value) |
                                   Q(currency__icontains=search_value) |
                                   Q(symbol__icontains=search_value) |
                                   Q(image_currency__icontains=search_value) |
                                   Q(wallet__icontains=search_value) |
                                   Q(is_active__icontains=search_value) |
                                   Q(created__icontains=search_value) |
                                   Q(updated__icontains=search_value))

    #print("Данные для таблицы отфильтрованные по поиску Search model2: ", queryset)
    #print("Поиск по: ", search_value)
    count = queryset.count()
    queryset = queryset.order_by(order_column)[start:start + length]
    #print("Данные для таблицы обработанные сериалайзером model3: ", queryset)
    return {
        'items': queryset,
        'count': count,
        'total': total,
        'draw': draw
    }


#-----------------------------------------------------------------------------------------------------------------------
# сортировка колонок таблицы БД Fiat_Wallet
# выбор из списка по первому параметру значения второго параметра(изначально сортировка по полю ключа 1) для таблицы БД Fiat_Wallet
ORDER_COLUMN_CHOICES_FiatWallet = Choices(
    ('0', ""),
    ('1', 'id'),
    ('2', 'name_currency__symbol'),
    ('3', 'name_bank'),
    ('4', 'image_bank'),
    ('5', 'wallet_bank'),
    ('6', 'is_active'),
    ('7', 'created'),
    ('8', 'updated')
)

class Fiat_Wallet(models.Model):
    name_currency = models.ForeignKey(Name_Currency, on_delete=models.CASCADE, blank=True, null=True, default=None)  # Связка(ссылка) на таблицу БД справочника наименования валют
    name_bank = models.CharField(max_length=30, blank=True, null=True, default=None)  # название банка
    image_bank = models.ImageField(upload_to='image_bank/', blank=True, null=True, max_length=255) # графич символ банка
    wallet_bank = models.CharField(max_length=80, blank=True, null=True, default=None)  # кошелек(счет) валюты в банке
    is_active = models.BooleanField(default=False)  # Поле для включения(отключения) отображения записи
    created = models.DateTimeField(auto_now_add=True, auto_now=False)  # время создания записи
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)  # время изменения записи """

# функция для класса FiatWallet_ViewSet и функции list в blok2/views.py
def query_fiat_wallet_by_args(**kwargs):
    draw = int(kwargs.get('draw', None)[0])
    length = int(kwargs.get('length', None)[0])
    start = int(kwargs.get('start', None)[0])
    search_value = kwargs.get('search[value]', None)[0]
    order_column = kwargs.get('order[0][column]', None)[0]
    order = kwargs.get('order[0][dir]', None)[0]

    order_column = ORDER_COLUMN_CHOICES_FiatWallet[order_column]
    #print("Значение kwargs order_column model1: ", order_column)
    # django orm '-' -> desc
    if order == 'desc':
        order_column = '-' + order_column

    queryset = Fiat_Wallet.objects.all()
    total = queryset.count()
    # класс Q применяется для использования логических элементов
    # & - логическое И (приоритет 2);
    # | - логическое ИЛИ (приоритет 3);
    # ~ - логическое НЕ (приоритет 1).
    # фильтрация таблицы по заданному поиску Search
    if search_value:
        queryset = queryset.filter(Q(id__icontains=search_value) |
                                   Q(name_currency__symbol__icontains=search_value) |
                                   Q(name_bank__icontains=search_value) |
                                   Q(image_bank__icontains=search_value) |
                                   Q(wallet_bank__icontains=search_value) |
                                   Q(is_active__icontains=search_value) |
                                   Q(created__icontains=search_value) |
                                   Q(updated__icontains=search_value))

    #print("Данные для таблицы отфильтрованные по поиску Search model2: ", queryset)
    #print("Поиск по: ", search_value)
    count = queryset.count()
    queryset = queryset.order_by(order_column)[start:start + length]
    #print("Данные для таблицы обработанные сериалайзером model3: ", queryset)
    return {
        'items': queryset,
        'count': count,
        'total': total,
        'draw': draw
    }



#-----------------------------------------------------------------------------------------------------------------------
# сортировка колонок таблицы БД Prices_Currency
# выбор из списка по первому параметру значения второго параметра(изначально сортировка по полю ключа 1) для таблицы БД Prices_Currency
ORDER_COLUMN_CHOICES_PricesCurrency = Choices(
    ('0', ""),
    ('1', 'id'),
    ('2', 'name_currency__symbol'),
    ('3', 'name_currency_sale_id'),
    ('4', 'name_currency_sale_currency'),
    ('5', 'min_buy'),
    ('6', 'max_buy'),
    ('7', 'kurs_sell'),
    ('8', 'id_pair_market'),
    ('9', 'is_active'),
    ('10', 'created'),
    ('11', 'updated')

)

# Справочник курсов пары валют с привязкой к торговой площадке (здесь market_exchange = 1-Poloniex,2-Binance,3-Nomarket)
class Prices_Currency(models.Model):
    market_exchange = models.ForeignKey(Market_Exchange, on_delete=models.CASCADE, blank=True, null=True, default=3)  # Связка(ссылка) на таблицу БД справочника торговых площадок
    name_currency = models.ForeignKey(Name_Currency, on_delete=models.CASCADE, blank=True, null=True, default=None) # Связка(ссылка) на таблицу БД справочника наименования валют
    name_currency_sale_id = models.IntegerField(default=0)  # для покупаемой валюты name_currency продаем валюту(записываем в поле id валюты)
    name_currency_sale_currency = models.CharField(max_length=50, blank=True, null=True, default=None)  # для покупаемой валюты name_currency продаем валюту(записываем в поле наименование валюты)
    min_buy = models.DecimalField(max_digits=20, decimal_places=5, default=0)  # минимальная сумма покупки валюты
    max_buy = models.DecimalField(max_digits=20, decimal_places=5, default=0)  # максимальная сумма покупки валюты
    kurs_sell = models.DecimalField(max_digits=30, decimal_places=10, default=0) # курс продажи
    id_pair_market = models.IntegerField(default=0)  # записываем в поле если есть id пары валют из торговой площадки(биржи)
    is_active = models.BooleanField(default=False)  # Поле для включения(отключения) отображения записи
    created = models.DateTimeField(auto_now_add=True, auto_now=False)  # время создания записи
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)  # время изменения записи

# функция для класса PricesCurrency_ViewSet и функции list в blok2/views.py
def query_prices_currency_by_args(**kwargs):
    draw = int(kwargs.get('draw', None)[0])
    length = int(kwargs.get('length', None)[0])
    start = int(kwargs.get('start', None)[0])
    search_value = kwargs.get('search[value]', None)[0] # переменная значения поиска Search
    order_column = kwargs.get('order[0][column]', None)[0]
    order = kwargs.get('order[0][dir]', None)[0]

    order_column = ORDER_COLUMN_CHOICES_PricesCurrency[order_column]
    #print("Значение kwargs order_column model1: ", order_column)
    #print("Значение kwargs search_value model1: ", order)
    # django orm '-' -> desc
    if order == 'desc':
        order_column = '-' + order_column

    queryset = Prices_Currency.objects.all()
    total = queryset.count()
    # класс Q применяется для использования логических элементов, фильтр применяется для поиска в таблице
    # & - логическое И (приоритет 2);
    # | - логическое ИЛИ (приоритет 3);
    # ~ - логическое НЕ (приоритет 1).
    # фильтрация таблицы по заданному поиску Search
    if search_value:
        queryset = queryset.filter(Q(id__icontains=search_value) |
                                   Q(min_buy__icontains=search_value) |
                                   Q(max_buy__icontains=search_value) |
                                   Q(kurs_sell__icontains=search_value) |
                                   Q(id_pair_market__icontains=search_value) |
                                   Q(is_active__icontains=search_value) |
                                   Q(created__icontains=search_value) |
                                   Q(updated__icontains=search_value) |
                                   Q(name_currency_sale_id__icontains=search_value) |
                                   Q(name_currency_sale_currency__icontains=search_value) |
                                   Q(market_exchange__market__icontains=search_value) |
                                   Q(name_currency__currency__icontains=search_value)) # поиск по полю currency БД name_currency

    #print("Данные для таблицы отфильтрованные по поиску Search model2: ", queryset.values())
    #print("Поиск по: ", search_value)
    count = queryset.count()
    queryset = queryset.order_by(order_column)[start:start + length] # сортировка
    #print("Данные для таблицы обработанные сериалайзером model3: ", queryset.values())
    return {
        'items': queryset,
        'count': count,
        'total': total,
        'draw': draw
    }

#-----------------------------------------------------------------------------------------------------------------------
# сортировка колонок таблицы БД Balance_Currency
# выбор из списка по первому параметру значения второго параметра(изначально сортировка по полю ключа 1) для таблицы БД Balance_Currency
ORDER_COLUMN_CHOICES_BalanceCurrency = Choices(
    ('0', ""),
    ('1', 'id'),
    ('2', 'name_currency__symbol'),
    ('3', 'balance_amount'),
    ('4', 'is_active'),
    ('5', 'created'),
    ('6', 'updated')

)

# Справочник остатков валют
class Balance_Currency(models.Model):
    name_currency = models.ForeignKey(Name_Currency, on_delete=models.CASCADE, blank=True, null=True, default=None) # Связка(ссылка) на таблицу БД справочника наименования валют
    balance_amount = models.DecimalField(max_digits=30, decimal_places=10, default=0) # сумма остатка валюты(резерв)
    is_active = models.BooleanField(default=False)  # Поле для включения(отключения) отображения записи
    created = models.DateTimeField(auto_now_add=True, auto_now=False)  # время создания записи
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)  # время изменения записи

# функция для класса PricesCurrency_ViewSet и функции list в blok2/views.py
def query_balance_currency_by_args(**kwargs):
    draw = int(kwargs.get('draw', None)[0])
    length = int(kwargs.get('length', None)[0])
    start = int(kwargs.get('start', None)[0])
    search_value = kwargs.get('search[value]', None)[0] # переменная значения поиска Search
    order_column = kwargs.get('order[0][column]', None)[0]
    order = kwargs.get('order[0][dir]', None)[0]

    order_column = ORDER_COLUMN_CHOICES_BalanceCurrency[order_column]
    #print("Значение kwargs order_column model1: ", order_column)
    #print("Значение kwargs search_value model1: ", order)
    # django orm '-' -> desc
    if order == 'desc':
        order_column = '-' + order_column

    queryset = Balance_Currency.objects.all()
    total = queryset.count()
    # класс Q применяется для использования логических элементов, фильтр применяется для поиска в таблице
    # & - логическое И (приоритет 2);
    # | - логическое ИЛИ (приоритет 3);
    # ~ - логическое НЕ (приоритет 1).
    # фильтрация таблицы по заданному поиску Search
    if search_value:
        queryset = queryset.filter(Q(id__icontains=search_value) |
                                   Q(balance_amount__icontains=search_value) |
                                   Q(min_buy__icontains=search_value) |
                                   Q(max_buy__icontains=search_value) |
                                   Q(is_active__icontains=search_value) |
                                   Q(created__icontains=search_value) |
                                   Q(updated__icontains=search_value) |
                                   Q(name_currency__symbol__icontains=search_value)) # поиск по полю symbol БД name_currency

    #print("Данные для таблицы отфильтрованные по поиску Search model2: ", queryset.values())
    #print("Поиск по: ", search_value)
    count = queryset.count()
    queryset = queryset.order_by(order_column)[start:start + length] # сортировка
    #print("Данные для таблицы обработанные сериалайзером model3: ", queryset.values())
    return {
        'items': queryset,
        'count': count,
        'total': total,
        'draw': draw
    }

#-----------------------------------------------------------------------------------------------------------------------
# Справочник связей покупки-продажи валют
# сортировка колонок таблицы БД Name_Currency_Trading
# выбор из списка по первому параметру значения второго параметра(изначально сортировка по полю ключа 1) для таблицы БД Name_Currency_Trading
# справочник стал не нужен так как изменилась логика курсов валют, поля 3,4,5 перешли в таблицу курсов валют
"""
ORDER_COLUMN_CHOICES_NameCurrencyTrading = Choices(
    ('0', ""),
    ('1', 'id'),
    ('2', 'name_currency__currency'),
    ('3', 'name_currency_sale_id'),
    ('4', 'name_currency_sale_currency'),
    ('5', 'id_pair_market'),
    ('6', 'is_active'),
    ('7', 'created'),
    ('8', 'updated')
)

class Name_Currency_Trading(models.Model):
    name_currency = models.ForeignKey(Name_Currency, on_delete=models.CASCADE, blank=True, null=True, default=None)  # Связка(ссылка) на таблицу БД справочника наименования валют
    name_currency_sale_id = models.IntegerField(default=0) # для покупаемой валюты name_currency продаем валюту(записываем в поле id валюты)
    name_currency_sale_currency = models.CharField(max_length=30, blank=True, null=True, default=None)  # # для покупаемой валюты name_currency продаем валюту(записываем в поле наименование валюты)
    id_pair_market = models.IntegerField(default=0)  # записываем в поле id пары валют из торговой площадки(биржи))
    is_active = models.BooleanField(default=False)  # Поле для включения(отключения) отображения записи
    created = models.DateTimeField(auto_now_add=True, auto_now=False)  # время создания записи
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)  # время изменения записи

# функция для класса NameCurrencyTrading_ViewSet и функции list в blok2/views.py
def query_name_currency_trading_by_args(**kwargs):
    draw = int(kwargs.get('draw', None)[0])
    length = int(kwargs.get('length', None)[0])
    start = int(kwargs.get('start', None)[0])
    search_value = kwargs.get('search[value]', None)[0]
    order_column = kwargs.get('order[0][column]', None)[0]
    order = kwargs.get('order[0][dir]', None)[0]

    order_column = ORDER_COLUMN_CHOICES_NameCurrencyTrading[order_column]
    #print("Значение kwargs order_column model1: ", order_column)
    # django orm '-' -> desc
    if order == 'desc':
        order_column = '-' + order_column

    queryset = Name_Currency_Trading.objects.all()
    total = queryset.count()
    # класс Q применяется для использования логических элементов
    # & - логическое И (приоритет 2);
    # | - логическое ИЛИ (приоритет 3);
    # ~ - логическое НЕ (приоритет 1).
    # фильтрация таблицы по заданному поиску Search
    if search_value:
        queryset = queryset.filter(Q(id__icontains=search_value) |
                                   Q(name_currency__currency__icontains=search_value) |
                                   Q(name_currency_sale_id__icontains=search_value) |
                                   Q(name_currency_sale_currency__icontains=search_value) |
                                   Q(id_pair_market__icontains=search_value) |
                                   Q(is_active__icontains=search_value) |
                                   Q(created__icontains=search_value) |
                                   Q(updated__icontains=search_value))

    #print("Данные для таблицы отфильтрованные по поиску Search model2: ", queryset)
    #print("Поиск по: ", search_value)
    count = queryset.count()
    queryset = queryset.order_by(order_column)[start:start + length]
    #print("Данные для таблицы обработанные сериалайзером model3: ", queryset)
    return {
        'items': queryset,
        'count': count,
        'total': total,
        'draw': draw
    }
"""

#-----------------------------------------------------------------------------------------------------------------------
# сортировка колонок таблицы БД News
# выбор из списка по первому параметру значения второго параметра(изначально сортировка по полю ключа 1) для таблицы БД News
ORDER_COLUMN_CHOICES_News = Choices(
    ('0', ""),
    ('1', 'id'),
    ('3', 'header'),
    ('4', 'news'),
    ('5', 'is_active'),
    ('6', 'created'),
    ('7', 'updated')

)


# Справочник новостей
class News(models.Model):
    header = models.CharField(max_length=80, blank=True, null=True, default=None)  # заголовок новости
    news = models.TextField(blank=True, null=True, default=None) # новость
    is_active = models.BooleanField(default=True) # Поле для включения,отключения отображения записи
    created = models.DateTimeField(auto_now_add=True, auto_now=False) # время создания
    updated = models.DateTimeField(auto_now_add=False, auto_now=True) # время изменения

# функция для класса News_ViewSet и функции list в blok2/views.py
def query_news_by_args(**kwargs):
    draw = int(kwargs.get('draw', None)[0])
    length = int(kwargs.get('length', None)[0])
    start = int(kwargs.get('start', None)[0])
    search_value = kwargs.get('search[value]', None)[0] # переменная значения поиска Search
    order_column = kwargs.get('order[0][column]', None)[0]
    order = kwargs.get('order[0][dir]', None)[0]

    order_column = ORDER_COLUMN_CHOICES_News[order_column]
    #print("Значение kwargs order_column model1: ", order_column)
    #print("Значение kwargs search_value model1: ", order)
    # django orm '-' -> desc
    if order == 'desc':
        order_column = '-' + order_column

    queryset = News.objects.all()
    total = queryset.count()
    # класс Q применяется для использования логических элементов, фильтр применяется для поиска в таблице
    # & - логическое И (приоритет 2);
    # | - логическое ИЛИ (приоритет 3);
    # ~ - логическое НЕ (приоритет 1).
    # фильтрация таблицы по заданному поиску Search
    if search_value:
        queryset = queryset.filter(Q(id__icontains=search_value) |
                                   Q(header__icontains=search_value) |
                                   Q(news__icontains=search_value) |
                                   Q(is_active__icontains=search_value) |
                                   Q(created__icontains=search_value) |
                                   Q(updated__icontains=search_value))


    #print("Данные для таблицы отфильтрованные по поиску Search model2: ", queryset.values())
    #print("Поиск по: ", search_value)
    count = queryset.count()
    queryset = queryset.order_by(order_column)[start:start + length] # сортировка
    #print("Данные для таблицы обработанные сериалайзером model3: ", queryset.values())
    return {
        'items': queryset,
        'count': count,
        'total': total,
        'draw': draw
    }

#-----------------------------------------------------------------------------------------------------------------------
# сортировка колонок таблицы БД NewsImage
# выбор из списка по первому параметру значения второго параметра(изначально сортировка по полю ключа 1) для таблицы БД NewsImage
ORDER_COLUMN_CHOICES_NewsImage = Choices(
    ('0', ""),
    ('1', 'id'),
    ('2', 'to_news__header'),
    ('3', 'image'),
    ('4', 'is_main'),
    ('5', 'is_active'),
    ('6', 'created'),
    ('7', 'updated')

)

# Справочник фотографий(картинок) для новостей
class NewsImage(models.Model):
    to_news = models.ForeignKey(News, on_delete=models.CASCADE, blank=True, null=True, default=None) # Связка(ссылка) на таблицу БД новостей News
    image = models.ImageField(upload_to='news_images/', null=True, max_length=255) # "pip install Pillow" , поле для картинок товаров
    is_main = models.BooleanField(default=False) # Включение картинки как главной
    is_active = models.BooleanField(default=True) # Поле для включения,отключения отображения записи
    created = models.DateTimeField(auto_now_add=True, auto_now=False) # время создания
    updated = models.DateTimeField(auto_now_add=False, auto_now=True) # время изменения

    #def __str__(self):
    #    return "Фото {}".format(self.image)

    #class Meta:
    #    verbose_name = 'Фото для главной'
    #    verbose_name_plural = 'Картинки для главной'

# функция для класса NewsImage_ViewSet и функции list в blok2/views.py
def query_newsimage_by_args(**kwargs):
    draw = int(kwargs.get('draw', None)[0])
    length = int(kwargs.get('length', None)[0])
    start = int(kwargs.get('start', None)[0])
    search_value = kwargs.get('search[value]', None)[0] # переменная значения поиска Search
    order_column = kwargs.get('order[0][column]', None)[0]
    order = kwargs.get('order[0][dir]', None)[0]

    order_column = ORDER_COLUMN_CHOICES_NewsImage[order_column]
    #print("Значение kwargs order_column model1: ", order_column)
    #print("Значение kwargs search_value model1: ", order)
    # django orm '-' -> desc
    if order == 'desc':
        order_column = '-' + order_column

    queryset = NewsImage.objects.all()
    total = queryset.count()
    # класс Q применяется для использования логических элементов, фильтр применяется для поиска в таблице
    # & - логическое И (приоритет 2);
    # | - логическое ИЛИ (приоритет 3);
    # ~ - логическое НЕ (приоритет 1).
    # фильтрация таблицы по заданному поиску Search
    if search_value:
        queryset = queryset.filter(Q(id__icontains=search_value) |
                                   Q(to_news__header__icontains=search_value) |
                                   Q(image__icontains=search_value) |
                                   Q(is_main__icontains=search_value) |
                                   Q(is_active__icontains=search_value) |
                                   Q(created__icontains=search_value) |
                                   Q(updated__icontains=search_value))

    print("Данные для таблицы отфильтрованные по поиску Search model2: ", queryset.values())
    #print("Поиск по: ", search_value)
    count = queryset.count()
    queryset = queryset.order_by(order_column)[start:start + length] # сортировка
    print("Данные для таблицы обработанные сериалайзером model3: ", queryset.values())
    return {
        'items': queryset,
        'count': count,
        'total': total,
        'draw': draw
    }

#-----------------------------------------------------------------------------------------------------------------------
# сортировка колонок таблицы БД Exchange_List
# выбор из списка по первому параметру значения второго параметра(изначально сортировка по полю ключа 1) для таблицы БД Exchange_List
ORDER_COLUMN_CHOICES_ExchangeList = Choices(
    ('0', ""),
    ('1', 'id'),
    ('2', 'id_user'),
    ('3', 'id_pair_market'),
    ('4', 'name_currency_buy_id'),
    ('5', 'name_currency_buy_currency'),
    ('6', 'sum_currency_buy'),
    ('7', 'wallet_currency_buy'),
    ('8', 'name_currency_sell_id'),
    ('9', 'name_currency_sell_currency'),
    ('10', 'sum_currency_sell'),
    ('11', 'wallet_currency_sell'),
    ('12', 'kurs_sell'),
    ('13', 'kurs_buy_fact'),
    ('14', 'sum_currency_buy_fact'),
    ('15', 'wallet_fact'),
    ('16', 'status'),
    ('17', 'is_active'),
    ('18', 'created'),
    ('19', 'updated')

)

# Реестр заявок на обмен
class Exchange_List(models.Model):
    id_user = models.IntegerField(default=0)  # id клиента
    id_pair_market = models.IntegerField(default=0)  # записываем в поле id пары валют из торговой площадки(биржи)) покупки-продажи
    name_currency_buy_id = models.IntegerField(default=0)  # id покупаемой валюты у клиента
    name_currency_buy_currency = models.CharField(max_length=50, blank=True, null=True, default=None)  # наименование покупаемой валюты у клиента
    sum_currency_buy = models.DecimalField(max_digits=30, decimal_places=10, default=0)  # сумма покупки валюты у клиента
    wallet_currency_buy = models.CharField(max_length=80, blank=True, null=True, default=None)  # кошелек(счет) с которго клиент отдает валюту
    name_currency_sell_id = models.IntegerField(default=0)  # id продаваемой валюты клиенту
    name_currency_sell_currency = models.CharField(max_length=50, blank=True, null=True, default=None)  # наименование продаваемой валюты клиенту
    sum_currency_sell = models.DecimalField(max_digits=30, decimal_places=10, default=0)  # сумма продажи валюты клиенту
    wallet_currency_sell = models.CharField(max_length=80, blank=True, null=True, default=None)  # кошелек(счет) на который клиент получает валюту
    kurs_sell = models.DecimalField(max_digits=30, decimal_places=10, default=0)  # курс продажи валюты клиенту
    kurs_buy_fact = models.DecimalField(max_digits=30, decimal_places=10, default=0)  # курс фактический покупки валюты клиенту
    sum_currency_buy_fact = models.DecimalField(max_digits=30, decimal_places=10, default=0)  # сумма за которую фактически купили валюту для клиента
    wallet_fact = models.CharField(max_length=80, blank=True, null=True, default=None)  # кошелек(счет) на который клиент переводит валюту для покупки на бирже(мой кошелек)
    status = models.IntegerField(default=0)  # статус заявки(0-аннулирована,1-принята,2-исполнена)
    is_active = models.BooleanField(default=False)  # Поле для включения(отключения) отображения записи
    created = models.DateTimeField(auto_now_add=True, auto_now=False)  # время создания записи
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)  # время изменения записи

# функция для класса PricesCurrency_ViewSet и функции list в blok2/views.py
def query_exchange_list_by_args(**kwargs):
    draw = int(kwargs.get('draw', None)[0])
    length = int(kwargs.get('length', None)[0])
    start = int(kwargs.get('start', None)[0])
    search_value = kwargs.get('search[value]', None)[0] # переменная значения поиска Search
    order_column = kwargs.get('order[0][column]', None)[0]
    order = kwargs.get('order[0][dir]', None)[0]

    order_column = ORDER_COLUMN_CHOICES_ExchangeList[order_column]
    #print("Значение kwargs order_column model1: ", order_column)
    #print("Значение kwargs search_value model1: ", order)
    # django orm '-' -> desc
    if order == 'desc':
        order_column = '-' + order_column

    queryset = Exchange_List.objects.all()
    total = queryset.count()
    # класс Q применяется для использования логических элементов, фильтр применяется для поиска в таблице
    # & - логическое И (приоритет 2);
    # | - логическое ИЛИ (приоритет 3);
    # ~ - логическое НЕ (приоритет 1).
    # фильтрация таблицы по заданному поиску Search
    if search_value:
        queryset = queryset.filter(Q(id__icontains=search_value) |
                                   Q(id_user__icontains=search_value) |
                                   Q(id_pair_market__icontains=search_value) |
                                   Q(name_currency_buy_id__icontains=search_value) |
                                   Q(name_currency_buy_currency__icontains=search_value) |
                                   Q(sum_currency_buy__icontains=search_value) |
                                   Q(wallet_currency_buy__icontains=search_value) |
                                   Q(name_currency_sell_id__icontains=search_value) |
                                   Q(name_currency_sell_currency__icontains=search_value) |
                                   Q(sum_currency_sell__icontains=search_value) |
                                   Q(wallet_currency_sell__icontains=search_value) |
                                   Q(kurs_sell__icontains=search_value) |
                                   Q(kurs_buy_fact__icontains=search_value) |
                                   Q(sum_currency_buy_fact__icontains=search_value) |
                                   Q(wallet_fact__icontains=search_value) |
                                   Q(status__icontains=search_value) |
                                   Q(is_active__icontains=search_value) |
                                   Q(created__icontains=search_value) |
                                   Q(updated__icontains=search_value))


    #print("Данные для таблицы отфильтрованные по поиску Search model2: ", queryset.values())
    #print("Поиск по: ", search_value)
    count = queryset.count()
    queryset = queryset.order_by(order_column)[start:start + length] # сортировка
    #print("Данные для таблицы обработанные сериалайзером model3: ", queryset.values())
    return {
        'items': queryset,
        'count': count,
        'total': total,
        'draw': draw
    }

