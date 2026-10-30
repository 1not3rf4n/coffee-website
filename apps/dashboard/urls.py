from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_index_view, name='index'),
    path('settings/', views.dashboard_settings_view, name='settings'),
    path('menu/', views.dashboard_menu_view, name='menu'),
    path('reservations/', views.dashboard_reservations_view, name='reservations'),
    path('orders/', views.dashboard_orders_view, name='orders'),
]
