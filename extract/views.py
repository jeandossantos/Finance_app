from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.contrib import messages
from django.http import HttpResponse, FileResponse
from django.conf import settings

from user_profile.models import Account, Category
from user_profile import utils
from .models import CashFlow

from datetime import datetime, timedelta
import os
from io import BytesIO

from weasyprint import HTML

def add_new_value(request):
    if request.method == 'GET':
        accounts = Account.objects.all().order_by('nickname')
        categories = Category.objects.all().order_by('name')
        
        return render(request, 'add_new_value.html', {
            'categories': categories,
            'accounts': accounts
        })
    
    value = request.POST.get('value')
    category_id = request.POST.get('category')
    description = request.POST.get('description')
    date = request.POST.get('date')
    account_id = request.POST.get('account')
    type_cash_flow = request.POST.get('cash_flow')

    cash_flow = CashFlow()
    cash_flow.value = value
    cash_flow.category_id = category_id
    cash_flow.description = description
    cash_flow.date = date
    cash_flow.account_id = account_id
    cash_flow.type_cash_flow = type_cash_flow
    
    account = Account.objects.get(id=account_id)
    
    if type_cash_flow == 'in':
        account.value += int(value)
    else:
        account.value -= int(value)
    
    cash_flow.save()
    account.save()
    
    messages.success(
        request,
        'Movimento de {0} registrado com sucesso.'.format('entrada' if type_cash_flow == 'in' else 'saída')
    )

    return redirect('/extract/add_new_value')

def view_extract(request):
    if request.method == 'GET':
        accounts = Account.objects.all().order_by('nickname')
        categories = Category.objects.all().order_by('name')
        
        account_id = request.GET.get('account')
        categories_id = request.GET.get('category')
        period = request.GET.get('period')
        
        cash_flow = CashFlow.objects.filter(date__month=datetime.now().month)
        
        if account_id:
            cash_flow = cash_flow.filter(account__id=account_id)
            
        if categories_id:
            cash_flow = cash_flow.filter(category__id=categories_id)
            
        if period:
            end_date = datetime.now().date()
            start_date = end_date - timedelta(days=int(period))
            cash_flow = cash_flow.filter(date__range=[start_date ,end_date])
        
        for flow in cash_flow:
            flow.value = utils.format_price(flow.value)            
            
        return render(request, 'view_extract.html', {
            'cash_flow': cash_flow,
            'accounts': accounts,
            'categories': categories
        })
        
def export_pdf(request):
    cash_flow = CashFlow.objects.filter(date__month=datetime.now().month)
    
    for flow in cash_flow:
            flow.value = utils.format_price(flow.value) 
    
    template_path = os.path.join(settings.BASE_DIR, 'templates', 'extract.html')
    
    template = render_to_string(template_path, {
        'cash_flow': cash_flow
    })
    
    path_output = BytesIO()
    
    HTML(string=template).write_pdf(path_output)
    
    path_output.seek(0)
    
    return FileResponse(path_output, filename='extrato.pdf')
    
