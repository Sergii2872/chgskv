from django import forms
from .models import *


# Вывод полей на основе моделей в файле models.py (класс сам определяет сколько полей в наших БД User и Profile)

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = [""]

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = [""]



