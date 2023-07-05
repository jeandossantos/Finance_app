from django.contrib import admin
from .models import Account, Category
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'essential', 'budget_price')

admin.site.register(Category, CategoryAdmin)


class AccountAdmin(admin.ModelAdmin):
    list_display = ('nickname','bank', 'type_of_person', 'value', 'icon', 'created_at')

admin.site.register(Account, AccountAdmin)
