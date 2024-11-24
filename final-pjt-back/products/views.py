from django.shortcuts import render, get_list_or_404, get_object_or_404
import requests
from django.conf import settings
from django.core.mail import send_mail
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
import random
from faker import Faker
import pandas as pd
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
fake = Faker()
User = get_user_model()

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
                    'dcls_month' : get_value_with_default(product, 'dcls_month', '-'),
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
                    'dcls_month' : get_value_with_default(product, 'dcls_month', '-'),
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
def deposit_intr_rate_update(request, fin_prdt_cd, depotis_option_id) :
    deposit_option = get_object_or_404(DepositOptions, fin_prdt_cd=fin_prdt_cd, pk=depotis_option_id)
    serializer = DepositOptionsUpdateSerializer(deposit_option, data=request.data, partial=True)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        send_email(fin_prdt_cd, True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT',])
@permission_classes([IsAdminUser])
def installment_savings_intr_rate_update(request, fin_prdt_cd, installment_savings_option_id) :
    installment_savings_option = get_object_or_404(InstallmentSavingsOptions,
                                                   fin_prdt_cd=fin_prdt_cd,
                                                   pk=installment_savings_option_id)
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

@api_view(['POST',])
@permission_classes([IsAdminUser])
def create_dummy_data(request) :
    nums_user = int(request.data.get('nums_user', 10))
    num_products_per_user = int(request.data.get('num_products_per_user', 5))
    existing_deposit_prdt_cd = set(Deposit.objects.values_list('fin_prdt_cd', flat=True))
    existing_installment_savings_prdt_cd = set(InstallmentSavings.objects.values_list('fin_prdt_cd', flat=True))
    total_prdt_cd = existing_deposit_prdt_cd.union(existing_installment_savings_prdt_cd)
    users_to_create = []
    products_to_create = []
    for _ in range(nums_user) :
        while True :
            email = fake.unique.email()
            if not User.objects.filter(email=email).exists():
                break
        user = User(
            username=fake.user_name(),
            email=email,
            age=random.randint(18, 70),
            assets=random.randint(1000, 100000),
            income=random.randint(3000, 30000),
            gender=random.choice(['M', 'F'])
        )
        user.set_password(fake.password())
        users_to_create.append(user)

    User.objects.bulk_create(users_to_create)
    for user in users_to_create:
        save_user = get_object_or_404(User, email = user.email)
        token, created = Token.objects.get_or_create(user=save_user)
        existing_user_product_cds = set(UserProducts.objects.filter(user=save_user).values_list('fin_prdt_cd', flat=True))
        available_prdt_cd = list(total_prdt_cd - existing_user_product_cds)
        for _ in range(num_products_per_user) :
            if not available_prdt_cd :
                break
            fin_prdt_cd = random.choice(available_prdt_cd)
            deposit_product = Deposit.objects.filter(fin_prdt_cd=fin_prdt_cd).first()
            if deposit_product:
                kor_co_nm = deposit_product.kor_co_nm
                fin_prdt_nm = deposit_product.fin_prdt_nm
                product_type = "정기 예금"
            else:
                installment_product = InstallmentSavings.objects.filter(fin_prdt_cd=fin_prdt_cd).first()
                if installment_product:
                    kor_co_nm = installment_product.kor_co_nm
                    fin_prdt_nm = installment_product.fin_prdt_nm
                    product_type = "정기 적금"
                else:
                    continue

            products_to_create.append(UserProducts(
                user=save_user,
                fin_prdt_cd=fin_prdt_cd,
                product_type=product_type,
                kor_co_nm=kor_co_nm,
                fin_prdt_nm=fin_prdt_nm
            ))
            available_prdt_cd.remove(fin_prdt_cd)
    UserProducts.objects.bulk_create(products_to_create)
    message = {
        "status" : "success",
        "message" : f"{nums_user}명의 유저가 생성되었습니다."
    }
    return Response(message, status=status.HTTP_201_CREATED)

@api_view(['GET',])
@permission_classes([IsAuthenticated])
def recommend_list(request) :
    user = request.user
    age = user.age
    assets = user.assets
    income = user.income
    all_users = User.objects.all().values('id', 'income', 'age', 'assets')
    df_users = pd.DataFrame(all_users)
    similar_users = df_users[
        (df_users['age'] >= age - 5) & (df_users['age'] <= age + 5) &
        (df_users["income"] >= income - 1000) & (df_users["income"] <= income + 1000) &
        (df_users['assets'] >= assets - 10000) & (df_users['assets'] <= assets + 10000)
    ]

    similar_users_ids = similar_users['id'].tolist()
    user_products = UserProducts.objects.filter(user_id__in=similar_users_ids)
    recommended_products = (UserProducts.objects.filter(user_id__in=similar_users_ids).exclude(fin_prdt_cd__in=user_products))
    df_products = pd.DataFrame(list(recommended_products.values('fin_prdt_cd','fin_prdt_nm', 'product_type', 'kor_co_nm')))
    product_counts = df_products.groupby(['fin_prdt_cd','fin_prdt_nm', 'product_type', 'kor_co_nm']).size().reset_index(name='count')
    top_products = product_counts.sort_values(by='count', ascending=False).head(10)
    result = [
        {
            "fin_prdt_cd" : row['fin_prdt_cd'],
            "fin_prdt_nm" : row['fin_prdt_nm'],
            "product_type": row['product_type'],
            "kor_co_nm": row['kor_co_nm'],
            "count": row['count']
        }
        for _, row in top_products.iterrows()
    ]
    return Response(result, status=status.HTTP_200_OK)




