from django.shortcuts import render, get_list_or_404, get_object_or_404
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import (DepositSerializer,
                          DepositOptionsSerializer,
                          InstallmentSavingsSerializer,
                          InstallmentSavingsOptionsSerializer,
                          DepositListSerializer,
                          InstallmentSavingsListSerializer)
from .models import (Deposit,
                     DepositOptions,
                     InstallmentSavings,
                     InstallmentSavingsOptions)
from gasung_fi import my_settings
# Create your views here.
BASE_URL = 'http://finlife.fss.or.kr/finlifeapi/'
API_KEY = my_settings.FIN_API_KEY

def get_value_with_default(data, key, default) :
    return data.get(key, default) if data.get(key) is not None else default

@api_view(['GET',])
def getDepositProduct(request):
    if request.method == 'GET':
        URL = BASE_URL + 'depositProductsSearch.json'
        params = {
            'auth' : API_KEY,
            'topFinGrpNo' : '020000',
            'pageNo' : '1',
        }
        response = requests.get(URL, params=params).json()
        products = response.get("result").get("baseList", [])
        for product in products:
            if not Deposit.objects.filter(fin_prdt_cd=product.get("fin_prdt_cd")).exists():
                serializer = DepositSerializer(data={
                    'fin_prdt_cd': product.get("fin_prdt_cd"),
                    'mtrt_int' : get_value_with_default(product, 'mtrt_int', '-1'),
                    'kor_co_nm': get_value_with_default(product, "kor_co_nm", "-1"),
                    'join_deny': get_value_with_default(product, "join_deny", "-1"),
                    'join_member': get_value_with_default(product, "join_member", "-1"),
                    'join_way': get_value_with_default(product, "join_way", "-1"),
                    'spcl_cnd': get_value_with_default(product, "spcl_cnd", "-1"),
                })

                if serializer.is_valid(raise_exception=True):
                    serializer.save()

        options = response.get("result").get("optionList", [])
        for option in options:
            fin_prdt_cd = option.get("fin_prdt_cd")
            product = Deposit.objects.get(fin_prdt_cd=fin_prdt_cd)
            if not DepositOptions.objects.filter(fin_prdt_cd=product,
                                                 intr_rate_type=option.get("intr_rate_type"),
                                                 intr_rate=option.get("intr_rate"),
                                                 intr_rate2=option.get("intr_rate2"),
                                                 save_trm=option.get("save_trm")).exists():
                serializer = DepositOptionsSerializer(data={
                    'intr_rate_type': get_value_with_default(option, "intr_rate_type", "-1"),
                    'intr_rate_type_nm': get_value_with_default(option, "intr_rate_type_nm", "-1"),
                    'intr_rate': get_value_with_default(option, "intr_rate", -1),
                    'intr_rate2': get_value_with_default(option, "intr_rate2", -1),
                    'save_trm': get_value_with_default(option, "save_trm", "-1"),
                })
                if serializer.is_valid(raise_exception=True):
                    serializer.save(fin_prdt_cd=product)
        message = {
            "status": "success",
            "message" : "예금 데이터가 성공적으로 저장되었습니다."
        }
        return Response(message, status=status.HTTP_200_OK)

@api_view(['GET',])
def getInstallmentSavingsProducts(request):
    if request.method == 'GET':
        URL = BASE_URL + 'savingProductsSearch.json'
        params = {
            'auth' : API_KEY,
            'topFinGrpNo' : '020000',
            'pageNo' : '1',
        }
        response = requests.get(URL, params=params).json()
        products = response.get("result").get("baseList", [])
        for product in products:
            if not InstallmentSavings.objects.filter(fin_prdt_cd=product.get("fin_prdt_cd")).exists():
                serializer = InstallmentSavingsSerializer(data={
                    'fin_prdt_cd': product.get("fin_prdt_cd"),
                    'mtrt_int' : get_value_with_default(product, 'mtrt_int', '-1'),
                    'kor_co_nm': get_value_with_default(product, "kor_co_nm", "-1"),
                    'join_deny': get_value_with_default(product, "join_deny", "-1"),
                    'join_member': get_value_with_default(product, "join_member", "-1"),
                    'join_way': get_value_with_default(product, "join_way", "-1"),
                    'spcl_cnd': get_value_with_default(product, "spcl_cnd", "-1"),
                })

                if serializer.is_valid(raise_exception=True):
                    serializer.save()

        options = response.get("result").get("optionList", [])
        for option in options:
            fin_prdt_cd = option.get("fin_prdt_cd")
            product = InstallmentSavings.objects.get(fin_prdt_cd=fin_prdt_cd)
            if not InstallmentSavingsOptions.objects.filter(fin_prdt_cd=product,
                                                 intr_rate_type=option.get("intr_rate_type"),
                                                 intr_rate=option.get("intr_rate"),
                                                 intr_rate2=option.get("intr_rate2"),
                                                 save_trm=option.get("save_trm"),
                                                 rsrv_type=option.get("rsrv_type")).exists():
                serializer = InstallmentSavingsOptionsSerializer(data={
                    'intr_rate_type': get_value_with_default(option, "intr_rate_type", "-1"),
                    'intr_rate_type_nm': get_value_with_default(option, "intr_rate_type_nm", "-1"),
                    'intr_rate': get_value_with_default(option, "intr_rate", -1),
                    'intr_rate2': get_value_with_default(option, "intr_rate2", -1),
                    'save_trm': get_value_with_default(option, "save_trm", "-1"),
                    'rsrv_type': get_value_with_default(option, "rsrv_type", "-1"),
                    'rsrv_type_nm': get_value_with_default(option, "rsrv_type_nm", "-1"),
                })
                if serializer.is_valid(raise_exception=True):
                    serializer.save(fin_prdt_cd=product)
        message = {
            "status": "success",
            "message" : "적금 데이터가 성공적으로 저장되었습니다."
        }
        return Response(message, status=status.HTTP_200_OK)

@api_view(['GET',])
def depositList(request) :
    if request.method == 'GET':
        deposits = get_list_or_404(Deposit)
        serializer = DepositListSerializer(deposits, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET',])
def depositDetail(request, fin_prdt_cd) :
    if request.method == 'GET':
        deposit = get_object_or_404(Deposit, fin_prdt_cd=fin_prdt_cd)
        serializer = DepositListSerializer(deposit)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET',])
def installmentSavingsList(request) :
    if request.method == 'GET':
        installment_savings = get_list_or_404(InstallmentSavings)
        serializer = InstallmentSavingsListSerializer(installment_savings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET',])
def installmentSavingsDetail(request, fin_prdt_cd) :
    if request.method == 'GET':
        installment_savings = get_object_or_404(InstallmentSavings, fin_prdt_cd=fin_prdt_cd)
        serializer = InstallmentSavingsListSerializer(installment_savings)
        return Response(serializer.data, status=status.HTTP_200_OK)