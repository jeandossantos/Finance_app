from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50)
    essential = models.BooleanField(default=False)
    budget_price = models.FloatField(default=0)
    
    def __str__ (self): 
        return self.name
    

class Account(models.Model):
    bank_list = (
        ('NU', 'Nubank'),
        ('CE', 'Caixa Econômica'),
        ('BR', 'Banco do Brasil'),
        ('IT', 'Itaú'),
        ('SF', 'Banco Safra'),
        ('SG', 'Santander Group')        
    )
    
    types_of_person = (
        ('PF', 'Pessoa Física'),
        ('PJ', 'Pessoa Jurídica')
    )
    
    nickname = models.CharField(max_length=50)
    bank = models.CharField(max_length=2, choices=bank_list)
    type_of_person = models.CharField(max_length=2, choices=types_of_person)
    value = models.FloatField()
    icon = models.ImageField(upload_to='icons')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__ (self): 
        return self.nickname
