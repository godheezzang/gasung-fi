from django.urls import path
from articles import views
urlpatterns = [
    path('', views.create_or_list_articles),
    path('<int:article_id>/', views.article_detail),
    path('<int:article_id>/comments/', views.create_or_list_comments),
    path('<int:article_id>/comments/<int:comment_id>/', views.comment_detail),

]