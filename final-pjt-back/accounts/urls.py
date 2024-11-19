from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView
from dj_rest_auth import views as rest_auth_views
from django.urls import path
from accounts import views
from accounts.serializers import UserLoginSerializer, UserRegisterSerializer, UserDetailSerializer

urlpatterns = [
    path('<int:user_id>/', views.user_detail),
    path('login/', LoginView.as_view(serializer_class=UserLoginSerializer)),
    path('signup/', RegisterView.as_view(serializer_class=UserRegisterSerializer)),
    path('detail/', rest_auth_views.UserDetailsView.as_view(serializer_class=UserDetailSerializer)),
    path('password/change/', views.password_change),
]