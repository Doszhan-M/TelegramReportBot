from django.db import models


class Score(models.Model):
    total = models.IntegerField(default=7000000, verbose_name='Сумма')
    leftover = models.IntegerField(default=700000, verbose_name='Остаток')
    monthly_payment = models.IntegerField(default=100000, verbose_name='Перевод')
    total_payment = models.IntegerField(default=0, verbose_name='Сумма переводов')
    date_score = models.DateTimeField(auto_now_add=True, verbose_name='Дата платежа')
    paid = 'оплачен'
    unpaid = 'ожидает'
    STATUS = [(paid, 'подтвержден'), (unpaid, 'ожидает подтверждния'), ]
    payment_status = models.CharField(max_length=30, choices=STATUS, default='ожидает подтверждния', verbose_name='Статус')

    # добавим абсолютный путь чтобы после создания нас перебрасывало на страницу с постом
    def get_absolute_url(self):
        return f'http://127.0.0.1:8000/'

    # Строковое отабражение поста
    def __str__(self):
        return f'Счет {self.id}'

    class Meta:
        verbose_name = 'Счет'
        verbose_name_plural = 'Счета'


class Payment(models.Model):
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата платежа')
    monthly_payment = models.IntegerField(default=100000, verbose_name='Перевод')

    # добавим абсолютный путь чтобы после создания нас перебрасывало на страницу с постом
    def get_absolute_url(self):
        return f'http://127.0.0.1:8000/'

    # Строковое отабражение поста
    def __str__(self):
        return f'Перевод {self.id}'

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'



class Lender(models.Model):
    lender_id = models.IntegerField(default=0, verbose_name='ID займодателя')

    # Строковое отабражение поста
    def __str__(self):
        return f'Займодатель {self.id}'

    class Meta:
        verbose_name = 'Займодатель'
        verbose_name_plural = 'Займодатели'


class Borrower(models.Model):
    borrower_id = models.IntegerField(default=0, verbose_name='ID заемщика')

    # Строковое отабражение поста
    def __str__(self):
        return f'Заемщик {self.id}'

    class Meta:
        verbose_name = 'Заемщик'
        verbose_name_plural = 'Заемщики'