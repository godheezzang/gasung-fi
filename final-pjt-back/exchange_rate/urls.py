from django.urls import path
from exchange_rate import views
urlpatterns = [
    path('getExchangeRates/', views.get_exchange_rates),
]