from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('track/', views.order_track_view, name='track'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('payment/<int:order_id>/', views.payment_mock_view, name='payment_mock'),
    path('payment/<int:order_id>/verify/', views.payment_verify_view, name='payment_verify'),
    path('success/<int:order_id>/', views.order_success_view, name='order_success'),
]
