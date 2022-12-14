# Generated by Django 2.0 on 2018-06-28 11:51

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('blok1', '0004_profile_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='verification_uuid',
            field=models.UUIDField(default=uuid.uuid4, verbose_name='Unique Verification UUID'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]
