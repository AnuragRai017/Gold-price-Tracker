# goldprice_app/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import register
from .views import profile

urlpatterns = [
    path('', views.home, name='home'),  # Root URL to home view
    path('home/', views.home, name='home_page'),  # Explicitly handle '/home'
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('prices/', views.get_gold_prices, name='get_gold_prices'),
]