from django.db import models
from user_profile.models import Category

class Bill(models.Model):
    title = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    description = models.TextField()
    value = models.FloatField()
    payment_day = models.IntegerField()
    
    def __str__(self):
        return self.title

class PaidBill(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.DO_NOTHING)
    payment_date = models.DateField()