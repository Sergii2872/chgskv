# Generated by Django 3.2.8 on 2022-10-17 09:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blok2', '0008_remove_prices_currency_kurs_buy'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fiat_Wallet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_bank', models.CharField(blank=True, default=None, max_length=30, null=True)),
                ('image_bank', models.ImageField(blank=True, max_length=255, null=True, upload_to='image_bank/')),
                ('wallet_bank', models.CharField(blank=True, default=None, max_length=80, null=True)),
                ('is_active', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name_currency', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='blok2.name_currency')),
            ],
        ),
    ]
