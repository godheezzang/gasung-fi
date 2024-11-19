from django.urls import path
from products import views
urlpatterns = [
    path('getDepositProducts/', views.getDepositProduct),
    path('getInstallmentSavingsProducts/', views.getInstallmentSavingsProducts),
]