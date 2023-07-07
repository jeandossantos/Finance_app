from datetime import datetime
from extract.models import CashFlow

def format_price(price):
    return "{:.2f}".format(price).replace(".", ",")

def format_price_string_to_float(price_string):
    price_string = price_string.replace(",", ".")
    return float(price_string)

def getTotalPrice(objs, key):
    total = 0
    
    for obj in objs:
        total += getattr(obj, key)
    
    return format_price(total)

def get_financial_balance():
    essential_spent = CashFlow.objects.filter(date__month=datetime.now().month).filter(
        category__essential=True
    ).filter(type_cash_flow='out')
    
    not_essential_spent =CashFlow.objects.filter(date__month=datetime.now().month).filter(
        category__essential=False
    ).filter(type_cash_flow='out')
        
    total_essential_spent = format_price_string_to_float(getTotalPrice(essential_spent, 'value'))
    total_not_essential_spent = format_price_string_to_float(getTotalPrice(not_essential_spent, 'value'))
    total_spent = total_essential_spent + total_not_essential_spent

    try:    
        percentual_essential_spent = int(total_essential_spent  * 100 / total_spent)
        percentual_not_essential_spent = int(total_not_essential_spent  * 100 / total_spent)

        return percentual_essential_spent, percentual_not_essential_spent
    except:
        return 0, 0