from django.shortcuts import render, get_list_or_404, get_object_or_404
import requests
from django.conf import settings
from django.core.mail import send_mail
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from .serializers import (DepositSerializer,
                          DepositOptionsSerializer,
                          InstallmentSavingsSerializer,
                          InstallmentSavingsOptionsSerializer,
                          DepositListSerializer,
                          InstallmentSavingsListSerializer,
                          UserProductsSerializer,
                          InstallmentSavingsOptionsUpdateSerializer,
                          DepositOptionsUpdateSerializer)
from .models import (Deposit,
                     DepositOptions,
                     InstallmentSavings,
                     InstallmentSavingsOptions,
                     UserProducts)
from gasung_fi import my_settings
# Create your views here.
BASE_URL = 'http://finlife.fss.or.kr/finlifeapi/'
API_KEY = my_settings.FIN_API_KEY

def get_value_with_default(data, key, default) :
    return data.get(key, default) if data.get(key) is not None else default

@api_view(['GET',])
def get_deposit_product(request):
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
                    'mtrt_int' : get_value_with_default(product, 'mtrt_int', '-'),
                    'fin_prdt_nm' : get_value_with_default(product, 'fin_prdt_nm', '-'),
                    'kor_co_nm': get_value_with_default(product, "kor_co_nm", "-"),
                    'join_deny': get_value_with_default(product, "join_deny", "-"),
                    'join_member': get_value_with_default(product, "join_member", "-"),
                    'join_way': get_value_with_default(product, "join_way", "-"),
                    'spcl_cnd': get_value_with_default(product, "spcl_cnd", "-"),
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
                    'intr_rate_type': get_value_with_default(option, "intr_rate_type", "-"),
                    'intr_rate_type_nm': get_value_with_default(option, "intr_rate_type_nm", "-"),
                    'intr_rate': get_value_with_default(option, "intr_rate", -1),
                    'intr_rate2': get_value_with_default(option, "intr_rate2", -1),
                    'save_trm': get_value_with_default(option, "save_trm", "-"),
                })
                if serializer.is_valid(raise_exception=True):
                    serializer.save(fin_prdt_cd=product)
        message = {
            "status": "success",
            "message" : "예금 데이터가 성공적으로 저장되었습니다."
        }
        return Response(message, status=status.HTTP_200_OK)

@api_view(['GET',])
def get_installment_savings_products(request):
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
                    'mtrt_int' : get_value_with_default(product, 'mtrt_int', '-'),
                    'kor_co_nm': get_value_with_default(product, "kor_co_nm", "-"),
                    'fin_prdt_nm': get_value_with_default(product, "fin_prdt_nm", "-"),
                    'join_deny': get_value_with_default(product, "join_deny", "-"),
                    'join_member': get_value_with_default(product, "join_member", "-"),
                    'join_way': get_value_with_default(product, "join_way", "-"),
                    'spcl_cnd': get_value_with_default(product, "spcl_cnd", "-"),
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
                    'intr_rate_type': get_value_with_default(option, "intr_rate_type", "-"),
                    'intr_rate_type_nm': get_value_with_default(option, "intr_rate_type_nm", "-"),
                    'intr_rate': get_value_with_default(option, "intr_rate", -1),
                    'intr_rate2': get_value_with_default(option, "intr_rate2", -1),
                    'save_trm': get_value_with_default(option, "save_trm", "-"),
                    'rsrv_type': get_value_with_default(option, "rsrv_type", "-"),
                    'rsrv_type_nm': get_value_with_default(option, "rsrv_type_nm", "-"),
                })
                if serializer.is_valid(raise_exception=True):
                    serializer.save(fin_prdt_cd=product)
        message = {
            "status": "success",
            "message" : "적금 데이터가 성공적으로 저장되었습니다."
        }
        return Response(message, status=status.HTTP_200_OK)

@api_view(['GET',])
def deposit_list(request) :
    if request.method == 'GET':
        deposits = get_list_or_404(Deposit)
        serializer = DepositListSerializer(deposits, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET','POST'])
def deposit_detail(request, fin_prdt_cd) :
    deposit = get_object_or_404(Deposit, fin_prdt_cd=fin_prdt_cd)
    if request.method == 'GET':
        serializer = DepositListSerializer(deposit)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        data = {
            "fin_prdt_cd" : fin_prdt_cd,
            "product_type" : "정기 예금",
            "kor_co_nm" : deposit.kor_co_nm,
            "fin_prdt_nm" : deposit.fin_prdt_nm,
        }
        serializer = UserProductsSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user = request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET',])
def installment_savings_list(request) :
    if request.method == 'GET':
        installment_savings = get_list_or_404(InstallmentSavings)
        serializer = InstallmentSavingsListSerializer(installment_savings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
def installment_savings_detail(request, fin_prdt_cd) :
    installment_savings = get_object_or_404(InstallmentSavings, fin_prdt_cd=fin_prdt_cd)
    if request.method == 'GET':
        serializer = InstallmentSavingsListSerializer(installment_savings)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        data = {
            "fin_prdt_cd" : fin_prdt_cd,
            "product_type" : "정기 적금",
            "kor_co_nm" : installment_savings.kor_co_nm,
            "fin_prdt_nm" : installment_savings.fin_prdt_nm,
        }
        serializer = UserProductsSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user = request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET',])
def deposit_search(request) :
    if request.method == 'GET':
        kor_co_nm = request.query_params.get('bank_name', "")
        save_trm = request.query_params.get('save_trm', "")
        filter_conditions = {}
        if kor_co_nm :
            filter_conditions['kor_co_nm'] = kor_co_nm
        if save_trm :
            filter_conditions['deposit_options__save_trm'] = save_trm
        if filter_conditions :
            deposit = Deposit.objects.filter(**filter_conditions)
        else :
            deposit = Deposit.objects.all()
        serializer = DepositListSerializer(deposit, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET',])
def installment_savings_search(request) :
    if request.method == 'GET':
        kor_co_nm = request.query_params.get('bank_name', "")
        save_trm = request.query_params.get('save_trm', "")
        filter_conditions = {}
        if kor_co_nm :
            filter_conditions['kor_co_nm'] = kor_co_nm
        if save_trm :
            filter_conditions['deposit_options__save_trm'] = save_trm
        if filter_conditions :
            installmentSavings = InstallmentSavings.objects.filter(**filter_conditions)
        else :
            installmentSavings = InstallmentSavings.objects.all()
        serializer = InstallmentSavingsListSerializer(installmentSavings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT',])
@permission_classes([IsAdminUser])
def deposit_intr_rate_update(request, fin_prdt_cd, save_trm) :
    deposit_option = get_object_or_404(DepositOptions, fin_prdt_cd=fin_prdt_cd, save_trm=save_trm)
    serializer = DepositOptionsUpdateSerializer(deposit_option, data=request.data, partial=True)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        send_email(fin_prdt_cd, True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT',])
@permission_classes([IsAdminUser])
def installment_savings_intr_rate_update(request, fin_prdt_cd, save_trm, rsrv_type) :
    installment_savings_option = get_object_or_404(InstallmentSavingsOptions,
                                                   fin_prdt_cd=fin_prdt_cd,
                                                   save_trm=save_trm,
                                                   rsrv_type=rsrv_type)
    serializer = InstallmentSavingsOptionsUpdateSerializer(installment_savings_option, data=request.data, partial=True)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        send_email(fin_prdt_cd, False)
        return Response(serializer.data, status=status.HTTP_200_OK)


def send_email(fin_prdt_cd, is_deposit):
    if is_deposit :
        product = get_object_or_404(Deposit, fin_prdt_cd=fin_prdt_cd)
        options = product.deposit_options.all()
    else :
        product = get_object_or_404(InstallmentSavings, fin_prdt_cd=fin_prdt_cd)
        options = product.installment_savings_options.all()
    fin_prdt_nm = product.fin_prdt_nm
    user_products = get_list_or_404(UserProducts, fin_prdt_cd=fin_prdt_cd)
    user_emails = [user_product.user.email for user_product in user_products]

    subject = f'금리 수정 확인 - 상품명 : {fin_prdt_nm}'
    recipient_list = user_emails
    mail_message = ''
    for option in options :
        if is_deposit :
            mail_message += f'가입기간 : {option.save_trm} - 금리 : {option.intr_rate} - 우대금리 : {option.intr_rate2}\n'
        else :
            mail_message += f'가입기간 : {option.save_trm} - 금리 : {option.intr_rate} - 우대금리 : {option.intr_rate2} - 적립유형 - {option.rsrv_type_nm}\n'
    message = f'''
    {fin_prdt_nm}상품의 금리가 다음과 같이 변경되었습니다.\n\n
    {mail_message}
    
    감사합니다.
    '''

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        recipient_list,
        fail_silently=False,
    )
