from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView, PasswordChangeView, LogoutView
from django.urls import path
from accounts import views
from accounts.serializers import UserLoginSerializer, UserRegisterSerializer, UserDetailSerializer

urlpatterns = [
    path('login/', LoginView.as_view(serializer_class=UserLoginSerializer)),
    path('signup/', RegisterView.as_view(serializer_class=UserRegisterSerializer)),
    path('detail/', views.user_detail),
    path('password/change/', PasswordChangeView.as_view()),
    path('logout/', LogoutView.as_view()),
]