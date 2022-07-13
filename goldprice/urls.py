from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('gold-price-ounce/', views.gold_ounce, name='ounce'),
    path('silver-price/', views.silver_price, name='silver'),
    # path('articles/<int:year>/', views.year_archive),
]