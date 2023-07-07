from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('manage/', views.manage, name='manage'),    
    path('create_account', views.create_account, name='create_account'),    
    path('remove_account/<int:id>', views.remove_account, name='remove_account'),    
    path('create_category', views.create_category, name='create_category'),    
    path('toggle_category_essential/<int:id>', views.toggle_category_essential, name='toggle_category_essential'),
    path('dashboard/', views.dashboard, name="dashboard"),
]