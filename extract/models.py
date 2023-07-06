from django.db import models
from user_profile.models import Category, Account
# Create your models here.
class CashFlow(models.Model):
    flow_cash_choices = (
        ('in', 'Entrada'),
        ('out', 'Saída')
    )
    
    value = models.FloatField()
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    description = models.TextField()
    date = models.DateField()
    account = models.ForeignKey(Account, on_delete=models.DO_NOTHING)
    type_cash_flow = models.CharField(max_length=3, choices=flow_cash_choices)

    def __str__(self):
        return self.description