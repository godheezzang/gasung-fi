from django.urls import path
from articles import views
urlpatterns = [
    path('', views.create_or_list_articles),
    path('<int:article_id>/', views.article_detail),
]