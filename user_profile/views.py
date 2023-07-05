from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Account, Category

from . import utils

def home(request):
    accounts = Account.objects.all().order_by('nickname')
    
    total = utils.getTotalPrice(accounts, 'value')
    
    for account in accounts: 
        account.value = utils.format_price(account.value)
    
    return render(request, 'home.html', {
        'accounts': {
            'data': accounts,
            'total': total            
        }
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
        
    