from django.urls import path
from . import views

urlpatterns = [
    path('add_bill', views.add_bill ,name='add_bill'),
    path('view_bills', views.view_bills ,name='view_bills'),
    path('pay_bill/<int:bill_id>', views.paid_bill ,name='paid_bill'),
]