from django.contrib import admin
from .models import Payment, Score


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_date', 'payment_status', 'monthly_payment',)


# class ScoreAdmin(admin.ModelAdmin):
#     list_display = ('total', 'total_payment',)


admin.site.register(Payment, PaymentAdmin)
admin.site.register(Score)


