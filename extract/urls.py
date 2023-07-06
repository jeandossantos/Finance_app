from django.urls import path
from . import views

urlpatterns = [
    path('add_new_value', views.add_new_value, name='add_new_value'),
    path('view_extract', views.view_extract, name='view_extract'),
    path('export_pdf', views.export_pdf, name='export_pdf'),
]