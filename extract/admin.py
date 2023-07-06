from django.contrib import admin
from .models import CashFlow
    
class CashFlowAdmin(admin.ModelAdmin):
        list_display = ("value",
        "category",
        "description",
        "date",
        "account",
        "type_cash_flow"
        )

admin.site.register(CashFlow, CashFlowAdmin)