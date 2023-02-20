from django.shortcuts import render, redirect
from django.db import transaction
from django.db.models import F
from django.contrib import messages, auth
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect,  Http404
import datetime

import json
#from time import strftime
from django.utils.timezone import localtime
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError

# для django3
from django.utils.encoding import smart_text
# для django4
#import django
#from django.utils.encoding import smart_str
#django.utils.encoding.smart_text = smart_str

import re
from .models import Profile, Site_maintenance
#from django.core.mail import send_mail

from blok2.models import Name_Currency, Prices_Currency, Balance_Currency, Exchange_List, Fiat_Wallet # импортируем таблицу БД Name_Currency, Name_Currency_Trading, Prices_Currency из models.py     табл стала не нужна, Name_Currency_Trading

# Пакет для работы с API биржи Poloniex
# инициализация pip install poloniex
from poloniex import Poloniex
from django.conf import settings


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

#Для герерации изображения qr кода нужны библиотеки qrcode и Pillow
# pip install qrcode
# pip install pillow
# https://tretyakov.net/post/generaciya-qr-koda-v-django/
import qrcode
from django.conf import settings as django_settings


# Create your views here.
# Домашняя(главная) страница обмена
def Home(request):

    #all_currency_trading_dict = dict()  # определяем переменную как словарь(доступ к элементам по ключам)
    #kurs_sell_currency_list = list() # список курсов продажи покупаемых у клиента валют
    #name_currences_purchases = Name_Currency.objects.filter(is_active=True).order_by("id") # покупаемые валюты
    #name_currences_purchases_trades = Name_Currency.objects.filter(is_active=True).order_by("id").values("id")  # покупаемые валюты словарь только id
    # all_currences_tradings = Name_Currency_Trading.objects.filter(is_active=True).values("name_currency_id","name_currency_sale_id")  # продаваемые валюты связка(не использую эту таблицу так как изменилась логика поля перешли в табл курсов валют)
    """
    i = 0
    id_first_currency = 0
    #     # проходим по справочнику покупаемых валют
    for name_currences_purchases_trade in name_currences_purchases_trades:
        i+=1
        kurs_sell_currency_list.append(name_currences_purchases_trade["id"])
        # проходим по справочнику связанных валют покупки-продажи
        all_currency_trading_list = list()  # определяем переменную как список(доступ к элементам по индексу)
        for all_currences_trading in all_currences_tradings:
            # если id справочника покупаемой валюты совпадает с id покупаемой валюты в справочнике связанных валют
            #  то заносим в список id связанной с покупаемой-продаваемой валдюты
            if name_currences_purchases_trade["id"] == all_currences_trading["name_currency_id"]:
                all_currency_trading_list.append(all_currences_trading["name_currency_sale_id"])
                # определяем значение id первой валюты в словаре для первоночального вывода списка продаваемых валют для первой валюты
                if i == 1:
                    id_first_currency = all_currences_trading["name_currency_id"]
                    print(id_first_currency)

        # в словарь соответствий покупаемой продаваемым валютам заносим запись где ключ это покупаемая валюта
        # а значение это список продаваемых валют
        all_currency_trading_dict[name_currences_purchases_trade["id"]] = all_currency_trading_list

    print("Словарь соответствий id покупаемой валюты - списку id продаваемых валют: ", all_currency_trading_dict)
    # проверяем есть ли соответствия покупаемой и продаваемой валюты в справочнике соответствий
    if id_first_currency > 0:
        # задаем начальный список продаваемых валют соответствующий первой покупаемой валюте
        # проверяем если не задан курс или резерв(остаток) то продаваемая валюта не отражается на странице
        name_currences_sells = Name_Currency.objects.filter(is_active=True,
                                                             id__in=all_currency_trading_dict[id_first_currency],
                                                             prices_currency__is_active=True,
                                                             balance_currency__is_active=True) \
            .values("id", "currency", "prices_currency__kurs_sell", "balance_currency__balance_amount")
        print("Список продаваемых валют:", name_currences_sells)
    """

        #name_currences_sells = Name_Currency.objects.filter(is_active=True, id__in=all_currency_trading_dict[id_first_currency])  # продаваемые валюты
    # курс продажи клиенту списка покупаемых валют
    #kurs_sell_currencys = Prices_Currency.objects.filter(is_active=True, name_currency_id__in=kurs_sell_currency_list).values("name_currency_id", "kurs_sell")
    #balans_sell_currencys = Balance_Currency.objects.filter(is_active=True, name_currency_id__in=kurs_sell_currency_list).values("name_currency_id", "balance_amount")
    #print(kurs_sell_currencys)
    #print(balans_sell_currencys)

    i = 0
    all_currency_trading_dict = dict()  # определяем переменную как словарь(доступ к элементам по ключам)
    all_currencys_by_list = list()  # список покупаемых валют, определяем переменную как список(доступ к элементам по индексу)
    all_currences_tradings = Prices_Currency.objects.filter(is_active=True).order_by("name_currency_id").values("name_currency_id", "name_currency_sale_id", "kurs_sell", "is_active")  # криптовалюты пары покупка-продажа
    all_currences_balans = Balance_Currency.objects.filter(is_active=True).values("name_currency_id", "balance_amount") # список резерва(остатков валют)
    # проходим по справочнику курсов пар криптовалют покупки-продажи
    for all_currences_trading in all_currences_tradings:
        currency_by_id = 0
        # если курс продажи установлен(не ноль) и запись активна
        if all_currences_trading["kurs_sell"] != 0 and all_currences_trading["is_active"] == True:
            # проходим по списку резерва(остатков) криптовалют
            for all_currence_balans in all_currences_balans:
                # если id продаваемой валюты пары есть в справочнике резервов(остатка) и остаток не равен нулю
                if all_currences_trading["name_currency_sale_id"] == all_currence_balans["name_currency_id"] and all_currence_balans["balance_amount"] > 0:
                    # если такой валюты нет в списке покупаемых валют
                    if all_currences_trading["name_currency_id"] not in all_currencys_by_list:
                        # то заносим в список покупаемых валдют id покупаемой валюты
                        all_currencys_by_list.append(all_currences_trading["name_currency_id"])
                        currency_by_id = all_currences_trading["name_currency_id"] # переменной присваиваем id покупаемой валюты
                        #if i == 0: # если еще нет списка продаваемых валют
                        all_currencys_sell_list = list()  # список продаваемых валют, определяем переменную как список(доступ к элементам по индексу)
                        # проходим по справочнику курсов пар криптовалют покупки-продажи для поиска соответствий покупаемой валюте-продаваемых валют
                        for all_currences_trading in all_currences_tradings:
                            # находим все пары где id покупаемой валюты равно id переменной
                            if currency_by_id == all_currences_trading["name_currency_id"]:
                                # проходим по списку резерва(остатков) криптовалют
                                for all_currence_balans in all_currences_balans:
                                    # если id продаваемой валюты пары есть в справочнике резервов(остатка) и остаток не равен нулю
                                    if all_currences_trading["name_currency_sale_id"] == all_currence_balans["name_currency_id"] and all_currence_balans["balance_amount"] > 0:
                                       # то заносим в список id продаваемых криптовалдют соответствующие покупаемой
                                       all_currencys_sell_list.append(all_currences_trading["name_currency_sale_id"])
                                       #i = 1 # устанавливаем индикатор в 1(делаем список продаваемых криптовалют только для первой покупаемой валюты которая активна и курс продажи продаваемых не ноль)

                        # в словарь соответствий покупаемой продаваемым валютам заносим запись где ключ это покупаемая валюта
                        # а значение это список продаваемых валют
                        all_currency_trading_dict[currency_by_id] = all_currencys_sell_list

    print("Словарь соответствий id покупаемой валюты - списку id продаваемых валют: ", all_currency_trading_dict)
    print("список покупаемых валют с курсом и у кот в паре остаток не 0", all_currencys_by_list)
    # Проверяем если список валют еще пустой(в базе данных валюты еще не заданы, то используем пустой словарь)
    if len(all_currencys_by_list) == 0:
        print("список продаваемых валют соответств первой покупаемой с курсом и в паре остат не 0", all_currency_trading_dict)
    else:
        print("список продаваемых валют соответств первой покупаемой с курсом и в паре остат не 0", all_currency_trading_dict[all_currencys_by_list[0]])
    # полный список(queryset) наименования валют
    name_currences = Name_Currency.objects.filter(is_active=True)
    # полный список(queryset) резервов валют
    balance_currences = Balance_Currency.objects.filter(is_active=True)
    # задаем начальный список поокупаемых валют id__in=all_currencys_by_list
    name_currences_purchases = Name_Currency.objects.filter(is_active=True, id__in=all_currencys_by_list)
    # задаем начальный список продаваемых валют соответствующий первой покупаемой валюте name_currency_id=all_currencys_by_list[0]
    # из словаря соответствий name_currency_sale_id__in=all_currency_trading_dict[all_currencys_by_list[1]]
    # __gt=0 - больше 0 , __lt=0 - меньше 0, __gte=0 - больше или равно 0
    # класс F() Объект представляет значение поля модели (from django.db.models import F)
    # F("prices_currency__name_currency_id")     не используюю так как возникает ошибка возврата значения запроса более одного значения
    # annotate добавляем значение в queryset

    if len(all_currencys_by_list) != 0:
        name_currences_sells = Prices_Currency.objects.filter(is_active=True,
                                                              name_currency_id=all_currencys_by_list[0],
                                                              name_currency_sale_id__in=all_currency_trading_dict[all_currencys_by_list[0]],
                                                              kurs_sell__gt=0) \
                                                              .values("name_currency_id",
                                                                      "name_currency_sale_id",
                                                                      "name_currency_sale_currency",
                                                                      "kurs_sell").annotate(kurs_sell_inverse=1/F("kurs_sell"),name_currency_currency=Name_Currency.objects.filter(is_active=True, id=all_currencys_by_list[0]).values("currency"))
        id_first_currency_by = all_currencys_by_list[0]
        print("id продаваемых валют", all_currency_trading_dict[all_currencys_by_list[0]])

    else:
        # Проверяем если список валют еще пустой(в базе данных валюты еще не заданы, то задаем пустой queryset и id первой валюты присваиваем 0)
        name_currences_sells = Prices_Currency.objects.filter(is_active=True)
        id_first_currency_by = 0
    print("queryset покупаемых валют:", name_currences_purchases)
    print("queryset продаваемых валют:", name_currences_sells)
    print("id первой покупаемой валюты", id_first_currency_by)


    # получаем значение индикатора техобслуживания сайта по id=1(в БД обязательно должна быть запись под id=1 !)
    site_maintenance = Site_maintenance.objects.filter(pk=1)
    # проверяем есть ли запись в БД с id=1, если нет то создаем ее с первоначальным значением True("Сайт на техобслуживании")
    if not site_maintenance:
        site_maintenance = Site_maintenance.objects.create(maintenance=True)

    site_maintenance = Site_maintenance.objects.get(pk=1)


#    reg_login = request.POST['username'] # username
#    reg_pass = request.POST['password']  # password
#    user = auth.authenticate(username=reg_login, password=reg_pass)
#    if user is not None and user.is_active:
        # Правильный пароль и пользователь "активен"
#        auth.login(request, user)
        # Перенаправление на страницу пользователя
#        return HttpResponseRedirect('home_usr.html')
#    else:
        # Отображение страницы с Гостем
#        return HttpResponseRedirect('home.html')

    return render(request, 'home.html', locals())


# функция для формирования словаря списка продаваемых валют передаваемого методом ajax в скрипт list_currencies_sell.js
def list_currencies_sell(request):
    return_dict = dict()  # переменную return_dict определяем как словарь
    print("post запрос в list_currencies_sell от list_currencies_sell.js")
    print(request.POST)  # выводим значение post запроса в терминале питона для проверки
    data = request.POST  # переменной data присваиваем значение post запроса
    currency_id = int(data.get("currency_id"))  # переменной currency_id присваиваем значение индекса currency_id списка data из exchange.html
    print("полученный id выбранной валюты", currency_id)
    #url1 = data.get("url1")
    #print("url", url1)
    csrfm = data.get("csrfmiddlewaretoken")
    name_currence_purchases = Name_Currency.objects.filter(is_active=True,id=currency_id).values("currency", "id", "market_exchange_id")  # покупаемая валюта словарь только наименование
    print("queryset выбранной валюты", name_currence_purchases)

    i = 0
    all_currency_trading_dict = dict()  # определяем переменную как словарь(доступ к элементам по ключам)
    all_currencys_by_list = list()  # список покупаемых валют, определяем переменную как список(доступ к элементам по индексу)
    all_currences_tradings = Prices_Currency.objects.filter(is_active=True).order_by("name_currency_id").values(
        "name_currency_id", "name_currency_sale_id", "kurs_sell", "is_active")  # криптовалюты пары покупка-продажа
    all_currences_balans = Balance_Currency.objects.filter(is_active=True).values("name_currency_id",
                                                                                  "balance_amount")  # список резерва(остатков валют)
    # проходим по справочнику курсов пар криптовалют покупки-продажи
    for all_currences_trading in all_currences_tradings:
        currency_by_id = 0
        # если курс продажи установлен(не ноль) и запись активна
        if all_currences_trading["kurs_sell"] != 0 and all_currences_trading["is_active"] == True:
            # проходим по списку резерва(остатков) криптовалют
            for all_currence_balans in all_currences_balans:
                # если id продаваемой валюты пары есть в справочнике резервов(остатка) и остаток не равен нулю
                if all_currences_trading["name_currency_sale_id"] == all_currence_balans["name_currency_id"] and \
                        all_currence_balans["balance_amount"] > 0:
                    # если такой валюты нет в списке покупаемых валют
                    if all_currences_trading["name_currency_id"] not in all_currencys_by_list:
                        # то заносим в список покупаемых валдют id покупаемой валюты
                        all_currencys_by_list.append(all_currences_trading["name_currency_id"])
                        currency_by_id = all_currences_trading["name_currency_id"]  # переменной присваиваем id покупаемой валюты
                        # if i == 0: # если еще нет списка продаваемых валют
                        all_currencys_sell_list = list()  # список продаваемых валют, определяем переменную как список(доступ к элементам по индексу)
                        # проходим по справочнику курсов пар криптовалют покупки-продажи для поиска соответствий покупаемой валюте-продаваемых валют
                        for all_currences_trading in all_currences_tradings:
                            # находим все пары где id покупаемой валюты равно id переменной
                            if currency_by_id == all_currences_trading["name_currency_id"]:
                                # проходим по списку резерва(остатков) криптовалют
                                for all_currence_balans in all_currences_balans:
                                    # если id продаваемой валюты пары есть в справочнике резервов(остатка) и остаток не равен нулю
                                    if all_currences_trading["name_currency_sale_id"] == all_currence_balans["name_currency_id"] and all_currence_balans["balance_amount"] > 0:
                                        # то заносим в список id продаваемых криптовалдют соответствующие покупаемой
                                        all_currencys_sell_list.append(all_currences_trading["name_currency_sale_id"])
                                        # i = 1 # устанавливаем индикатор в 1(делаем список продаваемых криптовалют только для первой покупаемой валюты которая активна и курс продажи продаваемых не ноль)

                        # в словарь соответствий покупаемой продаваемым валютам заносим запись где ключ это покупаемая валюта
                        # а значение это список продаваемых валют
                        all_currency_trading_dict[currency_by_id] = all_currencys_sell_list

    print("Словарь соответствий id покупаемой валюты - списку id продаваемых валют: ", all_currency_trading_dict)
    print("список покупаемых валют с курсом и у кот в паре остаток не 0", all_currencys_by_list)
    print("список продаваемых валют соответств выбранной покупаемой с курсом и в паре остат не 0", all_currency_trading_dict[currency_id])
    # список(queryset) наименования продаваемых валют
    name_currences_sells_img = Name_Currency.objects.filter(is_active=True, id__in=all_currency_trading_dict[currency_id])
    # список(queryset) резервов продаваемых валют
    balance_currences = Balance_Currency.objects.filter(is_active=True, name_currency_id__in=all_currency_trading_dict[currency_id]).values("name_currency_id", "balance_amount")
    # задаем список покупаемых валют id__in=all_currencys_by_list
    name_currences_purchases_trades = Name_Currency.objects.filter(is_active=True, id__in=all_currencys_by_list).order_by("id").values("id")  # покупаемые валюты словарь только id
    # задаем список продаваемых валют соответствующий выбранной покупаемой валюте  name_currency_id=currency_id
    # из словаря соответствий name_currency_sale_id__in=all_currency_trading_dict[currency_id]
    # F("prices_currency__name_currency_id")     не используюю так как возникает ошибка возврата значения запросса более одного значения
    name_currences_sells = Prices_Currency.objects.filter(is_active=True,
                                                          name_currency_id=currency_id,
                                                          name_currency_sale_id__in=all_currency_trading_dict[currency_id],
                                                          kurs_sell__gt=0) \
                                                          .values("name_currency_id",
                                                                  "name_currency_sale_id",
                                                                  "name_currency_sale_currency",
                                                                  "kurs_sell").annotate(kurs_sell_inverse=1/F("kurs_sell"),name_currency_currency=Name_Currency.objects.filter(is_active=True, id=currency_id).values("currency"))

    print("queryset покупаемых валют:", name_currences_purchases_trades)
    print("queryset продаваемых валют:", name_currences_sells)
    print("queryset продаваемых наименований для выбора иконок валют:", name_currences_sells_img)
    print("queryset продаваемых резервов валют:", balance_currences)

    # добавляем в словарь return_dict пустой список с индексом currency_sell
    return_dict["currency_sell"] = list()
    # заносим списки продаваемых валют в словарь для передачи ajax в скрипт list_currencies_sell.js
    for item in name_currences_sells:
        currency_dict = dict()
        currency_dict["id"] = item["name_currency_sale_id"]  # id продаваемой валюты
        for item_img in name_currences_sells_img:
            if item["name_currency_sale_id"] == item_img.id:
                currency_dict["image_currency"] = item_img.image_currency.url  # img продаваемой валюты
        currency_dict["currency"] = item["name_currency_sale_currency"]  # название продаваемой валюты
        currency_dict["kurs_sell"] = item["kurs_sell"]  # курс продаваемой валюты
        currency_dict["kurs_sell_inverse"] = item["kurs_sell_inverse"] # обратный курс продаваемой валюты
        currency_dict["name_currency_currency"] = item["name_currency_currency"] # название покупаемой валюты
        for item_balance in balance_currences:
            if item["name_currency_sale_id"] == item_balance["name_currency_id"]:
                currency_dict["balance_amount"] = item_balance["balance_amount"]  # резерв(баланс,остаток) продаваемой валюты
        currency_dict["url1"] = "/form_exchange/"  # url для перехода по ссылке href на страницу обмена выбранных валют для обмена клиентом
        # добавляем словарь product_dict в словарь return_dict с индексом currency_sell
        return_dict["currency_sell"].append(currency_dict)
    # добавляем в словарь return_dict пустой список с индексом currency_purchase
    return_dict["currency_purchase"] = list()
    # заносим в список покупаемую валюту в словарь для передачи ajax в скрипт list_currencies_sell.js
    currency_dict = dict()
    for name_currence_purchase in name_currence_purchases:
        currency_dict["name_currences_purchase_currency"] = name_currence_purchase["currency"]
        currency_dict["name_currences_purchase_id"] = name_currence_purchase["id"]
        currency_dict["name_currences_purchase_market_exchange_id"] = name_currence_purchase["market_exchange_id"] # принадлежность бирже
    return_dict["currency_purchase"].append(currency_dict)
    print("Словарь продаваемых валют с ключом currency_sell:", return_dict)


    """   не использую т.к. поменялась логика и структура таблиц БД
    name_currences_purchases_trades = Name_Currency.objects.filter(is_active=True).order_by("id").values("id")  # покупаемые валюты словарь только id
    # all_currences_tradings = Name_Currency_Trading.objects.filter(is_active=True).values("name_currency_id","name_currency_sale_id")  # продаваемые валюты связка(не использую эту таблицу так как изменилась логика поля перешли в табл курсов валют)
    all_currences_tradings = Prices_Currency.objects.filter(is_active=True).values("name_currency_id", "name_currency_sale_id")  # продаваемые валюты связка
    # проходим по справочнику покупаемых валют
    for name_currences_purchases_trade in name_currences_purchases_trades:
        kurs_sell_currency_list.append(name_currences_purchases_trade["id"])
        # проходим по справочнику связанных валют покупки-продажи
        all_currency_trading_list = list()  # определяем переменную как список(доступ к элементам по индексу)
        for all_currences_trading in all_currences_tradings:
            # если id справочника покупаемой валюты совпадает с id покупаемой валюты в справочнике связанных валют
            #  то заносим в список id связанной с покупаемой-продаваемой валдюты
            if name_currences_purchases_trade["id"] == all_currences_trading["name_currency_id"]:
                all_currency_trading_list.append(all_currences_trading["name_currency_sale_id"])


        # в словарь соответствий покупаемой продаваемым валютам заносим запись где ключ это покупаемая валюта
        # а значение это список продаваемых валют
        all_currency_trading_dict[name_currences_purchases_trade["id"]] = all_currency_trading_list

    print("Словарь соответствий id покупаемой валюты - списку id продаваемых валют: ", all_currency_trading_dict)
    # проверяем есть ли соответствия покупаемой и продаваемой валюты в справочнике соответствий
    
    
    if currency_id > 0:
        # задаем список продаваемых валют соответствующий выбранной покупаемой валюте
        # проверяем если не задан курс или резерв(остаток) то продаваемая валюта не отражается на странице
        name_currences_sells = Name_Currency.objects.filter(is_active=True,
                                                            id__in=all_currency_trading_dict[currency_id],
                                                            prices_currency__is_active=True,
                                                            balance_currency__is_active=True) \
            .values("id", "currency", "prices_currency__kurs_sell", "balance_currency__balance_amount")
        print("Список QuerySet продаваемых валют:", name_currences_sells)
        
        name_currences_sells_img = Name_Currency.objects.filter(is_active=True, id__in=all_currency_trading_dict[currency_id])
       
        
        # добавляем в словарь return_dict пустой список с индексом currency_sell
        return_dict["currency_sell"] = list()
        # заносим списки продаваемых валют в словарь для передачи ajax в скрипт list_currencies_sell.js
        for item in name_currences_sells:
            currency_dict = dict()
            currency_dict["id"] = item["id"] # id продаваемой валюты
            for item_img in name_currences_sells_img:
                if item["id"] == item_img.id:
                    currency_dict["image_currency"] = item_img.image_currency.url # img продаваемой валюты
            currency_dict["currency"] = item["currency"] # название продаваемой валюты
            currency_dict["kurs_sell"] = item["prices_currency__kurs_sell"] # курс продаваемой валюты
            currency_dict["balance_amount"] = item["balance_currency__balance_amount"] # резерв(баланс,остаток) продаваемой валюты
            currency_dict["url1"] = "/form_exchange/" # url для перехода по ссылке href на страницу обмена выбранных валют для обмена клиентом
            # добавляем словарь product_dict в словарь return_dict с индексом currency_sell
            return_dict["currency_sell"].append(currency_dict)
        # добавляем в словарь return_dict пустой список с индексом currency_purchase
        return_dict["currency_purchase"] = list()
        # заносим в список покупаемую валюту в словарь для передачи ajax в скрипт list_currencies_sell.js
        currency_dict = dict()
        for name_currence_purchase in name_currence_purchases:
            currency_dict["name_currences_purchase_currency"] = name_currence_purchase["currency"]
            currency_dict["name_currences_purchase_id"] = name_currence_purchase["id"]
        return_dict["currency_purchase"].append(currency_dict)
     """


    return JsonResponse(return_dict)

'''
Вариант когда используем стандартные формы регистрации django
тогда в navbarreg.html :
<form method="post">
  {% csrf_token %}
  {{ user_form.as_p }}
  {{ profile_form.as_p }}
  <button type="submit">Save changes</button>
</form>

Для краткости кода вы можете использовать декоратор login_required():
Функция login_required() делает следующее:
Если пользователь не авторизован, то перенаправляет его на URL, указанный в параметре конфигурации settings.LOGIN_URL, 
передавая текущий абсолютный путь в запросе. Например: /accounts/login/?next=/polls/3/.
Если пользователь авторизован, то выполняет код представления. 
В коде представления не требуется выполнять проверку авторизован ли пользователь или нет.

Django предоставляет один API для управления транзакциями базы данных.
atomic(using=None, savepoint=True)
Атомарность является основным свойством транзакций базы данных. 
atomic позволяет создать блок кода, для которого гарантируется атомарность операций над базой данных. 
Если этот блок кода выполнился без ошибок, все изменения фиксируются в базе данных. 
Если произошла ошибка, все изменений будут отменены.

from django.contrib.auth.decorators import login_required
from django.db import transaction

@login_required
@transaction.atomic
def Registration(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Регистрационные данные Вашего профиля обновлены!')
            return redirect('settings:profile')
        else:
            messages.error(request, 'Регистрационные данные не корректны')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'navbarreg.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
'''

# Регистрация на сервере в БД

@transaction.atomic
def Registration(request):
    return_user = dict()
    session_key = request.session.session_key  # переменной session_key присваиваем ключ сессии
    print("Ключ сессии:")
    print(session_key)
    if not session_key:  # Если пользователь не авторизирован то Django в последних версиях не создает ключ сессии
        request.session.cycle_key()  # Команда создания ключа сессии вручную
#        request.session.create()
    print(session_key)
    print("post запрос в Registration от script_reg.js")
    print(request.POST)  # выводим значение post запроса в терминале питона для проверки
    data = request.POST  # переменной data присваиваем значение post запроса(принимаем значения из scripts_reg.js переданные методом AJAX)
    reg_mail = data.get("reg_mail")  # переменной reg_mail присваиваем значение индекса reg_mail списка data
    reg_login = data.get("reg_login")  # переменной reg_login присваиваем значение индекса reg_login списка data
    reg_pass = data.get("reg_pass")  # переменной reg_pass присваиваем значение индекса reg_pass списка data
    reg_pass2 = data.get("reg_pass2")  # переменной reg_pass2 присваиваем значение индекса reg_pass2 списка data
    reg_phone = data.get("reg_phone")  # переменной reg_phone присваиваем значение индекса reg_phone списка data
    # now = datetime.datetime.now() # Время последнего входа пользователя
    vreg = data.get("vreg") # переменной vreg присваиваем значение индекса vreg списка data

    if request.method == 'POST':
       user = authenticate(username=reg_login, password=reg_pass)
       print("Пользователь:")
       print(user)
       if user is not None:
           # Если пользователь с таким логином и паролем в БД уже есть
           if user.is_active and user.profile.active is not False:
               print("Пользователь действителен, активен и аутентифицирован")
               return_user["login"] = reg_login
               return_user["password"] = reg_pass
               return_user["vreg"] = 1
#               user.last_login = now
#               user.save(update_fields=['last_login']) # обновляем время последнего входа пользователя
               auth.login(request, user)
               return JsonResponse(return_user)
           else:
               print("Пользователь с такими данными не активирован")
               return_user["login"] = 'Гость'
               return_user["vreg"] = 7
               return JsonResponse(return_user)

       else:
           if (user is None) and (vreg == '2'):
               # Если пользователя с таким именем и паролем в БД нет
               print(is_email(reg_mail))
               # Проверяем на корректный Email (функция is_email описана ниже)
               if is_email(reg_mail):
                   pass
               else:
                   print("Не корректный email")
                   return_user["login"] = 'Гость'
                   return_user["vreg"] = 4
                   return JsonResponse(return_user)
               # Проверяем на соответствие поля телефонному номеру
               if re.compile("^([0-9\(\)\/\+ \-]*)$").search(smart_text(reg_phone)):
                   pass
               else:
                   print("Не корректный номер телефона")
                   return_user["login"] = 'Гость'
                   return_user["vreg"] = 4
                   return JsonResponse(return_user)
               # Проверяем на совпадение пароля и подтверждающего пароля
               if reg_pass == reg_pass2:
                   pass
               else:
                   print("Не совпадает подтверждающий пароль")
                   return_user["login"] = 'Гость'
                   return_user["vreg"] = 4
                   return JsonResponse(return_user)
               # Проверяем email на уникальность User.objects.filter(email=reg_mail).exclude(username=reg_login).count()
               # убрал exclude так как проверяю и уникальный mail и уникальный login, если разрешить разные login с одинаковыми mail тогда применяем exclude
               if User.objects.filter(email=reg_mail).count() == 0:
                   pass
               else:
                   print("Такой email уже зарегистрирован")
                   return_user["login"] = 'Гость'
                   return_user["vreg"] = 5
                   return JsonResponse(return_user)
               # Проверяем логин на уникальность
               if User.objects.filter(username=reg_login).count() == 0:
                   pass
               else:
                   print("Такой login уже зарегистрирован")
                   return_user["login"] = 'Гость'
                   return_user["vreg"] = 6
                   return JsonResponse(return_user)
               print("Регистрируем нового пользователя")
               user = User.objects.create_user(reg_login, reg_mail, reg_pass)
               # user.last_login = now
               # Далее можем дополнительно заносить данные в другие поля
               # например user.last_name = 'Lennon',  user.profile.birth_date = '2000-02-20'
               user.profile.session_key = session_key
               user.profile.phone = reg_phone
               #user.profile.location = request.META['REMOTE_ADDR'] # ip пользователя
               user.profile.location = get_client_ip(request) # ip пользователя через функцию
               user.profile.active = False
               user.save()
               return_user["login"] = reg_login
               return_user["password"] = reg_pass
               return_user["vreg"] = 2
               messages.success(request, 'Регистрационные данные Вашего профиля обновлены!')
               # auth.login(request, user)
               # Отправка ссылки подтверждения по email для активации пользователя (здесь не использую)
               # (прописана в models.py(после новой записи в базу идет отправка на почту))
               #post_url = request.build_absolute_uri()
               #subject = "Активация учетной записи Chgskv.com"
               #msg = "Добрый день! Для активации регистрации перейдите по этой ссылке "+post_url
               #send_mail(subject, msg, settings.EMAIL_HOST_USER, [reg_mail], fail_silently=False)
               # ------------------------------------------------------------------
               return JsonResponse(return_user)

           else:
               if (vreg == '3'):
                   print("Пользователь вышел")
                   return_user["login"] = 'Гость'
                   return_user["vreg"] = 3
                   auth.logout(request)
                   return JsonResponse(return_user)

               else:
                   print("Пользователь с такими данными не зарегистрирован")
                   return_user["login"] = 'Гость'
                   return_user["vreg"] = 0
                   return JsonResponse(return_user)


# Функция получения ip пользователя
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

# Функция проверки(валидации) Email, метод django EmailValidator
def is_email(value):
    try:
        EmailValidator()(value)
    except ValidationError:
        return False
    else:
        return True

# Функция верификации по email пользователя
def Verify(request, uuid):
    try:
        profile = Profile.objects.get(verification_uuid=uuid, active=False)
        user = User.objects.get(id=profile.user_id)
        print(profile)
        print(user)
        print(user.profile.active)
        user.profile.active = True
        user.save()
        auth.login(request, user)
        return render(request, 'home.html', locals())
    except Profile.DoesNotExist:
        raise Http404("Пользователь отсутствует или уже верифицирован!")



# Функция для отображения страницы обмена выбранных клиентом валют
# Пакет для работы с API биржи Poloniex
# инициализация pip install poloniex(https://pypi.org/project/poloniex/)
def form_exchange(request, currence_purchase_id, currence_sell_id):
    print("ID покупаемой валюты: ", currence_purchase_id)
    print("ID продаваемой валюты: ", currence_sell_id)
    # клиент отдает криптовалюту
    name_currences_purchase = Name_Currency.objects.filter(is_active=True, id=currence_purchase_id) \
                                                           .values("id","currency","wallet")
    for currences_by in name_currences_purchase:
        currence_by=currences_by
    # клиент получает криптовалюту
    name_currences_sell = Name_Currency.objects.filter(is_active=True, id=currence_sell_id).values("id","currency")
    for currences_sell in name_currences_sell:
        currence_sell = currences_sell
    # курс выбранной пары криптовалют для обмена
    currencys_pair_exchange_rate = Prices_Currency.objects.filter(is_active=True,
                                                                  name_currency_id=currence_purchase_id,
                                                                  name_currency_sale_id=currence_sell_id) \
                                                                  .values("name_currency_id",
                                                                          "name_currency_sale_id",
                                                                          "kurs_sell", "min_buy", "max_buy",
                                                                          "id_pair_market", "market_exchange_id")
    for currency_pair_exchange_rate in currencys_pair_exchange_rate:
        currencypair_exchange_rate = currency_pair_exchange_rate
    exchange_kurs_sell = round(currencypair_exchange_rate["kurs_sell"],8)
    exchange_kurs_sell_inverse = round(1 / currencypair_exchange_rate["kurs_sell"], 8)
    # счета фиатных валют
    # если пара валют в справочнике курсов не принадлежит ни одной торговой площадке(бирже)(здесь 1-Poloniex,2-Binance,3-Nomarket[фиатные валюты])
    if currencypair_exchange_rate["market_exchange_id"] == 3:
        wallet_bank_buy = Fiat_Wallet.objects.filter(is_active=True, name_currency_id=currence_purchase_id).order_by("id")
        # получаем только первую запись
        placeholder_bank_buy = Fiat_Wallet.objects.filter(is_active=True, name_currency_id=currence_purchase_id).first()
        wallet_bank_sell = Fiat_Wallet.objects.filter(is_active=True, name_currency_id=currence_sell_id).order_by("id")
        # получаем только первую запись
        placeholder_bank_sell = Fiat_Wallet.objects.filter(is_active=True, name_currency_id=currence_sell_id).first()

    # остаток(резерв) продаваемой криптовалюты
    balance_currences_sell = Balance_Currency.objects.filter(is_active=True, name_currency_id=currence_sell_id) \
                                                             .values("name_currency_id",
                                                                     "balance_amount")
    for balance_currence_sell in balance_currences_sell:
        balancecurrence_sell = balance_currence_sell

    min_sell = round(currencypair_exchange_rate["min_buy"] / currencypair_exchange_rate["kurs_sell"],2)  # минимум получаемой валюты
    max_sell = round(currencypair_exchange_rate["max_buy"] / currencypair_exchange_rate["kurs_sell"],2)  # максимум получаемой валюты

    print("курс выбранной пары криптовалют для обмена", currencypair_exchange_rate)
    print("остаток(резерв) продаваемой криптовалюты", balancecurrence_sell)

    return_dict = dict()  # переменную return_dict определяем как словарь
    all_currency_trading_dict = dict()  # определяем переменную как словарь(доступ к элементам по ключам)
    all_currencys_by_list = list()  # список покупаемых валют, определяем переменную как список(доступ к элементам по индексу)
    all_currences_tradings = Prices_Currency.objects.filter(is_active=True).order_by("name_currency_id") \
                                                                           .values("name_currency_id",
                                                                                   "name_currency_sale_id",
                                                                                   "kurs_sell", "is_active")  # криптовалюты пары покупка-продажа
    all_currences_balans = Balance_Currency.objects.filter(is_active=True).values("name_currency_id",
                                                                                  "balance_amount")  # список резерва(остатков валют)
    # проходим по справочнику курсов пар криптовалют покупки-продажи
    for all_currences_trading in all_currences_tradings:
        currency_by_id = 0
        # если курс продажи установлен(не ноль) и запись активна
        if all_currences_trading["kurs_sell"] != 0 and all_currences_trading["is_active"] == True:
            # проходим по списку резерва(остатков) криптовалют
            for all_currence_balans in all_currences_balans:
                # если id продаваемой валюты пары есть в справочнике резервов(остатка) и остаток не равен нулю
                if all_currences_trading["name_currency_sale_id"] == all_currence_balans["name_currency_id"] and \
                        all_currence_balans["balance_amount"] > 0:
                    # если такой валюты нет в списке покупаемых валют
                    if all_currences_trading["name_currency_id"] not in all_currencys_by_list:
                        # то заносим в список покупаемых валдют id покупаемой валюты
                        all_currencys_by_list.append(all_currences_trading["name_currency_id"])
                        currency_by_id = all_currences_trading[
                            "name_currency_id"]  # переменной присваиваем id покупаемой валюты
                        # if i == 0: # если еще нет списка продаваемых валют
                        all_currencys_sell_list = list()  # список продаваемых валют, определяем переменную как список(доступ к элементам по индексу)
                        # проходим по справочнику курсов пар криптовалют покупки-продажи для поиска соответствий покупаемой валюте-продаваемых валют
                        for all_currences_trading in all_currences_tradings:
                            # находим все пары где id покупаемой валюты равно id переменной
                            if currency_by_id == all_currences_trading["name_currency_id"]:
                                # проходим по списку резерва(остатков) криптовалют
                                for all_currence_balans in all_currences_balans:
                                    # если id продаваемой валюты пары есть в справочнике резервов(остатка) и остаток не равен нулю
                                    if all_currences_trading["name_currency_sale_id"] == all_currence_balans["name_currency_id"] and all_currence_balans["balance_amount"] > 0:
                                        # то заносим в список id продаваемых криптовалдют соответствующие покупаемой
                                        all_currencys_sell_list.append(all_currences_trading["name_currency_sale_id"])
                                        # i = 1 # устанавливаем индикатор в 1(делаем список продаваемых криптовалют только для первой покупаемой валюты которая активна и курс продажи продаваемых не ноль)

                        # в словарь соответствий покупаемой продаваемым валютам заносим запись где ключ это покупаемая валюта
                        # а значение это список продаваемых валют
                        all_currency_trading_dict[currency_by_id] = all_currencys_sell_list

    print("Словарь соответствий id покупаемой валюты - списку id продаваемых валют: ", all_currency_trading_dict)
    print("список покупаемых валют с курсом и у кот в паре остаток не 0", all_currencys_by_list)
    print("список продаваемых валют соответств выбранной покупаемой с курсом и в паре остат не 0", all_currency_trading_dict[int(currence_purchase_id)])

    # список(queryset) наименования продаваемых валют для select из form_exchange.html
    name_currences_sells_img = Name_Currency.objects.filter(is_active=True,
                                                            id__in=all_currency_trading_dict[int(currence_purchase_id)])
    # задаем список(queryset) покупаемых валют для select из form_exchange.html
    name_currences_purchases_trades = Name_Currency.objects.filter(is_active=True, id__in=all_currencys_by_list) \
                                                                   .order_by("id")

    print("queryset покупаемых валют:", name_currences_purchases_trades)
    print("queryset продаваемых наименований для выбора иконок валют:", name_currences_sells_img)


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
    #currencies = polo.returnCurrencies()

    #order = polo.returnLoanOrders('TRX')
    #print(tik)



    return render(request, 'form_exchange.html', locals())


# Функция для отображения страницы результата обмена
def Exchange_currency_result(request, currency_by_id, currency_sell_id):
    print("post запрос в Exchange_currency_result от формы form_exchange.html ")
    if request.POST:
        # выводим значение post запроса в терминале питона для проверки
        print(request.POST)
        data = request.POST  # переменной data присваиваем значение post запроса
        sum_currency_by = data.get('sum_by') # сумма покупки валюты у клиента
        print(sum_currency_by)
        sum_currency_sell = data.get('sum_sell')  # сумма продажи валюты клиенту(откупаем на бирже)
        print(sum_currency_sell)
        # переменная currency_by_id из формы form_exchange.html
        print(currency_by_id) # id покупаемой валюты
        name_currences_by = Name_Currency.objects.filter(is_active=True, id=currency_by_id)
        for currences_by in name_currences_by:
            currence_by = currences_by
        # переменная currency_sell_id из формы form_exchange.html
        print(currency_sell_id) # id продаваемой валюты
        name_currences_sell = Name_Currency.objects.filter(is_active=True, id=currency_sell_id)
        for currences_sell in name_currences_sell:
            currence_sell = currences_sell
        wallet_by = data.get('wallet_by')  # кошелек клиента
        print(wallet_by)
        wallet_sell = data.get('wallet_sell')  # кошелек продавца
        print(wallet_sell)
        market = int(data.get('market'))  # принадлежность пары фиатным валютам(3-фиатные)
        print(market)
        # если пара валют фиатная
        if market == 3:
            name_bank_buy = data.get('name_bank_buy')
            print(name_bank_buy)
            name_bank_sell = data.get('name_bank_sell')
            print(name_bank_sell)
        email = data.get('email')  # кошелек продавца
        print(email)
        notify = data.get('notify')  # индикатор запоминать email или нет
        print(notify)
        # курс выбранной пары валют
        currencys_pair_exchange_rate = Prices_Currency.objects.filter(is_active=True,
                                                                      name_currency_id=currency_by_id,
                                                                      name_currency_sale_id=currency_sell_id) \
                                                                        .values("name_currency_id",
                                                                                "name_currency_sale_id",
                                                                                "kurs_sell", "min_buy", "max_buy",
                                                                                "id_pair_market")
        for currency_pair_exchange_rate in currencys_pair_exchange_rate:
            currencypair_exchange_rate = currency_pair_exchange_rate
        exchange_kurs_sell = round(currencypair_exchange_rate["kurs_sell"], 8)
        exchange_kurs_sell_inverse = round(1 / currencypair_exchange_rate["kurs_sell"], 8)
        # остаток(резерв) продаваемой криптовалюты
        balance_currences_sell = Balance_Currency.objects.filter(is_active=True, name_currency_id=currency_sell_id) \
                                                                    .values("name_currency_id",
                                                                            "balance_amount")



    return render(request, 'exchange_currency_result.html', locals())

# Функция для формирования заявки обмена валют
def Exchange_currency_bid(request, currency_by_id, currency_sell_id):
    print("post запрос в Exchange_currency_bid от формы exchange_currency_result.html ")
    if request.POST:
        # выводим значение post запроса в терминале питона для проверки
        print(request.POST)
        data = request.POST  # переменной data присваиваем значение post запроса
        # Текущий юзер—это request.user Объект request во вьюхе есть по определению,его не надо передавать из шаблона
        id_user = request.user.id # id текущего пользователя
        print(id_user)
        if not id_user:
            id_user = 0
        sum_currency_by = data.get('sum_by')  # сумма покупки валюты у клиента
        print(sum_currency_by)
        sum_currency_sell = data.get('sum_sell')  # сумма продажи валюты клиенту(откупаем на бирже)
        print(sum_currency_sell)
        # переменная currency_by_id из формы form_exchange.html
        print(currency_by_id)  # id покупаемой валюты
        name_currences_by = Name_Currency.objects.filter(is_active=True, id=currency_by_id).values("id","currency","wallet")
        for currences_by in name_currences_by:
            currence_by = currences_by
        # переменная currency_sell_id из формы form_exchange.html
        print(currency_sell_id)  # id продаваемой валюты
        name_currences_sell = Name_Currency.objects.filter(is_active=True, id=currency_sell_id).values("id","currency")
        for currences_sell in name_currences_sell:
            currence_sell = currences_sell
        # курс выбранной пары валют
        currencys_pair_exchange_rate = Prices_Currency.objects.filter(is_active=True,
                                                                      name_currency_id=currency_by_id,
                                                                      name_currency_sale_id=currency_sell_id) \
                                                                        .values("id_pair_market")
        for currency_pair_exchange_rate in currencys_pair_exchange_rate:
            currencypair_exchange_rate = currency_pair_exchange_rate
        wallet_by = data.get('wallet_by')  # кошелек клиента
        print(wallet_by)
        wallet_sell = data.get('wallet_sell')  # кошелек продавца
        print(wallet_sell)
        market = int(data.get('market'))  # принадлежность пары фиатным валютам(3-фиатные)
        print(market)
        # если пара валют фиатная
        if market == 3:
            name_bank_buy = data.get('name_bank_buy')
            print(name_bank_buy)
            name_bank_sell = data.get('name_bank_sell')
            print(name_bank_sell)
        else:
            name_bank_buy = "Nofiat"
        email = data.get('email')  # mail продавца
        print(email)
        notify = data.get('notify')  # индикатор запоминать email или нет
        print(notify)
        # курс выбранной пары валют
        exchange_kurs_sell = data.get('exchange_kurs_sell')
        print(exchange_kurs_sell)
        print("добавляем заявку в БД Реестр заявок на обмен Exchange_List")
        # status=1, где 1 - статус заявки: Принята, ожидает оплаты клиентом
        if market == 3:
            wallet_bank_buy = Fiat_Wallet.objects.filter(is_active=True, name_currency_id=currency_by_id, name_bank=name_bank_buy).values("wallet_bank")
            for wallets in wallet_bank_buy:
                wallet = wallets
            wallet_fact = wallet["wallet_bank"]
        else:
            wallet_fact = currence_by["wallet"]

        request_id = Exchange_List.objects.create(id_user=id_user, id_pair_market=currencypair_exchange_rate["id_pair_market"],
                                     name_currency_buy_id=currency_by_id, name_currency_buy_currency=currence_by["currency"],
                                     sum_currency_buy=sum_currency_by, wallet_currency_buy=wallet_by,
                                     name_currency_sell_id=currency_sell_id, name_currency_sell_currency=currence_sell["currency"],
                                     sum_currency_sell=sum_currency_sell, wallet_currency_sell=wallet_sell,
                                     kurs_sell=exchange_kurs_sell, wallet_fact=wallet_fact, status=1,
                                     is_active=True)
            
        # отправляем сообщение о заявке в телеграмм
        # Ставим сообщение в очередь.
        # узнать свой id , в телеграмм набрать get my id, затем /start
        # Оно будет отослано моему боту в переписку (чат) с ID 1156354914.
        # отправка сообщения python manage.py sitemessage_send_scheduled (периодически запускать в cron, celery или др. обработчике)
        if market == 3:
            schedule_messages('Новая заявка на обмен! Id = ' + str(request_id.pk) + ' Email: ' + email +
                              ' Отдает: ' + str(sum_currency_by) + ' ' + currence_by["currency"] +
                              ' С карты: ' + str(wallet_by) + ' ' + str(name_bank_buy) +
                              ' Получает: ' + str(sum_currency_sell) + ' ' + currence_sell["currency"] +
                              ' На карту: ' + wallet_sell + ' ' + str(name_bank_sell)
                              , recipients('telegram', '1156354914'))
        else:
            schedule_messages('Новая заявка на обмен! Id = ' + str(request_id.pk) + ' Email: ' + email +
                              ' Отдает: ' + str(sum_currency_by) + ' ' + currence_by["currency"] +
                              ' Со счета: ' + str(wallet_by) + ' ' +
                              ' Получает: '+str(sum_currency_sell)+' ' + currence_sell["currency"]+
                              ' На счет: ' + wallet_sell
                              , recipients('telegram', '1156354914'))



        # Message to a channel mychannel
        #schedule_messages('Новая заявка на обмен!!', recipients('telegram', '@obmen_skv_bot'))

    return render(request, 'exchange_currency_bid.html', locals())


# Функция для формирования заявки с номером ID для обмена клиентом выбранных валют и суммы перед оплатой с обновлением страницы
def Exchange_currency_bid_info(request, request_id, market, name_bank_buy):
    print("post запрос в Exchange_currency_bid_info от формы exchange_currency_bid.html ")
    print("ID заявки: ", request_id)
    market = int(market)
    #print(name_bank_buy)
    exchange_requests = Exchange_List.objects.filter(is_active=True, pk=request_id)
    for exchange_request in exchange_requests:
        exchange = exchange_request

    if request.is_ajax():
        return_izm = dict()
        print(request.POST)
        data = request.POST  # переменной data присваиваем значение post запроса
        request_id = data.get("request_id")
        exchange_requests = Exchange_List.objects.filter(is_active=True, pk=request_id)
        for exchange_request in exchange_requests:
            exchange = exchange_request
        return_izm["request_id"] = request_id # возвращаем номер заявки
        return_izm["status"] = exchange.status # возвращаем статус заявки
        return_izm["market"] = market  # возвращаем принадлежность к фиатным валютам
        return_izm["name_bank_buy"] = name_bank_buy  # возвращаем наименование банка карты платежа


        return JsonResponse(return_izm)


    return render(request, 'exchange_currency_bid_info.html', locals())


# Функция для оплаты клинтом сформированной заявки
def Exchange_currency_pay(request, request_id):
    print("post запрос в Exchange_currency_pay от формы exchange_currency_bid_info.html ")
    if request.POST:
        # выводим значение post запроса в терминале питона для проверки
        print(request.POST)
        data = request.POST  # переменной data присваиваем значение post запроса
        # Текущий юзер—это request.user Объект request во вьюхе есть по определению,его не надо передавать из шаблона
        id_user = request.user.id # id текущего пользователя
        wallet_fact = data.get("wallet_fact") # кошелек(счет) на который клиент переводит валюту для покупки на бирже(мой кошелек)
        name_currency_buy = data.get("name_currency_buy") # валюта которую клиент отдает
        name_currency_sell = data.get("name_currency_sell") # валюта которую клиент получает
        sum_currency_buy = data.get("sum_currency_buy") # сумма которую клиент отдает
        request_id = int(data.get("request_id"))  # id заявки на обмен
        market = int(data.get("market"))  # принадлежность к фиатным валютам
        name_bank_buy = data.get("name_bank_buy")  # возвращаем наименование банка карты платежа

        # генерация изображения qr кода
        qr_img = qrcode.make(wallet_fact) # генерируем qr-код кошелька на который клиент переводит валюту
        qr_img.save(django_settings.QR_ROOT+"qr.png") # сохраняем файл в директорию указанную QR_ROOT в settings.py
        exchanges = Exchange_List.objects.filter(pk=request_id).values("status")
        for exchange in exchanges:
            status = exchange
        status = int(status["status"]) # статус заявки



    return render(request, 'exchange_currency_pay.html', locals())


# Функция определения наличия пары для обмена при выборе select на странице обмена form_exchange.html
def Exchange_currency_select_by(request):
    return_izm = dict()
    print("post запрос в Exchange_currency_select_by от exchange_currency.js")
    if request.POST:
        # выводим значение post запроса в терминале питона для проверки
        print(request.POST)
        data = request.POST  # переменной data присваиваем значение ajax запроса
        # переменной currency_by_id присваиваем значение из ajax функции Exchange_Currencies_Updating скрипта exchange_currency.js
        currency_by_id = int(data.get("currency_by_id")) # id покупаемой валюты
        name_currences_by = Name_Currency.objects.filter(is_active=True, id=currency_by_id).values("id")
        for name_currence_by in name_currences_by:
            currence_by = name_currence_by
        # переменной currency_sell_id присваиваем значение из ajax функции Exchange_Currencies_Updating скрипта exchange_currency.js
        currency_sell_id = int(data.get("currency_sell_id")) # id продаваемой валюты
        name_currences_sell = Name_Currency.objects.filter(is_active=True, id=currency_sell_id).values("id")
        for name_currence_sell in name_currences_sell:
            currence_sell = name_currence_sell
        # курс выбранной пары валют
        currencys_pair_exchange_rate = Prices_Currency.objects.filter(is_active=True,
                                                                      name_currency_id=currency_by_id,
                                                                      name_currency_sale_id=currency_sell_id)
        print("наличие выбранной пары для обмена", currencys_pair_exchange_rate)
        print(len(currencys_pair_exchange_rate))
        if len(currencys_pair_exchange_rate) == 0:
            # если нет такой пары, то получаем список пар валют для покупаемой валюты
            currencys_pairs_exchange = Prices_Currency.objects.filter(is_active=True, name_currency_id=currency_by_id).order_by("name_currency_id").values("name_currency_id", "name_currency_sale_id", "kurs_sell")  # криптовалюты пары покупка-продажа
            i = 0 # индикатор
            # проходим по списку
            for item in currencys_pairs_exchange:
                # если курс не ноль
                if item["kurs_sell"] > 0 and i == 0:
                    # получаем список резерва
                    all_currences_balans = Balance_Currency.objects.filter(is_active=True, name_currency_id=item["name_currency_sale_id"]).values("name_currency_id", "balance_amount")  # список резерва(остатков валют)
                    # проходим по списку
                    for item1 in all_currences_balans:
                        # проверяем чтоб баланс(резерв) был не равен ноль
                        if item1["balance_amount"] > 0:
                            return_izm["result_pair_currencies"] = 0  # 0 - нет такой пары
                            return_izm["name_currences_by"] = currence_by
                            return_izm["name_currences_sell"] = item["name_currency_sale_id"] # передаем новый id продаваемой валюты соответствующий покупаемой
                            i = 1  # первый id продаваемой соответствующий покупаемой найден то выходим из всех циклов
                            break
                else:
                    break

        else:
            return_izm["result_pair_currencies"] = 1  # 1 - есть такая пара
            return_izm["name_currences_by"] = currence_by
            return_izm["name_currences_sell"] = currence_sell

        print(return_izm)

        return JsonResponse(return_izm)



# Функция аннулирования заявки клиента на обмен на странице exchange_currency_bid_info.html по кнопке input value="Отменить заявку"
def Exchange_request_del(request):
    return_izm = dict()
    print("post запрос в Exchange_request_del от exchange_result.js")
    if request.POST:
        # выводим значение post запроса в терминале питона для проверки
        print(request.POST)
        data = request.POST  # переменной data присваиваем значение ajax запроса
        # переменной currency_by_id присваиваем значение из ajax функции Exchange_Currencies_Updating скрипта exchange_currency.js
        request_id = int(data.get("request_id"))  # id заявки на обмен
        exchange = Exchange_List.objects.get(pk=request_id)
        exchange.status = 0
        exchange.save()
        exchanges = Exchange_List.objects.filter(pk=request_id).values("updated")
        exchange in exchanges
        date = localtime(exchange.updated).strftime('%d.%m.%Y, %H:%M')
        print(date)
        #date = datetime.datetime.today()
        return_izm["result"] = 0  # 0 - заявка аннулирована
        return_izm["updated"] = date
        print(return_izm)

        return JsonResponse(return_izm)


# -----------------------------------------------------------------------------------------------------------------------
# Просмотр БД Техобслуживание
def Site_maintenance_check(request):
    print("post запрос в Site_maintenance от navbar_kaba.html")
    maintenance = Site_maintenance.objects.get(pk=1)
    print(maintenance)

    return render(request, 'site_maintenance.html', locals())


# Активация сайта на техобслуживание
def Site_maintenance_active(request):
    print("post запрос в Users_clients_active от users_clients.js")
    return_izm = dict()  # определяем переменную как словарь
    if request.POST:
        # выводим значение post запроса в терминале питона для проверки
        print(request.POST)
        data = request.POST  # переменной data присваиваем значение post запроса
        item_id = data.get("item_id")
        # находим запись в реестре заявок по id (номер заявки)
        site_maintenance = Site_maintenance.objects.get(pk=item_id)
        site_maintenance.maintenance = True  # активируем техобслуживание
        site_maintenance.save()

        return_izm["user_id"] = item_id  # передаем id заявки

        return JsonResponse(return_izm)


# Деактивация сайта с техобслуживания
def Site_maintenance_deactivate(request):
    print("post запрос в Users_clients_deactivate от users_clients.js")
    return_izm = dict()  # определяем переменную как словарь
    if request.POST:
        # выводим значение post запроса в терминале питона для проверки
        print(request.POST)
        data = request.POST  # переменной data присваиваем значение post запроса
        item_id = data.get("item_id")
        # находим запись в реестре заявок по id (номер заявки)
        site_maintenance = Site_maintenance.objects.get(pk=item_id)
        site_maintenance.maintenance = False  # деактивируем техобслуживание
        site_maintenance.save()

        return_izm["user_id"] = item_id  # передаем id заявки

        return JsonResponse(return_izm)

# -----------------------------------------------------------------------------------------------------------------------