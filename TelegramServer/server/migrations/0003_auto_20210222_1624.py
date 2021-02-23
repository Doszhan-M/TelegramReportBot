# Generated by Django 3.1.7 on 2021-02-22 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0002_auto_20210222_1144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='score',
            name='payment_status',
            field=models.CharField(choices=[('оплачен', 'подтвержден'), ('ожидает', 'ожидает подтверждния')], default='ожидает подтверждния', max_length=30, verbose_name='Статус'),
        ),
    ]