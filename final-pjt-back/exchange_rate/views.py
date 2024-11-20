from django.shortcuts import render
import requests
from rest_framework.response import Response
from rest_framework.decorators import api_view
from gasung_fi import my_settings
# Create your views here.
API_KEY = my_settings.EX_API_KEY
@api_view(['POST',])
def getExchangeRates(request):
    if request.method == 'POST':
        data = request.data
        foreign_amount = data.get('foreign_amount')
        foreign_currency = data.get('foreign_currency')
        krw_amount = data.get('krw_amount')

        URL = 'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON'
        params = {
            "authkey" : API_KEY,
            "data" : "AP01"
        }
        response = requests.get(URL, params=params).json()
        exchange_rates = {item['cur_nm']: float(item['deal_bas_r'].replace(',','')) for item in response}
        converted_amount = None
        if krw_amount is not None and krw_amount > 0:
            converted_amount = krw_amount / exchange_rates.get(foreign_currency, 0)
        elif foreign_amount is not None and foreign_amount > 0:
            converted_amount = foreign_amount * exchange_rates.get(foreign_currency, 1)
        return Response({"변환된 금액" : round(converted_amount, 5)})
