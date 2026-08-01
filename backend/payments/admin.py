from django.contrib import admin

from .models import Payment, PendingPayment

# Register your models here.
admin.site.register(Payment)
admin.site.register(PendingPayment)