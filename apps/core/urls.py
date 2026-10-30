from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.landing_view, name='landing'),
    path('api/spin-wheel/', views.spin_wheel_api, name='spin_wheel_api'),
    path('api/quiz-recommend/', views.quiz_recommend_api, name='quiz_recommend_api'),
]
