from django.urls import path
from . import views

urlpatterns = [

    path(
        'dashboard/',
        views.billing_dashboard,
        name='billing_dashboard'
    ),
    path('create/',views.create_bill,name='create_bill'),
    path('receipt/<int:bill_id>/',views.bill_receipt,name='bill_receipt'),
]