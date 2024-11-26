from django.urls import path
from products import views
urlpatterns = [
    path('get_deposit_products/', views.get_deposit_product),
    path('get_installment_savings_products/', views.get_installment_savings_products),
    path('deposit/', views.deposit_list),
    path('deposit/<str:fin_prdt_cd>/', views.deposit_detail),
    path('installment_savings/', views.installment_savings_list),
    path('installment_savings/<str:fin_prdt_cd>/', views.installment_savings_detail),
    path('deposit/search', views.deposit_search),
    path('installment_savings/search', views.installment_savings_search),
    path('deposit/<str:fin_prdt_cd>/<int:deposit_option_id>/', views.deposit_intr_rate_update),
    path('installment_savings/<str:fin_prdt_cd>/<int:installment_savings_option_id>/', views.installment_savings_intr_rate_update),
    path('create_dummy_data/', views.create_dummy_data),
    path('recommend_list/', views.recommend_list),
    path('random_recommend_list/', views.random_recommend_list),
]