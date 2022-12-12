from django.shortcuts import render
from blok2.models import News, NewsImage # импортируем таблицу БД News, NewsImage из models.py



# Create your views here.

# Новости
def NewsFeed(request):
    news_feeds = News.objects.filter(is_active=True).order_by('-updated')  # фильтр активных новостей и сортировка по убыванию
    news_images = NewsImage.objects.filter(is_active=True).order_by('-is_main','-updated') # фильтр картинок новостей и сортировка по убыванию даты и главной
    return render(request, 'news_feed.html', locals())

# Отображение картинки по клику из новостей из news_feed.html(не использую, заменил на плагин jquery lightbox)
def News_Image_View(request,image_id):
    image = NewsImage.objects.get(id=image_id)

    return render(request, 'news_image_view.html', locals())

# Правила
def Regulations(request):

    return render(request, 'regulations.html', locals())

# Контакты
def Contact(request):

    return render(request, 'contact.html', locals())

# Условия
def Terms(request):

    return render(request, 'terms.html', locals())
