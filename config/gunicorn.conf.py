# Web сервер (крутиться на сервере , обрабатывает локальный адрес на сервере и передает управление внешнему
# серверу http nginx, все запросы которые приходят на nginx он проксирует на внутренний сервер gunicorn)
# пример https://github.com/DJWOMS/oms_project/blob/master/config/gunicorn.conf.py-tpl
bind = '127.0.0.1:8000'
workers = 2
user = "zipper"  # добавленный пользователь на сервере(из под root не рекомендовано запускать)
timeout = 120
