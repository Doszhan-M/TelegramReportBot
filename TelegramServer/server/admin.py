from django.contrib import admin
from .models import Payment, Score, Lender, Borrower


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_date', 'monthly_payment',)


class ScoreAdmin(admin.ModelAdmin):
    list_display = ('date_score', 'payment_status', 'monthly_payment',  'total_payment', 'leftover',  'total',)


admin.site.register(Payment, PaymentAdmin)
admin.site.register(Score, ScoreAdmin)
admin.site.register(Lender)
admin.site.register(Borrower)


