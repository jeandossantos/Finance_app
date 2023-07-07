from django.contrib import admin
from .models import Bill, PaidBill
# Register your models here.

class BillAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'description', 'value', 'payment_day']

class PaidBillAdmin(admin.ModelAdmin):
    list_display = ['bill', 'payment_date']


admin.site.register(Bill, BillAdmin)
admin.site.register(PaidBill, PaidBillAdmin)