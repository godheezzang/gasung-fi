from dj_rest_auth.serializers import LoginSerializer, UserDetailsSerializer
from django.contrib.auth import get_user_model
from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers

User = get_user_model()

class UserRegisterSerializer(RegisterSerializer):
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('이 이메일은 이미 사용 중입니다.')
        return value

class UserLoginSerializer(LoginSerializer):
    username = None
    def validate(self,attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("이메일 또는 비밀번호가 잘못되었습니다.")
        if not user.check_password(password):
            raise serializers.ValidationError("이메일 또는 비밀번호가 잘못되었습니다.")
        attrs['user'] = user
        return attrs

class UserDetailSerializer(UserDetailsSerializer) :
    class Meta(UserDetailsSerializer.Meta):
        model = User
        fields = ('username', 'email', 'age', 'assets', 'income', 'gender',)


