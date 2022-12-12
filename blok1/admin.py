from django.contrib import admin
from .models import * # Из файла models в текущей папке импортируем все(структуру таблицы БД)

# Register your models here.

# выполняем команду python manage.py createsuperuser - создаем админа в Django админке boss  bs28011972

# Заполняем форму для вывода на экран в нашем navbarreg.html файле (fields - включить поля, exclude - исключить поля)
# Ниже закоментированный код для промежуточного просмотра
class UserProfile (admin.ModelAdmin):
    # list_display = ["name", "email"] # Выводим поля имя и имейл в админке
    list_display = [field.name for field in Profile._meta.fields] # Выводим все поля которые есть в нашей БД
    #list_filter = ['name',] # Выводим колонку фильтр в админке для фильтрования наших записей
    #search_fields = ['name', 'email'] # Выводим поле в админке для ввода поиска записей по имени или емэйл

    #fields = ["email"]

    # exclude = ["email"]  Пример исключения поля email( не будет отображаться в админке)
	# inlines = [FieldMappingInline]
	# fields = []

    class Meta:
        model = Profile

admin.site.register(Profile, UserProfile)
# SubscriberAdmin класс для отображения полей в админке, меняет стандартные настройки нашей БД Subscriber

# регистрируем в админке БД Site_maintenance
class Site_maintenanceAdmin (admin.ModelAdmin):
    list_display = [field.name for field in Site_maintenance._meta.fields]


    class Meta:
        model = Site_maintenance

admin.site.register(Site_maintenance, Site_maintenanceAdmin)