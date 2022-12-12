from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from django.db.models import signals
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.core.exceptions import ValidationError


# Create your models here.

# Наша модель(БД) именем Profile встроенной базы пользователей django с дополнительными полями, метод OneToOneField
# Доп поля по ключу user_id встроенной БД(из админки) пользователей user
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Список дополнительных полей
    session_key = models.CharField(max_length=128, blank=True, null=True, default=None)  # ключ сессии, для контроля сторонних(хакерских) запросов, присваивается пользователю при посещении сайта, если заходит с другого броузера или компьютера то ключ изменится
    birth_date = models.DateField(null=True, blank=True) # день рождения
    location = models.CharField(max_length=30, blank=True) # Последний ip пользователя
    phone = models.CharField(max_length=30, blank=True) # Телефон пользователя
    active = models.BooleanField(default=False) # Поле для активации пользователя по email
    verification_uuid = models.UUIDField('Unique Verification UUID', default=uuid.uuid4) # Поле для проверки уникальности верификации по email
    created = models.DateTimeField(auto_now_add=True, auto_now=False)  # Поле дата когда пользователь зарегистрировался
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)  # Поле дата когда пользователь заходил последний раз

# Применяем функцию create_or_update_user_profile  к нашей БД Profile(по сигналу post_save
# при изменении в таблице БД User из django.contrib.auth.models делаются изменения в таблице БД Profile, т.е. так
# получается связка основной таблицы пользователей User и расширенной Profile  с дополнительными полями)
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        if not instance.profile.active:
            try:
                subject = 'Активация учетной записи Chgskv.com'
                msg = 'Добрый день! Для активации регистрации перейдите по этой ссылке: http://127.0.0.1:8000%s' % reverse('Verify', kwargs={'uuid': str(instance.profile.verification_uuid)})
                send_mail(
                    subject,
                    msg,
                    settings.EMAIL_HOST_USER, # EMAIL_HOST_USER задан в settings.py
                    [instance.email],
                    fail_silently=False,
                )
            except Exception as e:
                print("Ошибка отправки email: ", e)

    instance.profile.save()

# перенес в функцию create_user_profile чтобы не делать вторую функцию по сигналу post_save(упростил)
#@receiver(post_save, sender=User)
#def save_user_profile(sender, instance, **kwargs):
#    instance.profile.save()

 # Отправка ссылки подтверждения по email для активации пользователя(перенес в функцию create_user_profile, т.к.
 # дублировалась отправка сообщения )
#def user_post_save(sender, instance, signal, *args, **kwargs):
    # post_url = request.build_absolute_uri()
    # если поле active = False в таблице БД Profile то отправляем ссылку на email
#    if not instance.profile.active:
#        subject = 'Активация учетной записи Chgskv.com'
#        msg = 'Добрый день! Для активации регистрации перейдите по этой ссылке: http://127.0.0.1:8000%s' % reverse('Verify', kwargs={'uuid': str(instance.profile.verification_uuid)})
#        send_mail(
#            subject,
#            msg,
#            settings.EMAIL_HOST_USER,
#            [instance.email],
#            fail_silently=False,
#        )
#signals.post_save.connect(user_post_save, sender=User)


class Site_maintenance(models.Model):
    maintenance = models.BooleanField(default=False) # Поле для активации перехода сайта в техобслуживание
    created = models.DateTimeField(auto_now_add=True, auto_now=False)  # Поле дата создания записи
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)  # Поле дата изменения записи

    # _str_(self) - метод, вызываемый функциями str, print и format. Возвращает строковое представление объекта
    # Используем этот метод для удобного отображения информации полей в django админке
    # для отображения в админке, регистрируем в admin.py
    #def __str__(self):
    #    return "Техобслуживание {}".format(self.maintenance)

    # Для отображения наименований в django админке
    class Meta:
        verbose_name = 'БД Техобслуживание сайта'
        verbose_name_plural = 'Записи в БД Site_maintenance'