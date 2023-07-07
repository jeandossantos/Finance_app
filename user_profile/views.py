from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Account, Category
from extract.models import CashFlow
from bill.models import Bill, PaidBill

from . import utils

from datetime import datetime

def home(request):
    CURRENT_MONTH = datetime.now().month
    CURRENT_DAY = datetime.now().day
    
    bills = Bill.objects.all()
    # paid bills of the current month
    paid_bills = PaidBill.objects.filter(payment_date__month=CURRENT_MONTH).values('bill')
    
    # unpaid bills of this month (overdue) (vencidas!)
    unpaid_bills = bills.filter(payment_day__lt=CURRENT_DAY).exclude(id__in=paid_bills)
    
    # approaching bills within 5 days
    approaching_bills = bills.filter(payment_day__gte=CURRENT_DAY).filter(
        payment_day__lte=CURRENT_DAY + 5
    ).exclude(id__in=paid_bills)
    
    accounts = Account.objects.all().order_by('nickname')
    accounts.total = utils.getTotalPrice(accounts, 'value')
    
    cash_flow = CashFlow.objects.filter(date__month=datetime.now().month)
    in_flow = cash_flow.filter(type_cash_flow='in')
    out_flow = cash_flow.filter(type_cash_flow='out')
    total_in_flow = utils.getTotalPrice(in_flow, 'value')    
    total_out_flow = utils.getTotalPrice(out_flow, 'value')
    
    percentual_essential_spent, percentual_not_essential_spent = utils.get_financial_balance()    
    
    for account in accounts: 
        account.value = utils.format_price(account.value)
    
    return render(request, 'home.html', {
            'accounts': accounts,
            'total_in_flow': total_in_flow,
            'total_out_flow': total_out_flow,
            'percentual_essential_spent': percentual_essential_spent,
            'percentual_not_essential_spent': percentual_not_essential_spent,
            'unpaid_bills': len(unpaid_bills),
            'approaching_bills': len(approaching_bills)
    })

def manage(request): 
    categories = Category.objects.all().order_by('name')
    accounts = Account.objects.all().order_by('-created_at')
    
    total = utils.getTotalPrice(accounts, 'value')
    
    for account in accounts:
        account.value = utils.format_price(account.value)
    
    return render(request, 'manage.html', context={
        'accounts': {
            'data': accounts,
            'total': total
        },
        'categories': categories,
    })

def create_account(request):
    nickname = request.POST.get('nickname')
    bank = request.POST.get('bank')
    type_of_person = request.POST.get('type_of_person')
    value = request.POST.get('value')
    icon = request.FILES.get('icon')
    
    if len(nickname.strip()) == 0 or len(value.strip()) == 0:
        messages.error(request, 'Por favor, preencha todos os campos.')
        
        return redirect('/profile/manage/')
    
    account = Account()
    account.nickname = nickname
    account.bank = bank
    account.type_of_person = type_of_person
    account.value = value
    account.icon = icon
    account.save()
    
    messages.success(request, 'Conta criada com sucesso.')
    
    return redirect('/profile/manage/')

def remove_account(request, id):
    account = Account.objects.filter(id=id)
    
    if not account.exists():
        messages.warning(request, 'Conta não encontrada.')
        return redirect('/profile/manage/')
    
    account.delete()

    messages.success(request, 'Conta removida com sucesso.')
    
    return redirect('/profile/manage/')
    
def create_category(request):
    name = request.POST.get('name')
    essential = True if request.POST.get('essential') == 'is_essential' else False

    if len(name.strip()) == 0: 
        messages.error(request, 'Por favor, informe a categoria.')
        
        return redirect('/profile/manage/')
    
    category = Category()
    category.name = name
    category.essential = essential
    category.save()
    
    messages.success(request, 'Categoria criada com sucesso.')
    
    return redirect('/profile/manage/')

def toggle_category_essential(request, id):
    category = Category.objects.filter(id=id)
    
    if not category.exists():
        messages.warning(request, 'Categoria não encontrada.')
        
        return redirect('/profile/manage/')
    
    category = category.first()    
    category.essential = not category.essential

    category.save()
    
    return redirect('/profile/manage/')
        
def dashboard(request):
    data = {}
    
    categories = Category.objects.all()
    
    for category in categories:
        total_spent = CashFlow.objects.filter(category=category)
        data[category.name] = utils.format_price_string_to_float(utils.getTotalPrice(total_spent, 'value'))
    
    return render(request, 'dashboard.html', {
        'labels': list(data.keys()),
        'values': list(data.values())
    })