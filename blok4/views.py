from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from blok2.models import Name_Currency, Prices_Currency, Balance_Currency, Exchange_List    # , Name_Currency_Trading эту таблицу не использую так как изменилась логика курсов валют
from decimal import Decimal

# Пакет для работы с API биржи Poloniex
# инициализация pip install poloniex
from poloniex import Poloniex
from django.conf import settings

import datetime
import sys
import getopt
import time
from datetime import datetime
import json
import os

# пакет для progress bar  https://pysimplegui.readthedocs.io/en/latest/#pysimplegui-users-manual
import PySimpleGUI as sg

# пример progress bar(показывает в терминале pycharm, на фронте не виден)  https://habr.com/ru/post/483400/
# https://github.com/verigak/progress/  pip install progress
from progress.bar import IncrementalBar


# пакет для celeri progress bar  https://github.com/czue/celery-progress
# для windows чтоб не вылетала в celery ошибка делаем pip install gevent
# запускаем сервер redis redis-server.exe
# и запускаем celery командой celery -A chgskv worker -l info -P gevent
from celery import shared_task # pip install celery
from celery_progress.backend import ProgressRecorder # pip install celery-progress

# для отправки телеграмм сообщений пакета django-sitemessage
# https://django-sitemessage.readthedocs.io/en/stable/toolbox.html
from sitemessage.toolbox import send_scheduled_messages

# Telegram сообщения
# Пакет https://pypi.org/project/django-sitemessage/
# pip install django-sitemessage
# добавляем приложение sitemessage application to INSTALLED_APPS in your settings file ‘settings.py’
# создаем таблицы БД приложения python manage.py migrate
# отправка сообщения python manage.py sitemessage_send_scheduled (периодически запускать в cron, celery или др. обработчике)
from sitemessage.toolbox import register_messenger_objects, schedule_messages, recipients
from sitemessage.messengers.telegram import TelegramMessenger
# Конфигурируем посыльного Telegram.
# `bot_token` - это токен, полученный при создании телеграм-бота.(задаем в settings.py)
# https://pythonz.net/articles/48/
# https://django-sitemessage.readthedocs.io/en/latest/quickstart.html
register_messenger_objects(TelegramMessenger(settings.BOT_TOKEN))


# Create your views here.

# --------------- Функция периодического выполнения celery отправки сообщений в телеграмм( пакет django-sitemessage, https://pypi.org/project/django-sitemessage/)
@shared_task
def telegram_message():
    print("обработка сообщений телеграмм")
    send_scheduled_messages(ignore_unknown_messengers=True, ignore_unknown_message_types=True) # отправка сообщений боту телеграмм(напрямую из представления без python manage.py sitemessage_send_scheduled)
    #os.system("./manage.py sitemessage_send_scheduled") # запускаем обработчик сообщений боту телеграмм



# --------------- блок загрузки валют биржи Poloniex --------------------------------------------------------------
# Функция для загрузки валют биржи Poloniex
# Пакет для работы с API биржи Poloniex
# инициализация pip install poloniex(https://pypi.org/project/poloniex/)
def Load_Poloniex_NameCurrency(request):

    # Poloniex Api
    #polo = Poloniex()
    #help(polo)

    api_key = settings.POLONIEX_API_KEY
    api_secret = settings.POLONIEX_SECRET
    polo = Poloniex(api_key, api_secret)
    #help(polo) # описание функционала

    #ticker = polo.returnTicker()['BTC_ETH']
    #print(ticker)

    #balances = polo.returnBalances()
    #print(balances)

    #depo_acc = polo.returnDepositAddresses()['DOGE']
    #print(depo_acc)
    # tik = polo.return24hVolume()

    # котировки
    #quotation = polo.returnTicker()
    # валюты
    currencies = polo.returnCurrencies()

    #order = polo.returnLoanOrders('TRX')
    #print(tik)


    return render(request, 'load_poloniex_namecurrencys.html', locals()) #  {'task_id' : task.task_id, 'currencies' :currencies}

# Загрузка валют биржи Poloniex с отображением celery progress bar
@shared_task(bind=True)
def my_task(self, seconds):
    progress_recorder = ProgressRecorder(self) # celery progress bar
    l = 0  # итератор для progress bar
    i = 0  # индикатор
    result_add_currency_poloniex = 0 # переменная результат добавленных новых валют
    result_active_currency_poloniex = 0 # переменная результат активированных которые уже есть в БД валют
    result_delete_currency_poloniex = 0 # переменная результат удаленных валют из БД (на Poloniex больше не торгуются)
    return_dict = dict()  # переменную return_dict определяем как словарь
    # валюты
    #  # API биржи Poloniex
    # help(polo)
    # api ключи Poloniex в settings.py
    api_key = settings.POLONIEX_API_KEY
    api_secret = settings.POLONIEX_SECRET
    polo = Poloniex(api_key, api_secret)
    #polo = Poloniex()
    currencies = polo.returnCurrencies()  # получаем словарь криптовалют с биржи Poloniex
    count_progressbar = len(currencies.items())  # количество элементов в словаре
    print(count_progressbar)
    namecurrences = Name_Currency.objects.all()  # валюты справочника валют
    for key, value in currencies.items():  # проходим по полученному словарю криптовалют Poloniex
        if value["delisted"] == 0:  # если валюта не исключена из списка биржи
            # генерируем адрес кошелька с помощью api Poloniex
            adres = polo.generateNewAddress(key)
            if adres["success"] == 0:
                adres = adres["response"]
                adres = adres[adres.find(':') - len(adres) + 2:] # выделяем из строки адрес
                print(adres)
            else:
                adres = ""
                print(adres)
            for namecurrence in namecurrences:  # проходим по нашему справочнику валют
                # и если такая валюта(символ) есть и она не активна и совпадают id из биржи и эта валюта принадлежит Poloniex(поле market_exchange_id=1)
                if key == namecurrence.symbol and namecurrence.is_active == False and value["id"] == namecurrence.id_market and namecurrence.market_exchange_id == 1:
                    print("такая валюта есть но не активна, то редактируем поля и делаем активной")
                    name_currency = Name_Currency.objects.get(symbol=key)  # находим запись по символу равному символу валюты биржи
                    # то делаем эту валюту активной и обновляем дату, перезаписываем значение полей
                    name_currency.is_active = True
                    name_currency.wallet = adres
                    name_currency.updated = datetime
                    name_currency.save()
                    i = 1  # такая валюта есть то устанавливаем индикатор в 1
                    result_active_currency_poloniex += 1
                # если такая валюта(символ) есть и она активна и совпадают id из биржи и эта валюта принадлежит Poloniex(поле market_exchange_id=1)
                if key == namecurrence.symbol and namecurrence.is_active == True and value["id"] == namecurrence.id_market and namecurrence.market_exchange_id == 1:
                    print("такая валюта уже есть")
                    i = 1  # такая валюта есть то устанавливаем индикатор в 1
            if i == 0:
                print("такой валюты нет, добавляем ее")
                # market_exchange_id=1, где 1 это id биржи Poloniex в БД площадок(бирж)(при заполнении справочника под id=1 обязательно пишем Poloniex!!!)
                name_currency = Name_Currency.objects.create(market_exchange_id=1, id_market=value["id"],
                                                             currency=value["name"], symbol=key,
                                                             image_currency="image_currency/noimage.png", # ставим иконку начальную чтоб не было ошибки пустого поля
                                                             wallet=adres, is_active=True, # wallet=value["depositAddress"] заменил на генерацию адреса депозита
                                                             created=datetime, updated=datetime)
                result_add_currency_poloniex += 1

        if value["delisted"] == 1:  # если валюта исключена из списка биржи
            for namecurrence in namecurrences:  # проходим по нашему справочнику валют
                # если такая валюта(символ) есть и она активна и совпадают id из биржи и эта валюта принадлежит Poloniex(поле market_exchange_id=1)
                if key == namecurrence.symbol and namecurrence.is_active == True and value["id"] == namecurrence.id_market and namecurrence.market_exchange_id == 1:
                    print("такая валюта есть и она активна, то делаем ее не активной")
                    name_currency = Name_Currency.objects.get(symbol=key)  # находим запись по символу равному символу валюты биржи
                    # то делаем эту валюту не активной и обновляем дату, перезаписываем значения
                    name_currency.is_active = False
                    name_currency.updated = datetime
                    name_currency.save()
                    result_delete_currency_poloniex += 1

        i = 0  # для следующей итерации устанавливаем индикатор в 0
        time.sleep(0.1) # для задержки итераций прогрессбара и цикла
        l += 1
        progress_recorder.set_progress(l, count_progressbar) # celery progress bar

    return_dict["result_add_currency_poloniex"] = result_add_currency_poloniex
    return_dict["result_active_currency_poloniex"] = result_active_currency_poloniex
    return_dict["result_delete_currency_poloniex"] = result_delete_currency_poloniex

    # отправляем сообщение о заявке в телеграмм
    # Ставим сообщение в очередь.
    # узнать свой id , в телеграмм набрать get my id, затем /start
    # Оно будет отослано моему боту в переписку (чат) с ID 1156354914.
    # отправка сообщения python manage.py sitemessage_send_scheduled (периодически запускать в cron, celery или др. обработчике)
    # в админке настраиваем Periodic tasks
    schedule_messages('Справочник валют Poloniex обновлен! ' +
                      ' Новых криптовалют: ' + str(result_add_currency_poloniex) +
                      ' Вновь активировано криптовалют: ' + str(result_active_currency_poloniex) +
                      ' Удалено криптовалют: ' + str(result_delete_currency_poloniex)
                      , recipients('telegram', '1156354914'))

    return return_dict


# не использую
# Загрузка валют с биржи Poloniex , процесс загрузки выполняем в функции my_task
# асинхронным методом celery с индикатором загрузки progress bar
def Load_Poloniex_Currencies(request):
    #response_data = dict()  # переменную response_data определяем как словарь
    print("Загрузка криптовалют с Poloniex")
    print("post запрос в Load_Poloniex_Currencies от load_poloniex_currency.html по action")
    data = request.POST  # переменной data присваиваем значение post запроса
    print(data)  # выводим значение post запроса в терминале питона для проверки
    csrfm = data.get("csrfmiddlewaretoken")
    print(csrfm)
    if request.method == 'POST':
        result = my_task.delay(1)   # функция my_task загрузка валют биржи Poloniex с celery progress bar
        print("Celery my_task: ", result) # id задание для celery

        # для ajax
        #response_data = {
        #'state': result.state,
        #'details': result.info,
        #}

    return render(request, 'result_poloniex_namecurrency.html', {'task_id': result.task_id}) #, 'result': return_dict

    # пример progress bar celery для возврата по ajax https://buildwithdjango.com/blog/post/celery-progress-bars/
    #return HttpResponse(json.dumps(response_data), content_type='application/json')

    #return JsonResponse({"data": return_dict})

#----------------------------------------------------------------------------------------------------------------------



# --------------- блок загрузки пар валют биржи Poloniex --------------------------------------------------------------
# Функция для загрузки пар валют биржи Poloniex
# Пакет для работы с API биржи Poloniex
# инициализация pip install poloniex(https://pypi.org/project/poloniex/)
"""
# этот блок стал не нужен так как изменилась логика загрузки курсов валют и изменилась таблица бд курсов валют(в таблице добавлены поля продаваемой валюты)
def Load_Poloniex_PairCurrency(request):

    api_key = settings.POLONIEX_API_KEY
    api_secret = settings.POLONIEX_SECRET
    polo = Poloniex(api_key, api_secret)
    #help(polo) # описание функционала

    # котировки
    quotation = polo.returnTicker()



    return render(request, 'load_poloniex_paircurrencys.html', locals())


# Загрузка пар валют биржи Poloniex с отображением celery progress bar
@shared_task(bind=True)
def my_task_pair(self, seconds):
    progress_recorder = ProgressRecorder(self) # celery progress bar
    l = 0  # итератор для progress bar
    i = 0  # индикатор
    result_add_paircurrency_poloniex = 0  # переменная результат добавленных новых пар валют
    result_active_paircurrency_poloniex = 0  # переменная результат активированных которые уже есть в БД пар валют
    result_delete_paircurrency_poloniex = 0  # переменная результат удаленных пар валют из БД (на Poloniex больше не торгуются)
    return_dict = dict()  # переменную return_dict определяем как словарь
    # валюты
    polo = Poloniex()  # API биржи Poloniex
    currencies_pair = polo.returnTicker()  # получаем словарь котировок пар криптовалют с биржи Poloniex
    count_progressbar = len(currencies_pair.items())  # количество элементов в словаре
    print(count_progressbar)
    namecurrences_trading = Name_Currency_Trading.objects.all()  # валютные пары справочника валют
    for key, value in currencies_pair.items():  # проходим по полученному словарю пар криптовалют Poloniex
        if value["isFrozen"] == 0:  # если валюная пара торгуется в настоящее время на бирже
            currency_buy = key[:key.find('_')]  # покупаем у клиента валюту
            currency_sell = key[key.find('_') - len(key) + 1:]  # продаем клиенту валюту
            name_currency_buy = Name_Currency.objects.get(symbol=currency_buy, is_active=True)  # находим запись в справочнике валют по символу равному символу покупаемой у клиента валюты
            name_currency_sell = Name_Currency.objects.get(symbol=currency_sell, is_active=True)  # находим запись в справочнике валют по символу равному символу продаваемой клиенту валюты
            for namecurrence_trading in namecurrences_trading:  # проходим по нашему справочнику пар валют
                # если id пары биржи Poloniex равно id пары в справочнике пар и эта пара не активна и покупаемая валюта у клиента есть в справочнике валют(она активна) и продаваемая валюта клиенту есть в справочнике валют(она активна)
                if value["id"] == namecurrence_trading.id_pair_market and namecurrence_trading.is_active == False and name_currency_buy.symbol == currency_buy and name_currency_sell.symbol == currency_sell:
                    print("такая валютная пара есть но не активна, то делаем эту пару активной")
                    name_currency_trading = Name_Currency_Trading.objects.get(id_pair_market=value["id"])  # находим запись по id пары равной id пары биржи
                    # то делаем эту валюту активной и обновляем дату, перезаписываем значение полей
                    name_currency_trading.is_active = True
                    name_currency_trading.updated = datetime
                    name_currency_trading.save()
                    i = 1  # такая валютная пара есть то устанавливаем индикатор в 1
                    result_active_paircurrency_poloniex += 1
                # если id пары биржи Poloniex равно id пары в справочнике пар и эта пара активна и покупаемая валюта у клиента есть в справочнике валют(она активна) и продаваемая валюта клиенту есть в справочнике валют(она активна)
                if value["id"] == namecurrence_trading.id_pair_market and namecurrence_trading.is_active == True and name_currency_buy.symbol == currency_buy and name_currency_sell.symbol == currency_sell:
                    print("такая валютная пара уже есть")
                    i = 1  # такая валютная пара есть то устанавливаем индикатор в 1

            if i == 0 and name_currency_buy.symbol == currency_buy and name_currency_sell.symbol == currency_sell:
                print("такой валютной пары нет, добавляем ее")
                name_currency_trading = Name_Currency_Trading.objects.create(id_pair_market=value["id"],
                                                                             name_currency_id=name_currency_buy.id,
                                                                             name_currency_sale_id=name_currency_sell.id,
                                                                             name_currency_sale_currency=name_currency_sell.currency,
                                                                             is_active=True, created=datetime, updated=datetime)
                result_add_paircurrency_poloniex += 1

        if value["isFrozen"] == 1:  # если валюная пара не торгуется в настоящее время на бирже
            for namecurrence_trading in namecurrences_trading:  # проходим по нашему справочнику пар валют
                # если id пары биржи Poloniex равно id пары в справочнике пар и эта пара активна и покупаемая валюта у клиента есть в справочнике валют(она активна) и продаваемая валюта клиенту есть в справочнике валют(она активна)
                if value["id"] == namecurrence_trading.id_pair_market and namecurrence_trading.is_active == True and name_currency_buy.symbol == currency_buy and name_currency_sell.symbol == currency_sell:
                    print("такая валютная пара есть и она активна, то делаем ее не активной")
                    name_currency_trading = Name_Currency_Trading.objects.get(id_pair_market=value["id"])  # находим запись по id пары равной id пары биржи
                    # то делаем эту валютную пару не активной и обновляем дату, перезаписываем значение полей
                    name_currency_trading.is_active = False
                    name_currency_trading.updated = datetime
                    name_currency_trading.save()
                    result_delete_paircurrency_poloniex += 1

        i = 0  # для следующей итерации устанавливаем индикатор в 0
        #time.sleep(seconds) # для задержки итераций прогрессбара и цикла
        l += 1
        progress_recorder.set_progress(l, count_progressbar) # celery progress bar

    return_dict["result_add_paircurrency_poloniex"] = result_add_paircurrency_poloniex
    return_dict["result_active_paircurrency_poloniex"] = result_active_paircurrency_poloniex
    return_dict["result_delete_paircurrency_poloniex"] = result_delete_paircurrency_poloniex

    return return_dict


# Загрузка пар валют с биржи Poloniex , процесс загрузки выполняем в функции my_task_pair
# асинхронным методом celery с индикатором загрузки progress bar
def Load_Poloniex_Pair_Currencies(request):
    #response_data = dict()  # переменную response_data определяем как словарь
    print("Загрузка пар криптовалют с Poloniex")
    print("post запрос в Load_Poloniex_Pair_Currencies от load_poloniex_paircurrency.html по action")
    data = request.POST  # переменной data присваиваем значение post запроса
    print(data)  # выводим значение post запроса в терминале питона для проверки
    csrfm = data.get("csrfmiddlewaretoken")
    print(csrfm)
    if request.method == 'POST':
        result = my_task_pair.delay(1)   # функция my_task_pair загрузка валют биржи Poloniex с celery progress bar
        print("Celery my_task_pair: ", result) # id задание для celery


    return render(request, 'result_poloniex_paircurrency.html', {'task_id': result.task_id}) #, 'result': return_dict
#----------------------------------------------------------------------------------------------------------------------
"""

# --------------- блок загрузки курсов и остатка(обьема) валют биржи Poloniex --------------------------------------------------------------
# Функция для загрузки курсов валют биржи Poloniex
# Пакет для работы с API биржи Poloniex
# инициализация pip install poloniex(https://pypi.org/project/poloniex/)
def Load_Poloniex_KursCurrency(request):

    api_key = settings.POLONIEX_API_KEY
    api_secret = settings.POLONIEX_SECRET
    polo = Poloniex(api_key, api_secret)
    #help(polo) # описание функционала

    # котировки
    quotation = polo.returnTicker()



    return render(request, 'load_poloniex_kurscurrencys.html', locals())


# Загрузка курсов и остатка(обьема) валют биржи Poloniex с отображением celery progress bar
@shared_task(bind=True)
def my_task_kurs(self, seconds):
    progress_recorder = ProgressRecorder(self) # celery progress bar
    l = 0  # итератор для progress bar
    i = 0  # индикатор
    result_add_kurscurrency_poloniex = 0  # переменная результат добавленных новых курсов пары валют
    result_edit_kurscurrency_poloniex = 0  # переменная результат обновленных курсов которые уже есть в БД курсов пары валют
    result_delete_kurscurrency_poloniex = 0 # переменная результат деактивации курсов пары валют
    result_add_balancecurrency_poloniex = 0  # переменная результат добавленных новых остатков(резерв) валют
    result_edit_balancecurrency_poloniex = 0  # переменная результат обновленных остатков(резерв) которые уже есть в БД
    min_buy = 0
    max_buy = 0
    min_sell = 0
    max_sell = 0
    return_dict = dict()  # переменную return_dict определяем как словарь
    # валюты
    polo = Poloniex()  # API биржи Poloniex
    currencies_kurs = polo.returnTicker()  # получаем словарь котировок курсов криптовалют с биржи Poloniex
    count_progressbar = len(currencies_kurs.items())  # количество элементов в словаре
    print(count_progressbar)
    prices_currencys = Prices_Currency.objects.all()  # валюты справочника курсов валют
    for key, value in currencies_kurs.items():  # проходим по полученному словарю пар котировок криптовалют Poloniex
        if value["isFrozen"] == 0:  # если валюная пара торгуется в настоящее время на бирже
            #currency_pair = Name_Currency_Trading.objects.get(id_pair_market=value["id"], is_active=True) # находим запись в справочнике пар валют по id пары равной id пары торговой площадки Poloniex
            currency_buy = key[:key.find('_')]  # покупаем у клиента валюту
            currency_sell = key[key.find('_') - len(key) + 1:]  # продаем клиенту валюту
            print("poloniex buy ", currency_buy)
            print("poloniex sell ", currency_sell)
            name_currency_buy = Name_Currency.objects.get(symbol=currency_buy, is_active=True)  # находим запись в справочнике валют по символу равному символу покупаемой у клиента валюты
            name_currency_sell = Name_Currency.objects.get(symbol=currency_sell, is_active=True)  # находим запись в справочнике валют по символу равному символу продаваемой клиенту валюты
            # определяем границы минимумов и максимумов покупки продажи
            if value["high24hr"] == 0:
                min_buy = 0
                max_buy = 0
                min_sell = 0
                max_sell = 0
            if value["high24hr"] < 1 and value["high24hr"] != 0 and currency_buy != 'BTC':
                min_buy = 500
                max_buy = 100000
            else:
                min_buy = 0.1
                max_buy = 100000
            if value["high24hr"] >= 1 and value["high24hr"] < 1000:
                min_buy = 500
                max_buy = 100000
            if value["high24hr"] >= 1000:
                min_buy = 300
                max_buy = 100000
            if value["high24hr"] != 0:
                min_sell = min_buy / value["high24hr"]
                max_sell = max_buy / value["high24hr"]

            for prices_currency in prices_currencys:  # проходим по нашему справочнику курсов валют
                # если id пары биржи Poloniex равно id пары в справочнике курсов пар валют и эта пара активна и эта пара принадлежит площадке(бирже) Poloniex(market_exchange_id=1)
                if value["id"] == prices_currency.id_pair_market and prices_currency.is_active == True and prices_currency.market_exchange_id == 1:
                    # и id покупаемой валюты в справочнике курсов пар валют равно id покупаемой валюты биржи Poloniex
                    # и id продаваемой валюты в справочнике курсов пар валют равно id продаваемой валюты биржи Poloniex
                    if name_currency_buy.id == prices_currency.name_currency_id and name_currency_sell.id == prices_currency.name_currency_sale_id:
                        print("такая пара валют есть в справочнике пар курсов валют и она активна , то обновляем значение курса покупки и продажи(+5%)")
                        # обновляем курсы и обновляем дату курса, перезаписываем значение полей
                        prices_currency.kurs_sell = Decimal(format(float(value["high24hr"] + value["high24hr"] * 0.05), '.8f'))
                        prices_currency.min_buy = min_buy
                        prices_currency.max_buy = max_buy
                        prices_currency.min_sell = min_sell
                        prices_currency.max_sell = max_sell
                        prices_currency.updated = datetime
                        prices_currency.save()
                        i = 1  # такая валюта есть то устанавливаем индикатор в 1  celery -A chgskv worker -l info -P gevent
                        result_edit_kurscurrency_poloniex += 1
                    else:
                        print("такой id пары валют есть в справочнике пар курсов валют и эта пара активна , но не совпадает символ покупаемой или продаваемой валюты, то деактивируем эту пару")
                        prices_currency.is_active = False
                        prices_currency.updated = datetime
                        prices_currency.save()
                        result_delete_kurscurrency_poloniex += 1


            if i == 0:
                print("такой валютной пары нет в справочнике курсов, добавляем ее и записываем значения курсов")
                price_currency = Prices_Currency.objects.create(name_currency_id=name_currency_buy.id,
                                                                name_currency_sale_id=name_currency_sell.id,
                                                                name_currency_sale_currency=name_currency_sell.currency,
                                                                kurs_sell=Decimal(format(float(value["high24hr"] + value["high24hr"] * 0.05), '.8f')),
                                                                min_buy=min_buy,
                                                                max_buy=max_buy,
                                                                id_pair_market=value["id"],
                                                                market_exchange_id=1,
                                                                is_active=True, created=datetime, updated=datetime)
                result_add_kurscurrency_poloniex += 1
            i = 0  # для следующей итерации устанавливаем индикатор в 0
            balance_currencys = Balance_Currency.objects.all()  # валюты справочника остатков(резерв) валют
            for balance_currency in balance_currencys:  # проходим по нашему справочнику остатков(резерв) валют
                # если id валюты в справочнике остатков валют равно id продаваемой валюты в справочнике пар валют и эта валюта активна и текущая сумма меньше суммы обьема
                #if balance_currency.name_currency_id == prices_currencys.name_currency_sale_id and balance_currency.is_active == True and balance_currency.balance_amount < format(float(value["quoteVolume"]), '.8f'):
                # если id валюты в справочнике остатков валют равно id продаваемой валюты в справочнике наименования валют и эта валюта активна и текущая сумма меньше суммы обьема
                if balance_currency.name_currency_id == name_currency_sell.id and balance_currency.is_active == True:
                    if  balance_currency.balance_amount < Decimal(format(float(value["quoteVolume"]), '.8f')):
                        print("такая валюта есть в справочнике остатков валют и она присутствует в справочнике наименования валют и она активна , то обновляем значение остатка(резерва)")
                        #balance_currency = Balance_Currency.objects.get(name_currency_id=currency_pair.name_currency_sale_id, is_active=True)  # находим запись по id валюты равной id продаваемой валюты справочника пар валют
                        # обновляем остаток(резерв) перезаписываем значение полей
                        balance_currency.balance_amount = Decimal(format(float(value["quoteVolume"]), '.8f')) # quoteVolume - обьем котировки биржи Poloniex за последние 24 часа
                        balance_currency.updated = datetime
                        balance_currency.save()
                        result_edit_balancecurrency_poloniex += 1
                    i = 1  # такая валюта есть то устанавливаем индикатор в 1
            if i == 0:
                print("такой валюты нет в справочнике остатков валют, добавляем ее и записываем значение остатка(обьема)")
                balance_currency = Balance_Currency.objects.create(name_currency_id=name_currency_sell.id,
                                                                   balance_amount=Decimal(format(float(value["quoteVolume"]), '.8f')),
                                                                   is_active=True, created=datetime, updated=datetime)
                result_add_balancecurrency_poloniex += 1


        i = 0  # для следующей итерации устанавливаем индикатор в 0
        time.sleep(0.1)  # для задержки итераций прогрессбара и цикла
        l += 1
        progress_recorder.set_progress(l, count_progressbar) # celery progress bar

    return_dict["result_add_kurscurrency_poloniex"] = result_add_kurscurrency_poloniex
    return_dict["result_edit_kurscurrency_poloniex"] = result_edit_kurscurrency_poloniex
    return_dict["result_delete_kurscurrency_poloniex"] = result_delete_kurscurrency_poloniex
    return_dict["result_add_balancecurrency_poloniex"] = result_add_balancecurrency_poloniex
    return_dict["result_edit_balancecurrency_poloniex"] = result_edit_balancecurrency_poloniex


    # отправляем сообщение о заявке в телеграмм
    # Ставим сообщение в очередь.
    # узнать свой id , в телеграмм набрать get my id, затем /start
    # Оно будет отослано моему боту в переписку (чат) с ID 1156354914.
    # отправка сообщения python manage.py sitemessage_send_scheduled (периодически запускать в cron, celery или др. обработчике)
    # в админке настраиваем Periodic tasks
    schedule_messages('Справочник курсов и остатков валют Poloniex обновлен! ' +
                      ' Обновленных пар курсов криптовалют: ' + str(result_edit_kurscurrency_poloniex) +
                      ' Добавлено пар курсов криптовалют: ' + str(result_add_kurscurrency_poloniex) +
                      ' Деактивировано пар курсов криптовалют: ' + str(result_delete_kurscurrency_poloniex) +
                      ' Обновленных остатков(резерва) криптовалют: ' + str(result_edit_balancecurrency_poloniex) +
                      ' Добавлено остатков(резерва) криптовалют: ' + str(result_add_balancecurrency_poloniex)
                      , recipients('telegram', '1156354914'))

    return return_dict


# Загрузка курсов и обьема(резерва) валют с биржи Poloniex , процесс загрузки выполняем в функции my_task_kurs
# асинхронным методом celery с индикатором загрузки progress bar
def Load_Poloniex_Kurs_Currencies(request):
    print("Загрузка курсов и обьема(резерва) криптовалют с Poloniex")
    print("post запрос в Load_Poloniex_Kurs_Currencies от load_poloniex_kurscurrency.html по action")
    data = request.POST  # переменной data присваиваем значение post запроса
    print(data)  # выводим значение post запроса в терминале питона для проверки
    csrfm = data.get("csrfmiddlewaretoken")
    print(csrfm)
    if request.method == 'POST':
        result = my_task_kurs.delay(1)   # функция my_task_kurs загрузка валют биржи Poloniex с celery progress bar
        print("Celery my_task_kurs: ", result) # id задание для celery



    return render(request, 'result_poloniex_kurscurrency.html', {'task_id': result.task_id}) #, 'result': return_dict
#----------------------------------------------------------------------------------------------------------------------



# ------------- блок Синхронизация справочника пар курсов и остатка(обьема) криптовалют со списком пар биржи Poloniex --
# Функция для синхронизации справочника пар курсов и остатка(обьема) криптовалют со списком пар биржи Poloniex
# Пакет для работы с API биржи Poloniex
# инициализация pip install poloniex(https://pypi.org/project/poloniex/)
def Load_Poloniex_SynchronCurrency(request):

    api_key = settings.POLONIEX_API_KEY
    api_secret = settings.POLONIEX_SECRET
    polo = Poloniex(api_key, api_secret)
    #help(polo) # описание функционала

    # котировки
    quotation = polo.returnTicker()



    return render(request, 'load_poloniex_synchroncurrencys.html', locals())


# Синхронизация справочника пар курсов и остатка(обьема) криптовалют со списком пар биржи Poloniex с отображением celery progress bar
@shared_task(bind=True)
def my_task_synchron(self, seconds):
    progress_recorder = ProgressRecorder(self) # celery progress bar
    l = 0  # итератор для progress bar
    result_delete_synchroncurrency_poloniex = 0 # переменная результат деактивации курсов пары валют
    return_dict = dict()  # переменную return_dict определяем как словарь
    # валюты
    polo = Poloniex()  # API биржи Poloniex
    currencies_kurs = polo.returnTicker()  # получаем словарь котировок курсов криптовалют с биржи Poloniex
    prices_currencys = Prices_Currency.objects.all()  # валюты справочника курсов валют
    count_progressbar = Prices_Currency.objects.count()  # количество элементов в queryset
    print(count_progressbar)
    # деактивируем пары в справочнике курсов валют которых нет уже в словаре пар котировок криптовалют Poloniex
    for prices_currency in prices_currencys:  # проходим по нашему справочнику курсов валют
        k = 0  # индикатор
        for key,value in currencies_kurs.items():  # проходим по полученному словарю пар котировок криптовалют Poloniex
            # если валюная пара торгуется в настоящее время на бирже и если id пары биржи Poloniex равно id пары
            # в справочнике курсов пар валют и эта пара активна и эта пара принадлежит площадке(бирже) Poloniex(market_exchange_id=1)
            if value["isFrozen"] == 0 and value["id"] == prices_currency.id_pair_market and prices_currency.is_active == True and prices_currency.market_exchange_id == 1:
                k = 1 # если такая пара есть в актуальном словаре Poloniex
                # если такой пары уже нет в актуальном словаре Poloniex и эта пара принадлежит Poloniex(в справочнике бирж под 1)
        if k == 0 and prices_currency.is_active == True and prices_currency.market_exchange_id == 1:
            prices_currency.is_active = False
            prices_currency.updated = datetime
            prices_currency.save()
            result_delete_synchroncurrency_poloniex += 1

        time.sleep(0.1)  # для задержки итераций прогрессбара и цикла
        l += 1
        progress_recorder.set_progress(l, count_progressbar) # celery progress bar


    return_dict["result_delete_synchroncurrency_poloniex"] = result_delete_synchroncurrency_poloniex

    # отправляем сообщение о заявке в телеграмм
    # Ставим сообщение в очередь.
    # узнать свой id , в телеграмм набрать get my id, затем /start
    # Оно будет отослано моему боту в переписку (чат) с ID 1156354914.
    # отправка сообщения python manage.py sitemessage_send_scheduled (периодически запускать в cron, celery или др. обработчике)
    # в админке настраиваем Periodic tasks
    schedule_messages('Справочник пар курсов и остатка(обьема) криптовалют синхронизирован со списком пар биржи Poloniex! ' +
                      ' Деактивировано пар курсов криптовалют: ' + str(result_delete_synchroncurrency_poloniex)
                      , recipients('telegram', '1156354914'))

    return return_dict


# Синхронизация справочника пар курсов и остатка(обьема) криптовалют со списком пар биржи Poloniex , процесс загрузки выполняем в функции my_task_synchron
# асинхронным методом celery с индикатором загрузки progress bar
def Load_Poloniex_Synchron_Currencies(request):
    print(" Синхронизация справочника пар курсов и остатка(обьема) криптовалют со списком пар биржи Poloniex")
    print("post запрос в Load_Poloniex_Synchron_Currencies от load_poloniex_synchroncurrency.html по action")
    data = request.POST  # переменной data присваиваем значение post запроса
    print(data)  # выводим значение post запроса в терминале питона для проверки
    csrfm = data.get("csrfmiddlewaretoken")
    print(csrfm)
    if request.method == 'POST':
        result = my_task_synchron.delay(1)   # функция my_task_synchron синхронизация справочника пар курсов и остатка(обьема) криптовалют со списком пар биржи Poloniex с celery progress bar
        print("Celery my_task_synchron: ", result) # id задание для celery



    return render(request, 'result_poloniex_synchroncurrency.html', {'task_id': result.task_id}) #, 'result': return_dict
#----------------------------------------------------------------------------------------------------------------------



# Функция обработки заказов со статусом status=1 Приняты, ожидают оплаты клиентом
def OrderProcessing(request):
    print("post запрос в OrderProcessing")
    bid_list = list()
    # queryset(список) всех заявок со статусом "ожидает оплаты"
    exchange_requests = Exchange_List.objects.filter(is_active=True, status=1)
    markets = Name_Currency.objects.filter(is_active=True)
    # проходим по списку заявок со статусом "ожидает оплаты" и заносим значения в словарь bid
    for exchange_request in exchange_requests:
        bid = dict()
        bid["id"] = exchange_request.id
        bid["id_user"] = exchange_request.id_user
        bid["id_pair_market"] = exchange_request.id_pair_market
        bid["name_currency_buy_currency"] = exchange_request.name_currency_buy_currency
        bid["sum_currency_buy"] = exchange_request.sum_currency_buy
        bid["wallet_currency_buy"] = exchange_request.wallet_currency_buy
        bid["name_currency_sell_currency"] = exchange_request.name_currency_sell_currency
        bid["sum_currency_sell"] = exchange_request.sum_currency_sell
        bid["wallet_currency_sell"] = exchange_request.wallet_currency_sell
        bid["kurs_sell"] = exchange_request.kurs_sell
        bid["kurs_buy_fact"] = exchange_request.kurs_buy_fact
        bid["sum_currency_buy_fact"] = exchange_request.sum_currency_buy_fact
        bid["wallet_fact"] = exchange_request.wallet_fact
        bid["created"] = exchange_request.created
        bid["market"] = 3  # заносим начальное значение 3- здесь это Nomarket
        # проходим по списку наименования валют
        for market in markets:
            # если id валюты совпадает с id продаваемой клиентом валюты
            #print(exchange_request.name_currency_buy_id)
            #print(market.id)
            if market.id == exchange_request.name_currency_buy_id:
                # то заносим значение id площадки(биржи) к которой относится эта валюта и выходим из цикла
                bid["market"] = market.market_exchange_id
                break

        # заносим в список словарь значений
        bid_list.append(bid)

    return render(request, 'order_processing.html', locals())


# Функция проверки оплаты клиентом со статусом status=1 и покупки валюты
def Order_processing_check(request):
    print("post запрос в Order_processing_check от order_processing.js")
    return_izm = dict() # определяем переменную как словарь
    return_list = list()  # переменную определяем как список
    balans = 0 # задаем начальное значение переменной
    kurs = 0 # задаем начальное значение переменной
    info = "нет средств на балансе для проведения сделки" # задаем начальное значение переменной
    # Poloniex Api
    # polo = Poloniex()
    # help(polo)
    # api ключи Poloniex в settings.py
    api_key = settings.POLONIEX_API_KEY
    api_secret = settings.POLONIEX_SECRET
    polo = Poloniex(api_key, api_secret)
    if request.POST:
        # выводим значение post запроса в терминале питона для проверки
        print(request.POST)
        data = request.POST  # переменной data присваиваем значение post запроса
        item_id = data.get("item_id")
        # находим запись в реестре заявок по id (номер заявки)
        exchange_requests = Exchange_List.objects.filter(is_active=True, pk=item_id).values()
        for exchange_request in exchange_requests:
            wallet_fact = exchange_request["wallet_fact"] # адрес кошелька получения валюты от клиента(клиент отдает)
            name_currency_buy_id = exchange_request["name_currency_buy_id"] # id валюты которую клиент отдает
            sum_currency_buy = exchange_request["sum_currency_buy"] # сумма валюты которую клиент отдает
            #name_currency_sell_id = exchange_request["name_currency_sell_id"] # id валюты которую клиент получает
            #sum_currency_sell = exchange_request["sum_currency_sell"] # сумма валюты которую клиент получает
            kurs_sell = exchange_request["kurs_sell"] # курс валюты по которому продаем клиенту
            id_pair_market = exchange_request["id_pair_market"] # id валютной пары на бирже Poloniex


            name_currency = Name_Currency.objects.get(pk=name_currency_buy_id)  # находим запись по id равному id валюты которую клиент отдает
            print(name_currency.symbol) # символ валюты которую клиент отдает
            print(name_currency.market_exchange_id) # принадлежность торговой площадке(здесь 1-Poloniex,2-Binance,3-Nomarket)
            # если заявка где пара принадлежит бирже Poloniex
            if name_currency.market_exchange_id == 1:
                currencies_kurs = polo.returnTicker()  # получаем словарь котировок курсов криптовалют с биржи Poloniex
                for key, value in currencies_kurs.items():  # проходим по полученному словарю пар котировок криптовалют Poloniex
                    # если валюная пара торгуется в настоящее время на бирже и если id пары биржи Poloniex равно id пары нашей заявки
                    if value["isFrozen"] == 0 and value["id"] == id_pair_market:
                        kurs = value["high24hr"] # получаем актуальный курс валютной пары
                        kurs_margin = kurs + (kurs * 0.05) # актуальный курс +5%

                # если сумма валюты которую клиент отдает больше 0 и курс по которому продаем клиенту больше или равен актуальному курсу +5% и не равен 0
                if sum_currency_buy > 0 and kurs_sell >= kurs_margin and kurs != 0:

                    account = polo.returnAvailableAccountBalances() # словарь балансов криптовалют Poloniex не равных нулю
                    print(account["exchange"])
                    for key, value in account["exchange"].items():  # проходим по полученному словарю балансов криптовалют Poloniex не равных нулю
                        # если в словаре есть символ валюты которую клиент отдает
                        if key == name_currency.symbol:
                            balans = value # получаем баланс по валюте которую клиент отдает
                            # если сумма валюты которую клиент отдает больше чем баланс в этой валюте
                            if sum_currency_buy > balans:
                                info = "не хватает средств на балансе для проведения сделки"
                            else:
                                info = "достаточно средств на балансе для проведения сделки"

                    # получаем список словарей полученных депозитов(поступивших средств) на балансы биржи Poloniex
                    depo = polo.returnDeposits()
                    print(depo)
                    # проходим по списку
                    for item in depo:
                        return_dict = dict()  # переменную определяем как словарь
                        # если есть в словаре списка валюта которую клиент отдает
                        if item["currency"] == name_currency.symbol:
                            return_dict["amount"] = item["amount"] # сумма поступившая
                            return_dict["address"] = item["address"] # на какой адресс(кошелек) пришла
                            return_dict["currency"] = item["currency"] # в какой валюте
                            return_dict["timestamp"] = datetime.utcfromtimestamp(item["timestamp"]).strftime('%d.%m.%Y, %H:%M') # дата время поступления(переводим время из unix в читаемое)
                            return_list.append(return_dict) # заносим в список словарь значений поступления средств
                            print(return_dict)

                else:
                    info = "изменение курса(вырос), сделка не рентабельна"
            else:
                info = "эта пара валют не принадлежит торговой площадке(бирже) Poloniex"

        print(info)
        print(return_list)
        #balances = polo.returnBalances() # словарь всех балансов криптовалют Poloniex , в т.ч. и нулевых
        #print(balances)
        #balances1 = polo.returnCompleteBalances()
        #print(balances1)
        #deposit = polo.returnDepositAddresses()
        #print(deposit)

        return_izm["wallet_fact"] = wallet_fact # адрес кошелька получения валюты от клиента(клиент отдает)
        return_izm["balans"] =  balans # баланс Poloniex по валюте которую клиент отдает
        return_izm["info"] = info # сообщаем результат проверки
        return_izm["sum_currency_buy"] = sum_currency_buy # сумма валюты которую клиент отдает
        return_izm["name_currency_symbol"] = name_currency.symbol # символ валюты которую клиент отдает
        return_izm["kurs_sell"] = kurs_sell # курс валюты по которому продаем клиенту
        return_izm["kurs"] = kurs # актуальный курс валютной пары Poloniex
        return_izm["deposit"] = return_list # список словарей значений поступления средств

        return JsonResponse(return_izm)

# Функция удаления заявки клиента
def Order_processing_del(request):
    print("post запрос в Order_processing_del от order_processing.js")
    return_izm = dict() # определяем переменную как словарь
    if request.POST:
        # выводим значение post запроса в терминале питона для проверки
        print(request.POST)
        data = request.POST  # переменной data присваиваем значение post запроса
        item_id = data.get("item_id")
        # находим запись в реестре заявок по id (номер заявки)
        exchange_requests = Exchange_List.objects.get(is_active=True, pk=item_id)
        exchange_requests.status = 0 # устанавливаем статус 0 - заявка удалена
        exchange_requests.save()

        return_izm["exchange_requests"] = item_id # передаем id заявки

        return JsonResponse(return_izm)

# Функция покупки валюты по заявке клиента
def Order_processing_buy(request):
    print("post запрос в Order_processing_buy от order_processing.js")
    return_izm = dict() # определяем переменную как словарь
    balans = 0  # задаем начальное значение переменной
    info = "нет средств на балансе для проведения сделки"  # задаем начальное значение переменной
    i = 1 # индикатор
    # Poloniex Api
    # polo = Poloniex()
    # help(polo)
    # api ключи Poloniex в settings.py
    api_key = settings.POLONIEX_API_KEY
    api_secret = settings.POLONIEX_SECRET
    polo = Poloniex(api_key, api_secret)
    if request.POST:
        # выводим значение post запроса в терминале питона для проверки
        print(request.POST)
        data = request.POST  # переменной data присваиваем значение post запроса
        item_id = data.get("item_id")
        # находим запись в реестре заявок по id (номер заявки)
        exchange_requests = Exchange_List.objects.filter(is_active=True, pk=item_id).values()
        for exchange_request in exchange_requests:
            name_currency_buy_id = exchange_request["name_currency_buy_id"]  # id валюты которую клиент отдает
            sum_currency_buy = exchange_request["sum_currency_buy"]  # сумма валюты которую клиент отдает
            name_currency_sell_id = exchange_request["name_currency_sell_id"] # id валюты которую клиент получает
            sum_currency_sell = exchange_request["sum_currency_sell"] # сумма валюты которую клиент получает
            kurs_sell = exchange_request["kurs_sell"]  # курс валюты по которому продаем клиенту
            id_pair_market = exchange_request["id_pair_market"]  # id валютной пары на бирже Poloniex

        name_currency_buy = Name_Currency.objects.get(pk=name_currency_buy_id)  # находим запись по id равному id валюты которую клиент отдает
        print(name_currency_buy.symbol)  # символ валюты которую клиент отдает
        print(name_currency_buy.market_exchange_id)  # принадлежность торговой площадке(здесь 1-Poloniex,2-Binance,3-Nomarket)

        name_currency_sell = Name_Currency.objects.get(pk=name_currency_sell_id)  # находим запись по id равному id валюты которую клиент получает
        print(name_currency_sell.symbol)  # символ валюты которую клиент плучает

        # если заявка где пара принадлежит бирже Poloniex
        if name_currency_buy.market_exchange_id == 1:
            currencies_kurs = polo.returnTicker()  # получаем словарь котировок курсов криптовалют с биржи Poloniex
            for key, value in currencies_kurs.items():  # проходим по полученному словарю пар котировок криптовалют Poloniex
                # если валюная пара торгуется в настоящее время на бирже и если id пары биржи Poloniex равно id пары нашей заявки
                if value["isFrozen"] == 0 and value["id"] == id_pair_market:
                    kurs = value["high24hr"]  # получаем актуальный курс валютной пары
                    currencyPair = key # валютная пара (символы)
                    kurs_margin = kurs + (kurs * 0.05)  # актуальный курс +5%

            # если сумма валюты которую клиент отдает больше 0 и курс по которому продаем клиенту больше или равен актуальному курсу +5% и не равен 0
            if sum_currency_buy > 0 and kurs_sell >= kurs_margin and kurs != 0:

                account = polo.returnAvailableAccountBalances()  # словарь балансов криптовалют Poloniex не равных нулю
                print(account["exchange"])
                for key, value in account["exchange"].items():  # проходим по полученному словарю балансов криптовалют Poloniex не равных нулю
                    # если в словаре есть символ валюты которую клиент отдает
                    if key == name_currency_buy.symbol:
                        balans = value  # получаем баланс по валюте которую клиент отдает
                        # если сумма валюты которую клиент отдает больше чем баланс в этой валюте
                        if sum_currency_buy > balans:
                            info = "не хватает средств на балансе для проведения сделки"

                        else:
                            print("достаточно средств на балансе для проведения сделки, заявка на обмен сформирована")
                            # отсылаем заявку обмена валюты на Poloniex
                            print(kurs)
                            print(currencyPair)
                            print(round(sum_currency_sell,2))  # xrp/trx цена после точки 5 знаков иначе ошибка(нужно определять еол-во десятичных знаков)
                            # ловим ошибку при покупке, чтобы не прерывалась программа
                            try:
                                buy = polo.buy(currencyPair, kurs, round(sum_currency_sell,2))
                                print(buy)
                                info = "Заявка исполнена, номер ордера: " + str(buy["orderNumber"])
                                i = 0
                                # вставить этот блок выше
                                # получаем список словарей истории торгов для выбранной валютной пары currencyPair
                                trades = polo.returnTradeHistory(currencyPair)
                                for item in trades:
                                    trade = item
                                    print(trade)

                                    # {'globalTradeID': 96334939229851648, 'tradeID': 60002355, 'date': '2022-09-23 12:00:39',
                                    # 'rate': 0.001702, 'amount': 619.05, 'total': 1.0536231, 'fee': 0.00155, 'feeDisplay'
                                    # : '0.9595275 WIN (0.155%)', 'orderNumber': 96334939099824128, 'type': 'buy',
                                    # 'category': 'exchange'}

                                    # если номер ордера записи в словаре равен номеру ордера исполненной заявки
                                    if trade["orderNumber"] == buy["orderNumber"]:
                                        # if trade["orderNumber"] == 96334939099824128:
                                        print("купленная сумма(получаем) WIN: ", trade["amount"])  # купленная сумма(получаем) WIN
                                        print("по курсу(средняя цена сделки): ", trade["rate"])  # по курсу(средняя цена сделки)
                                        print("проданная сумма(отдаем) TRX: ", trade["total"])  # проданная сумма(отдаем) TRX
                                        print("комиссия при покупке (в валюте WIN): ", trade["feeDisplay"])  # комиссия при покупке (в валюте WIN)
                                        # находим запись в реестре заявок по id (номер заявки)
                                        exchange_requests = Exchange_List.objects.get(is_active=True, pk=item_id)
                                        exchange_requests.kurs_buy_fact = trade["rate"]  # курс фактический покупки валюты клиенту
                                        exchange_requests.sum_currency_buy_fact = trade["amount"]  # сумма за которую фактически купили валюту для клиента
                                        exchange_requests.status = 2  # устанавливаем статус 2 - заявка исполнена
                                        exchange_requests.save()

                            except Exception as e:
                                print("Ошибка покупки на Poloniex: ", e)
                                info = "Ошибка покупки на Poloniex:  " + str(e)


            else:
                info = "изменение курса(вырос), сделка не рентабельна"

        else:
            info = "эта пара валют не принадлежит торговой площадке(бирже) Poloniex"


        return_izm["info"] = info  # сообщаем результат проверки
        return_izm["i"] = i  # передаем индикатор для того чтоб при ошибке не перегружать страницу в order_processing.js

        return JsonResponse(return_izm)

# Функция перевода заявки клиента для фиатных валют в исполненные
def Order_processing_perform(request):
    print("post запрос в Order_processing_perform от order_processing.js")
    return_izm = dict() # определяем переменную как словарь
    if request.POST:
        # выводим значение post запроса в терминале питона для проверки
        print(request.POST)
        data = request.POST  # переменной data присваиваем значение post запроса
        item_id = data.get("item_id")
        kurs_buy_fact = data.get("kurs_buy_fact")
        sum_currency_buy_fact = data.get("sum_currency_buy_fact")
        # находим запись в реестре заявок по id (номер заявки)
        exchange_requests = Exchange_List.objects.get(is_active=True, pk=item_id)
        exchange_requests.kurs_buy_fact = kurs_buy_fact
        exchange_requests.sum_currency_buy_fact = sum_currency_buy_fact
        exchange_requests.status = 2 # устанавливаем статус 2 - заявка исполнена
        exchange_requests.save()

        return_izm["exchange_requests"] = item_id # передаем id заявки

        return JsonResponse(return_izm)



# пример торгового бота
# https://github.com/nhughey/trading-bot
# Скрипт для Python, который возвращает данные о ценах для валютных пар с использованием Poloniex API.
# Максимумы/минимумы и скользящие средние.
version_number = " ALPHA 0.1.3"
def main(argv):
    period = 10
    currentMA = 0
    lengthOfMA = 0
    pair = "BTC_XMR"
    prices = []

    # API Usher
    print("POLONIEX MA Trader." + version_number + "\n ")

    try:
        opts, args = getopt.getopt("300", "hp", ["period=", ]) # argv - вместо вызова со значением сразу поставил значение
    except getopt.GetoptError:
        print('matrader.py -p <period>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('matrader.py -p <period>')
            sys.exit()

        elif opt in ("-p", "--period"):
            if (int(arg) in [300, 900, 1800, 7200, 14400, 86400]):
                period = arg
            else:
                print('Clock Error. Exchange requires periods in 300,900,1800,7200,14400,86400 seconds.')
                sys.exit(2)

    # insert public & private key here:
    api_key = settings.POLONIEX_API_KEY
    api_secret = settings.POLONIEX_SECRET
    conn = Poloniex(api_key, api_secret)

    # send "returnTicker" query, adds data to Price list & returns Moving Average
    while True:
        currentValues = conn.returnTicker()
        lastPairPrice = currentValues[pair]["last"]
        if (len(prices) > 0):
            currentMA = sum(prices) / float(len(prices))
        # Add more indicators here

        print(" TIME: " + "{:%Y-%m-%d %H:%M:%S}".format(
            datetime.datetime.now()) + " PERIOD: %ss. \n Pair: %s %s  \n Current MA: %s." % (
              period, pair, lastPairPrice, currentMA))
        prices.append(float(lastPairPrice))
        time.sleep(int(period))

        # Highest/Lowest prices:
        def highest_price(prices):
            highest = prices[0]
            for high in prices:
                if high > highest:
                    highest = high
            return highest

        highpoint = highest_price(prices)
        print(" High: " + str(highpoint))

        def lowest_price(prices):
            lowest = prices[0]
            for low in prices:
                if low < lowest:
                    lowest = low
            return lowest

        lowpoint = lowest_price(prices)
        print(" Low: " + str(lowpoint) + "\n ")


if __name__ == "__main__":
    main(sys.argv[1:])

# пример торгового бота 2
# Бот для практики торговли на Python, который использует API Poloniex для совершения сделок на основе
#  скользящей средней. Бот размещает ордер на покупку BTC/USD, когда скользящая средняя (MACD) отрицательная,
#  а 1-я производная равна нулю (локальный минимум). Бот размещает ордер на продажу BTC/USD, когда скользящая
# средняя (MACD) положительна, а первая производная равна нулю (локальный максимум).
# https://github.com/4nir/CryptoTrading-Algorithm/blob/master/trading-bot-v1.py
# пример poloniex.py https://github.com/ConanKeaveney/Crypto_Trading_Bot/blob/master/plot_chart/poloniex.py

