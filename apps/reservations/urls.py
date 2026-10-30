from django.urls import path
from . import views

app_name = 'reservations'

urlpatterns = [
    path('', views.reservation_view, name='index'),
    path('deposit/<int:reservation_id>/', views.deposit_pay_view, name='deposit_pay'),
    path('success/<int:reservation_id>/', views.reservation_success_view, name='success'),
]
