from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail_view, name='detail'),
    path('api/add/', views.cart_add_api, name='add_api'),
    path('api/remove/', views.cart_remove_api, name='remove_api'),
    path('api/update/', views.cart_update_api, name='update_api'),
]
