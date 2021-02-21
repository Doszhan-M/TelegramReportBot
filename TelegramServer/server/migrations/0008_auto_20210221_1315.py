# Generated by Django 3.1.7 on 2021-02-21 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0007_auto_20210221_1254'),
    ]

    operations = [
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.IntegerField(default=7000000, verbose_name='Остаток')),
                ('total_payment', models.IntegerField(default=7000000, verbose_name='Сумма переводов')),
            ],
        ),
        migrations.RemoveField(
            model_name='payment',
            name='total',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='total_payment',
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_status',
            field=models.CharField(choices=[('оплачен', 'оплачен'), ('ожидает', 'ожидает')], default='paid', max_length=10, verbose_name='Статус'),
        ),
    ]
