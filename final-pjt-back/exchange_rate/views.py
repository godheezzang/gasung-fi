from django.shortcuts import render
import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from gasung_fi import my_settings
from datetime import datetime, timedelta
# Create your views here.
API_KEY = my_settings.EX_API_KEY
@api_view(['GET',])
@permission_classes([IsAuthenticated])
def get_exchange_rates(request):
    if request.method == 'GET':
        URL = 'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON'
        params = {
            "authkey" : API_KEY,
            "data" : "AP01"
        }
        response = requests.get(URL, params=params).json()
        if response is None or len(response) == 0:
            today = datetime.today()
            for i in range(1, 31):  # 최대 30일 전까지 요청
                search_date = (today - timedelta(days=i)).strftime('%Y%m%d')
                params['searchdate'] = search_date
                response = requests.get(URL, params=params).json()

                if response is not None and len(response) > 0:
                    break

        return Response(response, status=status.HTTP_200_OK)
