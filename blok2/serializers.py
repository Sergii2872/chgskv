# сериалайзер для функции list класса NameCurrency_ViewSet,PricesCurrency_ViewSet, ... в blok2/views.py
from django.conf import settings
from rest_framework import serializers
# пакет для полей файлов, картинок https://pypi.org/project/django-extra-fields/
from drf_extra_fields.fields import Base64ImageField

from .models import Market_Exchange, Name_Currency, Fiat_Wallet, Prices_Currency, Balance_Currency, News, NewsImage, Exchange_List #Name_Currency_Trading


#-----------------------------------------------------------------------------------------------------------------------
# сериалайзер формирующий записи таблицы БД Market_Exchange в упорядоченный словарь класса OrderedDict
# fields перечисляем какие поля и их значения формируем для передачи в функцию list класса MarketExchange_ViewSet в blok2/views.py
# преобразуем формат значений полей updated, created в формат заданный в settings.py(дата время или дата)
class Market_Exchange_Serializer(serializers.ModelSerializer):
    # If your <field_name> is declared on your serializer with the parameter required=False
    # then this validation step will not take place if the field is not included.
    # DATETIME_FORMAT и DATE_FORMAT форматы отображения значений полей дат, описаны в settings.py

    updated = serializers.DateTimeField(format=settings.DATETIME_FORMAT, required=False)
    created = serializers.DateTimeField(format=settings.DATE_FORMAT, required=False)

    class Meta:
        model = Market_Exchange
        fields = '__all__'

#-----------------------------------------------------------------------------------------------------------------------
# сериалайзер формирующий записи таблицы БД Name_Currency в упорядоченный словарь класса OrderedDict
# fields перечисляем какие поля и их значения формируем для передачи в функцию list класса NameCurrency_ViewSet в blok2/views.py
# преобразуем формат значений полей updated, created в формат заданный в settings.py(дата время или дата)
class Name_Currency_Serializer(serializers.ModelSerializer):
    # If your <field_name> is declared on your serializer with the parameter required=False
    # then this validation step will not take place if the field is not included.
    # DATETIME_FORMAT и DATE_FORMAT форматы отображения значений полей дат, описаны в settings.py

    updated = serializers.DateTimeField(format=settings.DATETIME_FORMAT, required=False)
    created = serializers.DateTimeField(format=settings.DATE_FORMAT, required=False)

    image_currency = Base64ImageField(required=False)  # поле из доп.пакета https://pypi.org/project/django-extra-fields/

    market_exchange = Market_Exchange_Serializer(many=False, read_only=True)  # подключаем сериализированные поля БД Market_Exchange
    market_exchange_id = serializers.IntegerField(write_only=True)  # подключаем связанное поле id(foreign key) БД Market_Exchange

    class Meta:
        model = Name_Currency
        fields = '__all__'
        #fields = ('id', 'currency', 'symbol', 'is_active', 'created', 'updated')


#-----------------------------------------------------------------------------------------------------------------------
# сериалайзер формирующий записи таблицы БД Fiat_Wallet в упорядоченный словарь класса OrderedDict
# fields перечисляем какие поля и их значения формируем для передачи в функцию list класса FiatWallet_ViewSet в blok2/views.py
# преобразуем формат значений полей updated, created в формат заданный в settings.py(дата время или дата)
class Fiat_Wallet_Serializer(serializers.ModelSerializer):
    # If your <field_name> is declared on your serializer with the parameter required=False
    # then this validation step will not take place if the field is not included.
    # DATETIME_FORMAT и DATE_FORMAT форматы отображения значений полей дат, описаны в settings.py

    updated = serializers.DateTimeField(format=settings.DATETIME_FORMAT, required=False)
    created = serializers.DateTimeField(format=settings.DATE_FORMAT, required=False)
    #kurs_date = serializers.DateField(format=settings.DATE_FORMAT, required=False)

    # https://ilyachch.gitbook.io/django-rest-framework-russian-documentation/overview/navigaciya-po-api/relations
    # https://progi.pro/djangorestframework-kak-serializovat-opredelennoe-pole-foriegnkey-a-ne-znachenie-pk-9235001
    # https://www.vhinandrich.com/blog/saving-foreign-key-id-django-rest-framework-serializer#comment-45

    image_bank = Base64ImageField(required=False)  # поле из доп.пакета https://pypi.org/project/django-extra-fields/

    name_currency = Name_Currency_Serializer(many=False, read_only=True) # подключаем сериализированные поля БД Name_Currency
    name_currency_id = serializers.IntegerField(write_only=True) # подключаем связанное поле id(foreign key) БД Name_Currency



    class Meta:
        model = Fiat_Wallet
        fields = '__all__'


#-----------------------------------------------------------------------------------------------------------------------
# сериалайзер формирующий записи таблицы БД Prices_Currency в упорядоченный словарь класса OrderedDict
# fields перечисляем какие поля и их значения формируем для передачи в функцию list класса PricesCurrency_ViewSet в blok2/views.py
# преобразуем формат значений полей updated, created в формат заданный в settings.py(дата время или дата)
class Prices_Currency_Serializer(serializers.ModelSerializer):
    # If your <field_name> is declared on your serializer with the parameter required=False
    # then this validation step will not take place if the field is not included.
    # DATETIME_FORMAT и DATE_FORMAT форматы отображения значений полей дат, описаны в settings.py

    updated = serializers.DateTimeField(format=settings.DATETIME_FORMAT, required=False)
    created = serializers.DateTimeField(format=settings.DATE_FORMAT, required=False)
    #kurs_date = serializers.DateField(format=settings.DATE_FORMAT, required=False)

    # https://ilyachch.gitbook.io/django-rest-framework-russian-documentation/overview/navigaciya-po-api/relations
    # https://progi.pro/djangorestframework-kak-serializovat-opredelennoe-pole-foriegnkey-a-ne-znachenie-pk-9235001
    # https://www.vhinandrich.com/blog/saving-foreign-key-id-django-rest-framework-serializer#comment-45

    #name_currency_symbol = serializers.CharField(read_only=True) # serializers.CharField(source="name_currency.symbol")
    #name_currency_id = serializers.CharField(source='name_currency.id')    #PrimaryKeyRelatedField(source="name_currency.id", queryset=Name_Currency.objects.all()) #SlugRelatedField(source="name_currency.id", many=True, read_only=True, slug_field='name_currency.id')
    name_currency = Name_Currency_Serializer(many=False, read_only=True) # подключаем сериализированные поля БД Name_Currency
    name_currency_id = serializers.IntegerField(write_only=True) # подключаем связанное поле id(foreign key) БД Name_Currency

    market_exchange = Market_Exchange_Serializer(many=False, read_only=True)  # подключаем сериализированные поля БД Market_Exchange
    market_exchange_id = serializers.IntegerField(write_only=True)  # подключаем связанное поле id(foreign key) БД Market_Exchange

    class Meta:
        model = Prices_Currency
        fields = '__all__'
        #fields = ('id', 'name_currency_symbol', 'name_currency_id', 'kurs_by', 'kurs_sell', 'kurs_date', 'is_active', 'created', 'updated')

    #def create(self, validated_data):
    #    print("Данные для валидации в сериалайзере от ajax:", validated_data)
        #tracks_data = validated_data.pop('name_currency')
        #print(tracks_data)
    #    prices_currency = Prices_Currency.objects.create(**validated_data)
        #for track_data in tracks_data:
            #Name_Currency.objects.create(prices_currency=prices_currency, **track_data)
    #    return prices_currency


#-----------------------------------------------------------------------------------------------------------------------
# сериалайзер формирующий записи таблицы БД Balance_Currency в упорядоченный словарь класса OrderedDict
# fields перечисляем какие поля и их значения формируем для передачи в функцию list класса BalanceCurrency_ViewSet в blok2/views.py
# преобразуем формат значений полей updated, created в формат заданный в settings.py(дата время или дата)
class Balance_Currency_Serializer(serializers.ModelSerializer):
    # If your <field_name> is declared on your serializer with the parameter required=False
    # then this validation step will not take place if the field is not included.
    # DATETIME_FORMAT и DATE_FORMAT форматы отображения значений полей дат, описаны в settings.py

    updated = serializers.DateTimeField(format=settings.DATETIME_FORMAT, required=False)
    created = serializers.DateTimeField(format=settings.DATE_FORMAT, required=False)

    # https://ilyachch.gitbook.io/django-rest-framework-russian-documentation/overview/navigaciya-po-api/relations
    # https://progi.pro/djangorestframework-kak-serializovat-opredelennoe-pole-foriegnkey-a-ne-znachenie-pk-9235001
    # https://www.vhinandrich.com/blog/saving-foreign-key-id-django-rest-framework-serializer#comment-45

    name_currency = Name_Currency_Serializer(many=False, read_only=True) # подключаем сериализированные поля БД Name_Currency
    name_currency_id = serializers.IntegerField(write_only=True) # подключаем связанное поле id(foreign key) БД Name_Currency

    class Meta:
        model = Balance_Currency
        fields = '__all__'


#-----------------------------------------------------------------------------------------------------------------------
# сериалайзер формирующий записи таблицы БД News в упорядоченный словарь класса OrderedDict
# fields перечисляем какие поля и их значения формируем для передачи в функцию list класса News_ViewSet в blok2/views.py
# преобразуем формат значений полей updated, created в формат заданный в settings.py(дата время или дата)
class News_Serializer(serializers.ModelSerializer):
    # If your <field_name> is declared on your serializer with the parameter required=False
    # then this validation step will not take place if the field is not included.
    # DATETIME_FORMAT и DATE_FORMAT форматы отображения значений полей дат, описаны в settings.py

    updated = serializers.DateTimeField(format=settings.DATETIME_FORMAT, required=False)
    created = serializers.DateTimeField(format=settings.DATE_FORMAT, required=False)


    class Meta:
        model = News
        fields = '__all__'


#-----------------------------------------------------------------------------------------------------------------------
# сериалайзер формирующий записи таблицы БД NewsImage в упорядоченный словарь класса OrderedDict
# fields перечисляем какие поля и их значения формируем для передачи в функцию list класса NewsImage_ViewSet в blok2/views.py
# преобразуем формат значений полей updated, created в формат заданный в settings.py(дата время или дата)
class NewsImage_Serializer(serializers.ModelSerializer):
    # If your <field_name> is declared on your serializer with the parameter required=False
    # then this validation step will not take place if the field is not included.
    # DATETIME_FORMAT и DATE_FORMAT форматы отображения значений полей дат, описаны в settings.py

    updated = serializers.DateTimeField(format=settings.DATETIME_FORMAT, required=False)
    created = serializers.DateTimeField(format=settings.DATE_FORMAT, required=False)
    #image = serializers.ImageField(allow_empty_file=True, required=False) # max_length=None, allow_empty_file=False, use_url=False
    image = Base64ImageField(required=False) # поле из доп.пакета https://pypi.org/project/django-extra-fields/

    # https://ilyachch.gitbook.io/django-rest-framework-russian-documentation/overview/navigaciya-po-api/relations
    # https://progi.pro/djangorestframework-kak-serializovat-opredelennoe-pole-foriegnkey-a-ne-znachenie-pk-9235001
    # https://www.vhinandrich.com/blog/saving-foreign-key-id-django-rest-framework-serializer#comment-45

    to_news = News_Serializer(many=False, read_only=True) # подключаем сериализированные поля БД News
    to_news_id = serializers.IntegerField(write_only=True) # подключаем связанное поле id(foreign key) БД News


    class Meta:
        model = NewsImage
        fields = '__all__'

#-----------------------------------------------------------------------------------------------------------------------
# сериалайзер формирующий записи таблицы БД Exchange_List в упорядоченный словарь класса OrderedDict
# fields перечисляем какие поля и их значения формируем для передачи в функцию list класса ExchangeList_ViewSet в blok2/views.py
# преобразуем формат значений полей updated, created в формат заданный в settings.py(дата время или дата)
class Exchange_List_Serializer(serializers.ModelSerializer):
    # If your <field_name> is declared on your serializer with the parameter required=False
    # then this validation step will not take place if the field is not included.
    # DATETIME_FORMAT и DATE_FORMAT форматы отображения значений полей дат, описаны в settings.py

    updated = serializers.DateTimeField(format=settings.DATETIME_FORMAT, required=False)
    created = serializers.DateTimeField(format=settings.DATE_FORMAT, required=False)

    # https://ilyachch.gitbook.io/django-rest-framework-russian-documentation/overview/navigaciya-po-api/relations
    # https://progi.pro/djangorestframework-kak-serializovat-opredelennoe-pole-foriegnkey-a-ne-znachenie-pk-9235001
    # https://www.vhinandrich.com/blog/saving-foreign-key-id-django-rest-framework-serializer#comment-45

    class Meta:
        model = Exchange_List
        fields = '__all__'

