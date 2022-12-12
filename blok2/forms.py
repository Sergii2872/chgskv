from django import forms


# Задаем поля без значений first_name,last_name,location и birth_date формы и передаем в файл views.py
# (в views.py импортируем from .forms import ContactForm), не использую т.к. использую метод ajax в scripts_izreg.js
class ContactForm(forms.Form):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    #location = forms.CharField(required=True)
    birth_date = forms.DateField(required=True)

class ContactFormPass(forms.Form):
    password = forms.CharField(required=True)
    password1 = forms.CharField(required=True)





