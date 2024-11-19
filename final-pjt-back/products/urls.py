from django.urls import path
from products import views
urlpatterns = [
    path('getDepositProducts/', views.getDepositProduct),
    path('getInstallmentSavingsProducts/', views.getInstallmentSavingsProducts),
    path('deposit/', views.depositList),
    path('deposit/<str:fin_prdt_cd>/', views.depositDetail),
    path('installmentSavings/', views.installmentSavingsList),
    path('installmentSavings/<str:fin_prdt_cd>/', views.installmentSavingsDetail),
]