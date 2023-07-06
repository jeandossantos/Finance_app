from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from user_profile import utils

from user_profile.models import Category
from extract.models import CashFlow

from datetime import datetime
import json

def create_planning(request):
    categories = Category.objects.all().order_by('name')
    
    for category in categories:
        category.budget_price = utils.format_price(category.budget_price)
    
    return render(request, 'create_planning.html', {
        'categories': categories,
    })
        
@csrf_exempt        
def update_category_budge_price(request, id):
    try:
        data = json.loads(request.body)
        new_budge_price = data['new_budge_price']
        
        category = Category.objects.get(id=id)
        category.budget_price = utils.format_price_string_to_float(new_budge_price)
        
        category.save()
        
        return HttpResponse(json.dumps({'status': 'success'}))
    except json.JSONDecodeError:
        return HttpResponse(json.dumps({'status': 'failure: invalid JSON'}))
    except Category.DoesNotExist:
        return HttpResponse(json.dumps({'status': 'failure: category not found'}))
    except Exception as e:
        return HttpResponse(json.dumps({'status': 'failure', 'error': str(e)}))

def view_planning(request):
    categories = Category.objects.all().order_by('name')
    
    cashFlow = CashFlow.objects.filter(date__month=datetime.now().month).filter(type_cash_flow='out')
    
    categories.total_cash_flow = utils.getTotalPrice(cashFlow, 'value')
    categories.total_budget = utils.getTotalPrice(categories, 'budget_price')
    categories.total_percentage_spent = int((utils.format_price_string_to_float(categories.total_cash_flow) / utils.format_price_string_to_float(categories.total_budget)) * 100)
    
    for category in categories:        
        category_expenses = cashFlow.filter(category__id=category.id)
                
        category.monthly_expense = utils.getTotalPrice(category_expenses, 'value')
        category.percentage_spent = 0
        
        if category.budget_price != 0:
            category.percentage_spent = int((utils.format_price_string_to_float(category.monthly_expense) / category.budget_price) * 100)
        
        category.budget_price = utils.format_price(category.budget_price)
        
        
    return render(request, 'view_planning.html', {
        'categories': categories
        })