from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse

from .models import Bill, PaidBill
from user_profile.models import Category
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import json

def add_bill(request):
    if request.method == 'GET':
        categories = Category.objects.all().order_by('name')
        
        return render(request, 'add_bill.html', {
            'categories': categories
        })
    else:
        title = request.POST.get('title')
        category_id = request.POST.get('category')
        description = request.POST.get('description')
        value = request.POST.get('value')
        payment_day = request.POST.get('payment_day')
        
        bill = Bill()
        bill.title = title
        bill.category_id = category_id
        bill.description = description
        bill.value = value
        bill.payment_day = payment_day        
        
        bill.save()
        messages.success(request, 'Conta adicionada com sucesso.')
        return redirect('/bill/add_bill')
    

def view_bills(request):
    CURRENT_MONTH = datetime.now().month
    CURRENT_DAY = datetime.now().day
    
    bills = Bill.objects.all().order_by('title')    
    # paid bills of the current month
    paid_bills = PaidBill.objects.filter(payment_date__month=CURRENT_MONTH).values('bill') 
    
    # unpaid bills of this month (overdue) (vencidas!)
    unpaid_bills = bills.filter(payment_day__lt=CURRENT_DAY).exclude(id__in=paid_bills)
    
    # approaching bills within 5 days
    approaching_bills = bills.filter(payment_day__gte=CURRENT_DAY).filter(
        payment_day__lte=CURRENT_DAY + 5
    ).exclude(id__in=paid_bills)
    
    upcoming_bills = bills.exclude(id__in=paid_bills).exclude(id__in=approaching_bills).exclude(id__in=unpaid_bills)

    return render(request, 'view_bills.html', {
        'unpaid_bills': unpaid_bills,
        'approaching_bills': approaching_bills,
        'upcoming_bills': upcoming_bills,        
        'total_unpaid_bills': len(unpaid_bills),
        'total_approaching_bills': len(approaching_bills),
        'total_upcoming_bills': len(upcoming_bills),
        'total_paid_bills': len(paid_bills)
    })
    
@csrf_exempt
def paid_bill(request, bill_id):
    print('PAID BVIx')

    paid_bill = PaidBill()
    paid_bill.bill_id = bill_id
    paid_bill.payment_date = datetime.now().date()
    
    paid_bill.save()
    
    return JsonResponse({ "result": "ok"})