from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('<int:order_id>/initiate/', views.initiate_payment, name='initiate_payment'),
    path('<int:order_id>/success/', views.payment_success, name='payment_success'),
    path('<int:order_id>/failed/', views.payment_failed, name='payment_failed'),
]
