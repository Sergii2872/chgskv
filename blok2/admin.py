# для отражения в админке
from django.contrib import admin
from .models import *

# Register your models here.

class NewsImageAdmin (admin.ModelAdmin):
    list_display = [field.name for field in NewsImage._meta.fields]


    class Meta:
        model = NewsImage

admin.site.register(NewsImage, NewsImageAdmin)