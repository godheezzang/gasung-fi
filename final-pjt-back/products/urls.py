from django.urls import path
from products import views
urlpatterns = [
    path('getDepositProducts/', views.get_deposit_product),
    path('getInstallmentSavingsProducts/', views.get_installment_savings_products),
    path('deposit/', views.deposit_list),
    path('deposit/<str:fin_prdt_cd>/', views.deposit_detail),
    path('installmentSavings/', views.installment_savings_list),
    path('installmentSavings/<str:fin_prdt_cd>/', views.installment_savings_detail),
    path('deposit/search', views.deposit_search),
    path('installmentSavings/search', views.installment_savings_search),
]