# для progress bar celery
# по примеру https://www.youtube.com/watch?v=BbPswIqn2VI
# https://github.com/PrettyPrinted/youtube_video_code/blob/master/2020/06/24/How%20to%20Create%20a%20Celery%20Task%20Progress%20Bar%20in%20Django/djangoprogressbar/progress/progress/celery.py

# другие настройки
# https://hashsum.ru/celery-django-redis/

# Запуск терминала-сервера redis https://webdevblog.ru/asinhronnye-zadachi-v-django-s-redis-i-celery/
# для windows чтоб не вылетала в celery ошибка делаем pip install gevent
# и запускаем celery командой celery -A chgskv worker -l info -P gevent

from __future__ import absolute_import, unicode_literals

import os

# Из только что установленной библиотеки celery импортируем класс Celery
from celery import Celery

# set the default Django settings module for the 'celery' program.
# Указываем где находится модуль django и файл с настройками django (имя_вашего_проекта.settings)
# в свою очередь в файле settings будут лежать все настройки celery.
# Соответственно при указании данной директивы нам не нужно будет при вызове каждого task(функции) прописывать
# эти настройки.
# chgskv - здесь имя_вашего_проекта
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chgskv.settings')

# Создаем объект(экземпляр класса) celery и даем ему имя
app = Celery('chgskv')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
# Загружаем config с настройками для объекта celery.
# т.е. импортируем настройки из django файла settings
# namespace='CELERY' - в данном случае говорит о том, что применятся будут только
# те настройки из файла settings.py которые начинаются с ключевого слова CELERY
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
# В нашем приложении мы будем создавать файлы tasks.py в которых будут находится
# task-и т.е. какие-либо задания. При указании этой настройки
# celery будет автоматом искать такие файлы и подцеплять к себе.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))