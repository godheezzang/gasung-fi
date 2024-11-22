from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from dj_rest_auth.registration.views import LoginView

from accounts.serializers import (UserDetailSerializer,
                                  UserUpdateSerializer)


# Create your views here.
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def user_detail(request):
    user = request.user
    if request.method == 'GET':
        serializer = UserDetailSerializer(user)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    elif request.method == 'DELETE':
        user.delete()
        data = {
            "data" : "회원 탈퇴 완료"
        }
        return Response(data, status=status.HTTP_204_NO_CONTENT)

class CustomLoginView(LoginView) :
    def get_response(self):
        response_data = super().get_response().data
        response_data['username'] = self.serializer.validated_data['user'].username
        return Response(response_data, status=status.HTTP_200_OK)