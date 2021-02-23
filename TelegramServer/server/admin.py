from django.contrib import admin
from .models import Payment, Score, Lender, Borrower


# class PaymentAdmin(admin.ModelAdmin):
#     list_display = ('payment_date', 'payment_status', 'monthly_payment',)


# class ScoreAdmin(admin.ModelAdmin):
#     list_display = ('total', 'total_payment',)


admin.site.register(Payment)
admin.site.register(Score)
admin.site.register(Lender)
admin.site.register(Borrower)


