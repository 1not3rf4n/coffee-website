from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.shop_index_view, name='index'),
    path('<slug:slug>/', views.product_detail_view, name='detail'),
]
