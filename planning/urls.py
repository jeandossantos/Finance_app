from django.urls import path
from . import views

urlpatterns = [
    path('create_planning/', views.create_planning, name='create_planning'),
    path('view_planning/', views.view_planning, name='view_planning'),
    path('update_category_budge_price/<int:id>',
         views.update_category_budge_price, 
         name='update_category_budge_price'),
]