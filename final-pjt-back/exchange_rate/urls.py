from django.urls import path
from exchange_rate import views
urlpatterns = [
    path('get_exchange_rates/', views.get_exchange_rates),
]