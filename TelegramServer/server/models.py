from django.db import models


class Payment(models.Model):
    total = models.IntegerField(default=7000000, verbose_name='Сумма')
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата платежа')
    monthly_payment = models.IntegerField(default=100000, verbose_name='Перевод')
    leftover = models.IntegerField(default=700000, verbose_name='Остаток')
    total_payment = models.IntegerField(default=7000000, verbose_name='Сумма переводов')
    paid = 'оплачен'
    unpaid = 'ожидает'
    STATUS = [(paid, 'оплачен'), (unpaid, 'ожидает'), ]
    payment_status = models.CharField(max_length=10, choices=STATUS, default='paid', verbose_name='Статус')

    # Поступил перевод
    def transfer(self):
        self.leftover = self.total - 100000
        self.save()


    # добавим абсолютный путь чтобы после создания нас перебрасывало на страницу с постом
    def get_absolute_url(self):
        return

    # Строковое отабражение поста
    def __str__(self):
        return f'Перевод {self.id}'

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'


class Score(models.Model):
    total = models.IntegerField(default=7000000, verbose_name='Сумма')



