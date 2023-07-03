from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def manage(request):
    return render(request, 'manage.html')