
def format_price(price):
    return "{:.2f}".format(price).replace(".", ",")

def getTotalPrice(objs, key):
    total = 0
    
    for obj in objs:
        total += getattr(obj, key)
    
    return format_price(total)