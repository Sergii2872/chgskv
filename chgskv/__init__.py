# для progress bar celery
# по примеру https://www.youtube.com/watch?v=BbPswIqn2VI
# https://github.com/PrettyPrinted/youtube_video_code/blob/master/2020/06/24/How%20to%20Create%20a%20Celery%20Task%20Progress%20Bar%20in%20Django/djangoprogressbar/progress/progress/__init__.py

from __future__ import absolute_import, unicode_literals

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
# импортируем из созданного нами ранее файла celery.py наш объект(экземпляр класса) celery (app)
from .celery import app as celery_app

# Подключаем объект
__all__ = ('celery_app',)