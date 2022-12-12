from django.shortcuts import render
from .forms import ContactForm,ContactFormPass # ContactForm импортируем из forms.py (не использую т.к. ajax)
from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect,  Http404
import datetime
from .models import Market_Exchange, query_market_exchange_by_args # импортируем таблицу БД Market_Exchange из models.py
from .models import  Name_Currency,query_name_currency_by_args # импортируем таблицу БД Name_Currency из models.py
from .models import  Fiat_Wallet,query_fiat_wallet_by_args # импортируем таблицу БД Fiat_Wallet из models.py
from .models import Prices_Currency, query_prices_currency_by_args # импортируем таблицу БД Prices_Currency из models.py
from .models import Balance_Currency, query_balance_currency_by_args # импортируем таблицу БД Balance_Currency из models.py
from .models import News, query_news_by_args # импортируем таблицу БД News из models.py
from .models import NewsImage, query_newsimage_by_args # импортируем таблицу БД NewsImage из models.py
from .models import Exchange_List, query_exchange_list_by_args # импортируем таблицу БД Exchange_List из models.py
from blok1.models import Profile
#from .models import Name_Currency_Trading, query_name_currency_trading_by_args # импортируем таблицу БД Name_Currency_Trading из models.py
from .serializers import Market_Exchange_Serializer, Name_Currency_Serializer, Fiat_Wallet_Serializer, Prices_Currency_Serializer, Balance_Currency_Serializer, News_Serializer, NewsImage_Serializer, Exchange_List_Serializer #Name_Currency_Trading_Serializer
from rest_framework import viewsets, status
from django.template.response import TemplateResponse
from django.http.response import HttpResponse
from rest_framework.response import Response


# Create your views here.

# Кабинет пользователя
def Account(request):


    return render(request, 'account.html', locals())

'''
# просмотр,редактирование,удаление учетных данных без метода ajax
def Account_user(request):
    # ContactForm импортируем из forms.py
    form = ContactForm(request.POST or None)
    if request.POST:
        # выводим значение post запроса в терминале питона для проверки
        print(request.POST)
        if form.is_valid():  # проверяем все ли правильно в нашей форме отрисованной в account_user.html
            print("форма корректная")  # если все правильно то выводим текст в терминале питона для проверки
            data = request.POST  # переменной data присваиваем значение post запроса
            user = User.objects.get(username=request.user)
            # Текущий юзер—это request.user.Объект request во вьюхе есть по определению,его не надо передавать из шаблона
            # переменной first_name присваиваем значение введеное в поле имя из формы в account_user.html и т.д.
            first_name = data["first_name"]
            last_name = data["last_name"]
            location = data["location"]
            birth_date = data["birth_date"]
            # присваиваем значения полям
            user.first_name = first_name
            user.last_name = last_name
            user.profile.birth_date = birth_date
            user.profile.location = location
            user.save()
        else:
            print("форма некорректна")  # выводим значение в терминале питона для проверки

    return render(request, 'account_user.html', locals())
'''

# просмотр,редактирование,удаление учетных данных
def Account_user(request):
    vreg = 0
    return_izm = dict()
    print("post запрос в Account_user от script_izreg.js")
    if request.POST:
        # выводим значение post запроса в терминале питона для проверки
        print(request.POST)
        data = request.POST  # переменной data присваиваем значение post запроса
        user = User.objects.get(username=request.user)
        # Текущий юзер—это request.user. Объект request во вьюхе есть по определению,его не надо передавать из шаблона
        # переменной first_name присваиваем значение введеное в поле имя из формы в account_user.html и т.д.
        first_name = data.get("izm_fname")
        last_name = data.get("izm_lname")
        #location = data.get("izm_locat")
        birth_date = data.get("izm_bdate")
        # присваиваем значения полям
        user.first_name = first_name
        user.last_name = last_name
        user.profile.birth_date = birth_date
        #user.profile.location = location
        if first_name != "" and last_name != "" and birth_date != "":  # and location != ""
            user.save()
            vreg = 1
        if request.is_ajax():
            return_izm["first_name"] = first_name
            return_izm["last_name"] = last_name
            #return_izm["location"] = location
            return_izm["birth_date"] = birth_date
            return_izm["vreg"] = vreg
            return JsonResponse(return_izm)

    return render(request, 'account_user.html', locals())

'''
# Изменение пароля без метода ajax
def Account_user_pass(request):
    # ContactFormPass импортируем из forms.py
    form = ContactFormPass(request.POST or None)
    if request.POST:
        # выводим значение post запроса в терминале питона для проверки
        print(request.POST)
        if form.is_valid():  # проверяем все ли правильно в нашей форме отрисованной в account_user.html
            print("форма корректная")  # если все правильно то выводим текст в терминале питона для проверки
            data = request.POST  # переменной data присваиваем значение post запроса
            user = User.objects.get(username=request.user)
            # Текущий юзер—это request.user.Объект request во вьюхе есть по определению,его не надо передавать из шаблона
            # переменной first_name присваиваем значение введеное в поле имя из формы в account_user.html и т.д.
            password = data["password"]
            password1 = data["password1"]
            # Проверяем на совпадение пароля и подтверждающего пароля
            if password == password1:
               user.set_password(password)
               user.save()
               auth.login(request, user)
            else:
                print("Не совпадает подтверждающий пароль")
        else:
            print("форма некорректна")  # выводим значение в терминале питона для проверки

    return render(request, 'account_user_pass.html', locals())

'''

# Изменение пароля
def Account_user_pass(request):
    return_izm = dict()
    print("post запрос в Account_user_pass от script_izreg.js")
    # ContactFormPass импортируем из forms.py
    if request.POST:
        # выводим значение post запроса в терминале питона для проверки
        print(request.POST)
        data = request.POST  # переменной data присваиваем значение post запроса
        user = User.objects.get(username=request.user)
        # Текущий юзер—это request.user.Объект request во вьюхе есть по определению,его не надо передавать из шаблона
        # переменной first_name присваиваем значение введеное в поле имя из формы в account_user.html и т.д.
        password = data.get("izm_pass1")
        password1 = data.get("izm_pass2")
        # Проверяем на совпадение пароля и подтверждающего пароля
        if password == password1 and request.is_ajax() and password != "" and password1 != "":
            user.set_password(password)
            user.save()
            auth.login(request, user)
            # флаг vizm = 0 пароль успешно изменен 1 не совпадает
            return_izm["vizm"] = 0
            return JsonResponse(return_izm)
        else:
            if password == "" and password1 == "":
                print("Пароль не может быть пустым")
                return_izm["vizm"] = 2
            else:
                print("Не совпадает подтверждающий пароль")
                return_izm["vizm"] = 1
            return JsonResponse(return_izm)

    return render(request, 'account_user_pass.html', locals())

# Функция проверки корректной введенной пользователем даты
def check_date(year, month, day):
    correctDate = None
    try:
        newDate = datetime.datetime(year, month, day)
        correctDate = True
    except ValueError:
        correctDate = False
    return correctDate

#-----------------------------------------------------------------------------------------------------------------------
#Редактирование справочников с помощью плагина datatables:
    # инсталлируем фрэймворк rest framework, pip install djangorestframework, pip install django-model-utils
    # В settings.py подключаем в INSTALLED_APPS фрэймворк 'rest_framework'
    # отображаем таблицу справочника с помощью плагина datatables.net, подключаем скрипт плагина и его стили в blok1/base.html
    # blok2\models.py - таблица БД
    # blok2\templates\navbar_kaba.html - пункт меню справочника
    # blok2\urls.py - ссылка на функцию выполняемого пункта меню справочника в blok2\views.py
    # blok2\views.py - функция выполняемого пункта меню и класс с функцией list для обмена данными методом ajax с скриптом в js\table_..._.js
    # blok2\serializers.py - сериалайзер формирующий записи таблицы БД в упорядоченный словарь класса OrderedDict
    # chgskv\urls.py - роутер(маршрутизатор DefaultRouter) rest_framework и роутер для класса из blok2\views.py
    # js\table_..._.js - скрипт отрисовки таблицы плагина datatables.net для таблицы БД справочника
    # blok2\templates\..._.html - страница для просмотра,редактирования записей справочника таблицы БД в blok2\models.py вызываемая из navbar_kaba.html
#-----------------------------------------------------------------------------------------------------------------------
# Редактирование справочника торговой площадки(биржи) с помощью плагина таблицы datatables
def MarketExchange(request):
    print("запрос от market_exchange.html")
    user = request.user  # достаем из запроса пользователя для второго уровня проверки(первый в navbar.html)
    reg_gl_menu = 1 # переменная для отрисовки пункта меню "Главная" в blok1/navbarreg.html
    if user.is_superuser:
        html = TemplateResponse(request, 'market_exchange.html', locals())
        return HttpResponse(html.render())

    else:

        return HttpResponseRedirect('/')
            #reversed("home"))  # Иначе перегружаем домашнюю страницу, если ошибка то HttpResponseRedirect('/')

# класс с функцией list для обмена данніми методом ajax с скриптом js/table_market_exchange.js
# обращаемся к классу через роутер в chgskv/urls.py
# queryset атрибут класса для возврата значений объекта табл БД Market_Exchange
# serializer_class атрибут класса для проверки и десериализации ввода, а также для сериализации вывода
class MarketExchange_ViewSet(viewsets.ModelViewSet):
    queryset = Market_Exchange.objects.all()
    # сериалайзер из blok2/serializers.py, преобразует записи из табл БД в упорядоченный словарь класса OrderedDict
    serializer_class = Market_Exchange_Serializer

    def list(self, request, **kwargs):
        try:

            market_exchange = query_market_exchange_by_args(**request.query_params) # функция query_market_exchange_by_args из blok2/models.py
            # переменной присваиваем значения из табл БД сформированные функцией query_market_exchange_by_args из blok2/models.py
            # и обработанные сериалайзером Market_Exchange_Serializer в blok2/serializers.py для отображения(рендерим)
            #  в формате json для ajax запроса из скрипта js/table_market_exchange.js
            #print("Данные для таблицы обработанные функцией query_market_exchange_by_args в model views1: ",market_exchange)
            serializer = Market_Exchange_Serializer(market_exchange['items'], many=True)
            #print("Данные для таблицы обработанные сериалайзером views2: ", serializer)
            result = dict()
            result['data'] = serializer.data
            #print("Данные для таблицы обработанные сериалайзером views3: ", result)
            result['draw'] = market_exchange['draw']
            result['recordsTotal'] = market_exchange['total']
            result['recordsFiltered'] = market_exchange['count']
            print("Данные для таблицы обработанные сериалайзером views4: ", result)

            return Response(result, status=status.HTTP_200_OK, template_name=None, content_type=None)
            #return Response(serializer.data, status=status.HTTP_200_OK, template_name=None, content_type=None)

        except Exception as e:
            return Response(e, status=status.HTTP_404_NOT_FOUND, template_name=None, content_type=None)


#-----------------------------------------------------------------------------------------------------------------------
# Редактирование справочника наименования валют с помощью плагина таблицы datatables
def NameCurrency(request):
    print("запрос от name_currency.html")
    user = request.user  # достаем из запроса пользователя для второго уровня проверки(первый в navbar.html)
    reg_gl_menu = 1 # переменная для отрисовки пункта меню "Главная" в blok1/navbarreg.html
    marketexchange = Market_Exchange.objects.filter(is_active=True)  # переменная для выбора торговой площадки из таблицы БД Market_Exchange для blok2/name_currency.html
    if user.is_superuser:
        html = TemplateResponse(request, 'name_currency.html', locals())
        return HttpResponse(html.render())

    else:

        return HttpResponseRedirect('/')
            #reversed("home"))  # Иначе перегружаем домашнюю страницу, если ошибка то HttpResponseRedirect('/')

# класс с функцией list для обмена данніми методом ajax с скриптом js/table_name_currency.js
# обращаемся к классу через роутер в chgskv/urls.py
# queryset атрибут класса для возврата значений объекта табл БД Name_Currency
# serializer_class атрибут класса для проверки и десериализации ввода, а также для сериализации вывода
class NameCurrency_ViewSet(viewsets.ModelViewSet):
    queryset = Name_Currency.objects.all()
    # сериалайзер из blok2/serializers.py, преобразует записи из табл БД в упорядоченный словарь класса OrderedDict
    serializer_class = Name_Currency_Serializer

    def list(self, request, **kwargs):
        try:

            name_currency = query_name_currency_by_args(**request.query_params) # функция query_name_currency_by_args из blok2/models.py
            # переменной присваиваем значения из табл БД сформированные функцией query_name_currency_by_args из blok2/models.py
            # и обработанные сериалайзером Name_Currency_Serializer в blok2/serializers.py для отображения(рендерим)
            #  в формате json для ajax запроса из скрипта js/table_name_currency.js
            #print("Данные для таблицы обработанные функцией query_name_currency_by_args в model views1: ",name_currency)
            serializer = Name_Currency_Serializer(name_currency['items'], many=True)
            #print("Данные для таблицы обработанные сериалайзером views2: ", serializer)
            result = dict()
            result['data'] = serializer.data
            #print("Данные для таблицы обработанные сериалайзером views3: ", result)
            result['draw'] = name_currency['draw']
            result['recordsTotal'] = name_currency['total']
            result['recordsFiltered'] = name_currency['count']
            print("Данные для таблицы обработанные сериалайзером views4: ", result)

            return Response(result, status=status.HTTP_200_OK, template_name=None, content_type=None)
            #return Response(serializer.data, status=status.HTTP_200_OK, template_name=None, content_type=None)

        except Exception as e:
            return Response(e, status=status.HTTP_404_NOT_FOUND, template_name=None, content_type=None)

        # [Get] api/music/
        # def list(self, request, **kwargs):
        #     try:
        #         name_currency = Name_Currency.objects.all()
        #         serializer = Name_Currency_Serializer(name_currency, many=True)
        #
        #         return Response(serializer.data, status=status.HTTP_200_OK, template_name=None, content_type=None)
        #
        #     except Exception as e:
        #         return Response(e.message, status=status.HTTP_404_NOT_FOUND, template_name=None, content_type=None)
        #


#-----------------------------------------------------------------------------------------------------------------------
# Редактирование справочника наименования валют с помощью плагина таблицы datatables
def FiatWallet(request):
    print("запрос от fiat_wallet.html")
    user = request.user  # достаем из запроса пользователя для второго уровня проверки(первый в navbar.html)
    reg_gl_menu = 1 # переменная для отрисовки пункта меню "Главная" в blok1/navbarreg.html
    namecurrency = Name_Currency.objects.filter(is_active=True, id_market=0)  # переменная для выбора фиатной валюты(id_market=0) из таблицы БД Name_Currency для blok2/fiat_wallet.html
    if user.is_superuser:
        html = TemplateResponse(request, 'fiat_wallet.html', locals())
        return HttpResponse(html.render())

    else:

        return HttpResponseRedirect('/')
            #reversed("home"))  # Иначе перегружаем домашнюю страницу, если ошибка то HttpResponseRedirect('/')

# класс с функцией list для обмена данніми методом ajax с скриптом js/table_fiat_wallet.js
# обращаемся к классу через роутер в chgskv/urls.py
# queryset атрибут класса для возврата значений объекта табл БД Fiat_Wallet
# serializer_class атрибут класса для проверки и десериализации ввода, а также для сериализации вывода
class FiatWallet_ViewSet(viewsets.ModelViewSet):
    queryset = Fiat_Wallet.objects.all()
    # сериалайзер из blok2/serializers.py, преобразует записи из табл БД в упорядоченный словарь класса OrderedDict
    serializer_class = Fiat_Wallet_Serializer

    def list(self, request, **kwargs):
        try:

            fiat_wallet = query_fiat_wallet_by_args(**request.query_params) # функция query_name_currency_by_args из blok2/models.py
            # переменной присваиваем значения из табл БД сформированные функцией query_name_currency_by_args из blok2/models.py
            # и обработанные сериалайзером Fiat_Wallet_Serializer в blok2/serializers.py для отображения(рендерим)
            #  в формате json для ajax запроса из скрипта js/table_fiat_wallet.js
            #print("Данные для таблицы обработанные функцией query_fiat_wallet_by_args в model views1: ",fiat_wallet)
            serializer = Fiat_Wallet_Serializer(fiat_wallet['items'], many=True)
            #print("Данные для таблицы обработанные сериалайзером views2: ", serializer)
            result = dict()
            result['data'] = serializer.data
            #print("Данные для таблицы обработанные сериалайзером views3: ", result)
            result['draw'] = fiat_wallet['draw']
            result['recordsTotal'] = fiat_wallet['total']
            result['recordsFiltered'] = fiat_wallet['count']
            print("Данные для таблицы обработанные сериалайзером views4: ", result)

            return Response(result, status=status.HTTP_200_OK, template_name=None, content_type=None)
            #return Response(serializer.data, status=status.HTTP_200_OK, template_name=None, content_type=None)

        except Exception as e:
            return Response(e, status=status.HTTP_404_NOT_FOUND, template_name=None, content_type=None)


#-----------------------------------------------------------------------------------------------------------------------
# Редактирование справочника курсов валют с помощью плагина таблицы datatables
def PricesCurrency(request):
    print("запрос от prices_currency.html")
    user = request.user  # достаем из запроса пользователя для второго уровня проверки(первый в navbar.html)
    reg_gl_menu = 1  # переменная для отрисовки пункта меню "Главная" в blok1/navbarreg.html
    namecurrency = Name_Currency.objects.filter(is_active=True) # переменная для выбора валюты из таблицы БД Name_Currency для blok2/prices_currency.html
    marketexchange = Market_Exchange.objects.filter(is_active=True)  # переменная для выбора площадки(биржи) из таблицы БД Market_Exchange для blok2/prices_currency.html
    if user.is_superuser:
        html = TemplateResponse(request, 'prices_currency.html', locals())
        return HttpResponse(html.render())

    else:

        return HttpResponseRedirect('/')
            #reversed("home"))  # Иначе перегружаем домашнюю страницу, если ошибка то HttpResponseRedirect('/')


# класс с функцией list для обмена данніми методом ajax с скриптом js/table_prices_currency.js
# обращаемся к классу через роутер в chgskv/urls.py
# queryset атрибут класса для возврата значений объекта табл БД Prices_Currency
# serializer_class атрибут класса для проверки и десериализации ввода, а также для сериализации вывода
class PricesCurrency_ViewSet(viewsets.ModelViewSet):
    queryset = Prices_Currency.objects.all()
    # сериалайзер из blok2/serializers.py, преобразует записи из табл БД в упорядоченный словарь класса OrderedDict
    serializer_class = Prices_Currency_Serializer
    #print("Данные для таблицы обработанные сериалайзер-класс: ",serializer_class)
    def list(self, request, **kwargs):
        try:
            print("request.query_params ", request.query_params)
            prices_currency = query_prices_currency_by_args(**request.query_params)  # функция query_prices_currency_by_args из blok2/models.py
            # переменной присваиваем значения из табл БД сформированные функцией query_prices_currency_by_args из blok2/models.py
            # и обработанные сериалайзером Prices_Currency_Serializer в blok2/serializers.py для отображения(рендерим)
            #  в формате json для ajax запроса из скрипта js/table_prices_currency.
            #print("Данные для таблицы обработанные функцией query_prices_currency_by_args в model views1: ", prices_currency)
            serializer = Prices_Currency_Serializer(prices_currency['items'], many=True)
            #print("Данные для таблицы обработанные сериалайзером views2: ", serializer)
            result = dict()
            result['data'] = serializer.data
            #print("Данные для таблицы обработанные сериалайзером views3: ", result)
            result['draw'] = prices_currency['draw']
            result['recordsTotal'] = prices_currency['total']
            result['recordsFiltered'] = prices_currency['count']
            print("Данные для таблицы обработанные сериалайзером views4: ", result)

            return Response(result, status=status.HTTP_200_OK, template_name=None, content_type=None)
            # return Response(serializer.data, status=status.HTTP_200_OK, template_name=None, content_type=None)

        except Exception as e:
            return Response(e, status=status.HTTP_404_NOT_FOUND, template_name=None, content_type=None)


#-----------------------------------------------------------------------------------------------------------------------
# Редактирование справочника резерва(остатка) валют с помощью плагина таблицы datatables
def BalanceCurrency(request):
    print("запрос от balance_currency.html")
    user = request.user  # достаем из запроса пользователя для второго уровня проверки(первый в navbar.html)
    reg_gl_menu = 1  # переменная для отрисовки пункта меню "Главная" в blok1/navbarreg.html
    namecurrency = Name_Currency.objects.filter(is_active=True)  # переменная для выбора валюты из таблицы БД Name_Currency для blok2/balance_currency.html
    if user.is_superuser:
        html = TemplateResponse(request, 'balance_currency.html', locals())
        return HttpResponse(html.render())

    else:

        return HttpResponseRedirect('/')

# класс с функцией list для обмена данніми методом ajax с скриптом js/table_balance_currency.js
# обращаемся к классу через роутер в chgskv/urls.py
# queryset атрибут класса для возврата значений объекта табл БД Balance_Currency
# serializer_class атрибут класса для проверки и десериализации ввода, а также для сериализации вывода
class BalanceCurrency_ViewSet(viewsets.ModelViewSet):
    queryset = Balance_Currency.objects.all()
    # сериалайзер из blok2/serializers.py, преобразует записи из табл БД в упорядоченный словарь класса OrderedDict
    serializer_class = Balance_Currency_Serializer

    #print("Данные для таблицы обработанные сериалайзер-класс: ",serializer_class)
    def list(self, request, **kwargs):
        try:
            #print("request.query_params ", request.query_params)
            balance_currency = query_balance_currency_by_args(**request.query_params)  # функция query_balance_currency_by_args из blok2/models.py
            # переменной присваиваем значения из табл БД сформированные функцией query_balance_currency_by_args из blok2/models.py
            # и обработанные сериалайзером Balance_Currency_Serializer в blok2/serializers.py для отображения(рендерим)
            #  в формате json для ajax запроса из скрипта js/table_prices_currency.
            #print("Данные для таблицы обработанные функцией query_balance_currency_by_args в model views1: ", balance_currency)
            serializer = Balance_Currency_Serializer(balance_currency['items'], many=True)
            #print("Данные для таблицы обработанные сериалайзером views2: ", serializer)
            result = dict()
            result['data'] = serializer.data
            #print("Данные для таблицы обработанные сериалайзером views3: ", result)
            result['draw'] = balance_currency['draw']
            result['recordsTotal'] = balance_currency['total']
            result['recordsFiltered'] = balance_currency['count']
            print("Данные для таблицы обработанные сериалайзером views4: ", result)

            return Response(result, status=status.HTTP_200_OK, template_name=None, content_type=None)

        except Exception as e:
            return Response(e, status=status.HTTP_404_NOT_FOUND, template_name=None, content_type=None)


#-----------------------------------------------------------------------------------------------------------------------
# Редактирование справочника новостей с помощью плагина таблицы datatables
def FNews(request):
    print("запрос от news.html")
    user = request.user  # достаем из запроса пользователя для второго уровня проверки(первый в navbar.html)
    reg_gl_menu = 1  # переменная для отрисовки пункта меню "Главная" в blok1/navbarreg.html
    if user.is_superuser:
        html = TemplateResponse(request, 'news.html', locals())
        return HttpResponse(html.render())

    else:

        return HttpResponseRedirect('/')

# класс с функцией list для обмена данніми методом ajax с скриптом js/table_news.js
# обращаемся к классу через роутер в chgskv/urls.py
# queryset атрибут класса для возврата значений объекта табл БД News
# serializer_class атрибут класса для проверки и десериализации ввода, а также для сериализации вывода
class News_ViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    # сериалайзер из blok2/serializers.py, преобразует записи из табл БД в упорядоченный словарь класса OrderedDict
    serializer_class = News_Serializer

    #print("Данные для таблицы обработанные сериалайзер-класс: ",serializer_class)
    def list(self, request, **kwargs):
        try:
            #print("request.query_params ", request.query_params)
            news = query_news_by_args(**request.query_params)  # функция query_news_by_args из blok2/models.py
            # переменной присваиваем значения из табл БД сформированные функцией query_news_by_args из blok2/models.py
            # и обработанные сериалайзером News_Serializer в blok2/serializers.py для отображения(рендерим)
            #  в формате json для ajax запроса из скрипта js/table_news.js
            #print("Данные для таблицы обработанные функцией query_news_by_args в model views1: ", news)
            serializer = News_Serializer(news['items'], many=True)
            #print("Данные для таблицы обработанные сериалайзером views2: ", serializer)
            result = dict()
            result['data'] = serializer.data
            #print("Данные для таблицы обработанные сериалайзером views3: ", result)
            result['draw'] = news['draw']
            result['recordsTotal'] = news['total']
            result['recordsFiltered'] = news['count']
            print("Данные для таблицы обработанные сериалайзером views4: ", result)

            return Response(result, status=status.HTTP_200_OK, template_name=None, content_type=None)

        except Exception as e:
            return Response(e, status=status.HTTP_404_NOT_FOUND, template_name=None, content_type=None)


#-----------------------------------------------------------------------------------------------------------------------
# Редактирование справочника фото(картинок) для новостей с помощью плагина таблицы datatables
def FNewsImage(request):
    print("запрос от newsimage.html")
    user = request.user  # достаем из запроса пользователя для второго уровня проверки(первый в navbar.html)
    reg_gl_menu = 1  # переменная для отрисовки пункта меню "Главная" в blok1/navbarreg.html
    tidings = News.objects.filter(is_active=True)  # переменная для выбора заголовка из таблицы БД News для blok2/newsimage.html
    if user.is_superuser:
        html = TemplateResponse(request, 'newsimage.html', locals())
        return HttpResponse(html.render())

    else:

        return HttpResponseRedirect('/')

# класс с функцией list для обмена данніми методом ajax с скриптом js/table_newsimage.js
# обращаемся к классу через роутер в chgskv/urls.py
# queryset атрибут класса для возврата значений объекта табл БД NewsImage
# serializer_class атрибут класса для проверки и десериализации ввода, а также для сериализации вывода
class NewsImage_ViewSet(viewsets.ModelViewSet):
    queryset = NewsImage.objects.all()
    # сериалайзер из blok2/serializers.py, преобразует записи из табл БД в упорядоченный словарь класса OrderedDict
    serializer_class = NewsImage_Serializer

    print("Данные для таблицы обработанные сериалайзер-класс: ",serializer_class)
    def list(self, request, **kwargs):
        try:
            print("request.query_params ", request.query_params)
            newsimage = query_newsimage_by_args(**request.query_params)  # функция query_newsimage_by_args из blok2/models.py
            # переменной присваиваем значения из табл БД сформированные функцией query_newsimage_by_args из blok2/models.py
            # и обработанные сериалайзером NewsImage_Serializer в blok2/serializers.py для отображения(рендерим)
            #  в формате json для ajax запроса из скрипта js/table_newsimage.js
            print("Данные для таблицы обработанные функцией query_newsimage_by_args в model views1: ", newsimage)
            serializer = NewsImage_Serializer(newsimage['items'], many=True)
            print("Данные для таблицы обработанные сериалайзером views2: ", serializer)
            result = dict()
            result['data'] = serializer.data
            print("Данные для таблицы обработанные сериалайзером views3: ", result)
            result['draw'] = newsimage['draw']
            result['recordsTotal'] = newsimage['total']
            result['recordsFiltered'] = newsimage['count']
            print("Данные для таблицы обработанные сериалайзером views4: ", result)

            return Response(result, status=status.HTTP_200_OK, template_name=None, content_type=None)

        except Exception as e:
            return Response(e, status=status.HTTP_404_NOT_FOUND, template_name=None, content_type=None)


#-----------------------------------------------------------------------------------------------------------------------
# Редактирование справочника списка заявок на обмен с помощью плагина таблицы datatables
def ExchangeList(request):
    print("запрос от exchange_list.html")
    user = request.user  # достаем из запроса пользователя для второго уровня проверки(первый в navbar.html)
    reg_gl_menu = 1  # переменная для отрисовки пункта меню "Главная" в blok1/navbarreg.html
    if user.is_superuser:
        html = TemplateResponse(request, 'exchange_list.html', locals())
        return HttpResponse(html.render())

    else:

        return HttpResponseRedirect('/')
            #reversed("home"))  # Иначе перегружаем домашнюю страницу, если ошибка то HttpResponseRedirect('/')


# класс с функцией list для обмена данніми методом ajax с скриптом js/table_exchange_list.js
# обращаемся к классу через роутер в chgskv/urls.py
# queryset атрибут класса для возврата значений объекта табл БД Exchange_List
# serializer_class атрибут класса для проверки и десериализации ввода, а также для сериализации вывода
class ExchangeList_ViewSet(viewsets.ModelViewSet):
    queryset = Exchange_List.objects.all()
    # сериалайзер из blok2/serializers.py, преобразует записи из табл БД в упорядоченный словарь класса OrderedDict
    serializer_class = Exchange_List_Serializer
    #print("Данные для таблицы обработанные сериалайзер-класс: ",serializer_class)
    def list(self, request, **kwargs):
        try:
            print("request.query_params ", request.query_params)
            exchange_list = query_exchange_list_by_args(**request.query_params)  # функция query_exchange_list_by_args из blok2/models.py
            # переменной присваиваем значения из табл БД сформированные функцией query_exchange_list_by_args из blok2/models.py
            # и обработанные сериалайзером Exchange_List_Serializer в blok2/serializers.py для отображения(рендерим)
            #  в формате json для ajax запроса из скрипта js/table_exchange_list.
            #print("Данные для таблицы обработанные функцией query_exchange_list_by_args в model views1: ", exchange_list)
            serializer = Exchange_List_Serializer(exchange_list['items'], many=True)
            #print("Данные для таблицы обработанные сериалайзером views2: ", serializer)
            result = dict()
            result['data'] = serializer.data
            #print("Данные для таблицы обработанные сериалайзером views3: ", result)
            result['draw'] = exchange_list['draw']
            result['recordsTotal'] = exchange_list['total']
            result['recordsFiltered'] = exchange_list['count']
            print("Данные для таблицы обработанные сериалайзером views4: ", result)

            return Response(result, status=status.HTTP_200_OK, template_name=None, content_type=None)
            # return Response(serializer.data, status=status.HTTP_200_OK, template_name=None, content_type=None)

        except Exception as e:
            return Response(e, status=status.HTTP_404_NOT_FOUND, template_name=None, content_type=None)


#-----------------------------------------------------------------------------------------------------------------------
# Просмотр справочника пользователей
def Users_clients(request):
    print("post запрос в Users_clients от navbar_kaba.html")
    users = User.objects.all().values("id","username","first_name","last_name","email","profile__birth_date","profile__phone","profile__location","profile__active","profile__created","profile__updated")

    return render(request, 'users_clients.html', locals())

# Активация пользователя
def Users_clients_active(request):
    print("post запрос в Users_clients_active от users_clients.js")
    return_izm = dict()  # определяем переменную как словарь
    if request.POST:
        # выводим значение post запроса в терминале питона для проверки
        print(request.POST)
        data = request.POST  # переменной data присваиваем значение post запроса
        item_id = data.get("item_id")
        # находим запись в реестре заявок по id (номер заявки)
        user = Profile.objects.get(user_id=item_id)
        user.active = True  # активируем клиента
        user.save()

        return_izm["user_id"] = item_id  # передаем id заявки

        return JsonResponse(return_izm)

# Деактивация пользователя
def Users_clients_deactivate(request):
    print("post запрос в Users_clients_deactivate от users_clients.js")
    return_izm = dict()  # определяем переменную как словарь
    if request.POST:
        # выводим значение post запроса в терминале питона для проверки
        print(request.POST)
        data = request.POST  # переменной data присваиваем значение post запроса
        item_id = data.get("item_id")
        # находим запись в реестре заявок по id (номер заявки)
        user = Profile.objects.get(user_id=item_id)
        user.active = False  # деактивируем клиента
        user.save()

        return_izm["user_id"] = item_id  # передаем id заявки

        return JsonResponse(return_izm)

#-----------------------------------------------------------------------------------------------------------------------

# Просмотр всех операций обмена администратором
def Exchange_operations(request):
    print("post запрос в Exchange_operations от navbar_kaba.html")
    exchange_requests = Exchange_List.objects.filter(is_active=True)

    return render(request, 'exchange_operations.html', locals())


# Просмотр своих операций обмена клиентом
def Exchange_operations_client(request):
    print("post запрос в Exchange_operations_client от navbar_kab.html")
    print("Текущий клиент: ", request.user)
    # находим пользователя в БД пользователей чтоб получить его id
    user = User.objects.get(username=request.user)
    # находим все заявки пользователя
    exchange_requests = Exchange_List.objects.filter(is_active=True, id_user=user.id)

    return render(request, 'exchange_operations_client.html', locals())



"""
# справочник стал не нужен так как изменилась логика курсов валют, поля 3,4,5 перешли в таблицу курсов валют
# Редактирование справочника связей покупки-продажи валют с помощью плагина таблицы datatables
def NameCurrencyTrading(request):
    print("запрос от name_currency_trading.html")
    user = request.user  # достаем из запроса пользователя для второго уровня проверки(первый в navbar.html)
    reg_gl_menu = 1 # переменная для отрисовки пункта меню "Главная" в blok1/navbarreg.html
    namecurrency = Name_Currency.objects.filter(is_active=True)  # переменная для выбора валюты из таблицы БД Name_Currency для blok2/prices_currency.html
    if user.is_superuser:
        html = TemplateResponse(request, 'name_currency_trading.html', locals())
        return HttpResponse(html.render())

    else:

        return HttpResponseRedirect('/')
            #reversed("home"))  # Иначе перегружаем домашнюю страницу, если ошибка то HttpResponseRedirect('/')

# класс с функцией list для обмена данніми методом ajax с скриптом js/table_name_currency_trading.js
# обращаемся к классу через роутер в chgskv/urls.py
# queryset атрибут класса для возврата значений объекта табл БД Name_Currency_Trading
# serializer_class атрибут класса для проверки и десериализации ввода, а также для сериализации вывода
class NameCurrencyTrading_ViewSet(viewsets.ModelViewSet):
    queryset = Name_Currency_Trading.objects.all()
    # сериалайзер из blok2/serializers.py, преобразует записи из табл БД в упорядоченный словарь класса OrderedDict
    serializer_class = Name_Currency_Trading_Serializer

    def list(self, request, **kwargs):
        try:

            name_currency_trading = query_name_currency_trading_by_args(**request.query_params) # функция query_name_currency_trading_by_args из blok2/models.py
            # переменной присваиваем значения из табл БД сформированные функцией query_name_currency_trading_by_args из blok2/models.py
            # и обработанные сериалайзером Name_Currency_Trading_Serializer в blok2/serializers.py для отображения(рендерим)
            #  в формате json для ajax запроса из скрипта js/table_name_currency_trading.js
            #print("Данные для таблицы обработанные функцией query_prices_currency_trading_by_args в model views1: ",name_currency_trading)
            serializer = Name_Currency_Trading_Serializer(name_currency_trading['items'], many=True)
            #print("Данные для таблицы обработанные сериалайзером views2: ", serializer)
            result = dict()
            result['data'] = serializer.data
            #print("Данные для таблицы обработанные сериалайзером views3: ", result)
            result['draw'] = name_currency_trading['draw']
            result['recordsTotal'] = name_currency_trading['total']
            result['recordsFiltered'] = name_currency_trading['count']
            print("Данные для таблицы обработанные сериалайзером views4: ", result)

            return Response(result, status=status.HTTP_200_OK, template_name=None, content_type=None)
            #return Response(serializer.data, status=status.HTTP_200_OK, template_name=None, content_type=None)

        except Exception as e:
            return Response(e, status=status.HTTP_404_NOT_FOUND, template_name=None, content_type=None)
"""



# Отрисовка страницы печати отчета через плагин https://www.reportbro.com/doc/installation(отключил)
"""
def Print_report(request):
    result_list = list()
    if request.POST:
        result = Name_Currency.objects.all().values('id', 'currency', 'symbol', 'is_active')
        for res in result:
            result_list.append(res)

        print(result_list)


    return render(request, 'report.html', locals())

# Отрисовка страницы печати отчета через jQuery
def Print_pdf(request):
    result_list = list()
    if request.POST:
        result = Name_Currency.objects.all().values('id', 'currency', 'symbol', 'is_active')
        for res in result:
            result_list.append(res)

        print(result_list)

    return render(request, 'report1.html', locals())
"""


