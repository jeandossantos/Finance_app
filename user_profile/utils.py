
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