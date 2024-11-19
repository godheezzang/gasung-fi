from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView
from django.urls import path
from accounts import views
from accounts.serializers import UserLoginSerializer, UserRegisterSerializer

urlpatterns = [
    path('<int:user_id>/', views.user_detail),
    path('login/', LoginView.as_view(serializer_class=UserLoginSerializer)),
    path('signup/', RegisterView.as_view(serializer_class=UserRegisterSerializer)),
    path('password/change/', views.password_change),
]