from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('سعر اونص الذهب في ألمانيا اليوم/', views.gold_ounce, name='ounce'),
    path('سعر الفضة في ألمانيا/', views.silver_price, name='silver'),
    # path('articles/<int:year>/', views.year_archive),
]