# Gasung-Fi

<!--배지-->
![MIT License][license-shield] 

<!--프로젝트 대문 이미지-->
![Project Title](img/project-title.png)

<!--목차-->
# Table of Contents
- [[1] About the Project](#1-about-the-project)
  - [Features](#features)
  - [Technologies](#technologies)
- [[2] Getting Started](#2-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
- [[3] Usage](#3-usage)
- [[4] AI Use](#4-ai-use)
- [[5] Team](#5-team)
- [[6] Review](#6-review)
- [[7] License](#7-license)



# [1] About the Project

- 사용자가 금융 상품을 쉽고 빠르게 비교할 수 있도록 설계된 웹 어플리케이션입니다.
- 사용자들이 필요한 금융 서비스를 보다 편리하게 이용할 수 있도록 돕습니다.

## Architecture

![Architecture](https://file.miricanvas.com/user_image/2024/11/27/01/10/kns1sr8x7r2hs58e/image.png?size=400)

## ERD

![ERD](https://file.miricanvas.com/user_image/2024/11/27/00/20/ku8he4jh4tvkumy7/image.png?size=400)

## Technologies

- [Python](https://docs.python.org/ko/3/) 3.12
- [MySQL](https://www.mysql.com/) 8.0
- [Django](https://docs.djangoproject.com/ko/4.2/) 4.2.16
- [Vue.js](https://v3-docs.vuejs-korea.org/) 3.5.12
- [Javascript](https://developer.mozilla.org/ko/docs/Web/JavaScript)
- [pinia](https://pinia.vuejs.kr/) 2.2.6
- [chart.js](https://www.chartjs.org/docs/latest/) 3.9.1
- [axios](https://axios-http.com/kr/docs/intro) 1.7.7
- [requests](https://requests.readthedocs.io/en/latest/) 2.32.3
- [pandas](https://pandas.pydata.org/docs/) 2.2.3
- [dj-rest-auth](https://dj-rest-auth.readthedocs.io/en/latest/) 7.0.0
- [django-rest-framework](https://www.django-rest-framework.org/) 3.15.2
- [django-allauth](https://docs.allauth.org/en/latest/) 0.61.1
- [django-cors-headers](https://pypi.org/project/django-cors-headers/) 4.6.0


# [2] Getting Started

## Prerequisites

- [Open API key](https://openai.com/index/openai-api/)
- [금융상품통합비교공시 API key](https://finlife.fss.or.kr/finlife/main/contents.do?menuNo=700029)
- [한국수출입은행 환율정보 API key](https://www.koreaexim.go.kr/ir/HPHKIR020M01?apino=2&viewtype=C&searchselect=&searchword=)
- [Kakao map API key](https://apis.map.kakao.com/)

## Installation
- Repository 클론
```bash
git clone https://lab.ssafy.com/myhamah/final-pjt.git
```
### 프론트엔드 부분
1. NPM packages 설치
```bash
npm install
```
2. Vue 실행
```bash
npm run dev
```
### 백엔드 부분
1. pip packages 설치
```bash
pip install -r requirements.txt
```
2. python migrate
```bash
python manage.py migrate
```
3. python runserver
```bash
python manage.py runserver
```

## Configuration
- `.env`에 VITE_BASE_URL, VITE_KAKAO_MAP_KEY 입력
```bash
const VITE_BASE_URL = "BASE_URL";
const VITE_KAKAO_MAP_KEY = "<Your API key>";
```
- `my_settings.py`에 내용 입력
```bash
FIN_API_KEY = "<Your API key>"
EX_API_KEY = "<Your API key>"
MY_DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '데이터베이스 이름',
        'USER': '유저 이름',
        'PASSWORD': '유저 비밀번호',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

EMAIL_HOST_USER = "메일 주소"
EMAIL_HOST_PASSWORD = "메일 비밀번호"

OPENAI_API_KEY = '<Your API key>'
```

# [3] Usage

![게시글 CRUD](img/usage.png)

- 게시글 생성, 수정, 조회, 삭제 기능
- 게시글 조회 시 댓글도 같이 반환
- 댓글 생성, 수정, 삭제 기능
- 대댓글 작성 가능
- 게시글 더미 데이터 생성 기능(댓글 까지만 가능 대댓글은 불가)

## 게시글, 댓글 CRUD API
```python
@api_view(['GET', 'POST',])
def create_or_list_articles(request):
    if request.method == 'GET':
        articles = Article.objects.all().order_by('-created_at')
        paginator = ArticlesPagination()
        paginated_articles = paginator.paginate_queryset(articles, request)
        serializer = ArticleListSerializer(paginated_articles, many=True)
        return paginator.get_paginated_response(serializer.data)
    elif request.method == 'POST':
        serializer = ArticleCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
@api_view(['GET', 'PUT','DELETE',])
def article_detail(request, article_id):
    article = get_object_or_404(Article.objects.prefetch_related('comments__replies'), pk=article_id)
    if request.method in ['DELETE', 'PUT'] :
        if request.user != article.user:
            message = {
                "detail" : "권한이 없습니다."
            }
            return Response(message, status=status.HTTP_403_FORBIDDEN)
    if request.method == 'GET':
        serializer = ArticleListSerializer(article)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = ArticleListSerializer(article, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        article.delete()
        message = {
            'data' : f'{article_id}번 게시글이 삭제되었습니다.'
        }
        return Response(message, status=status.HTTP_204_NO_CONTENT)
```
```python
@api_view(['POST',])
@permission_classes([IsAuthenticated])
def create_comments(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    if request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, article=article)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['DELETE', 'PUT', 'POST'])
@permission_classes([IsAuthenticated])
def comment_detail(request, article_id, comment_id):
    article = get_object_or_404(Article, pk=article_id)
    comment = get_object_or_404(Comment, article = article, pk=comment_id)
    if request.method in ['DELETE', 'PUT'] :
        if request.user != comment.user:
            message = {
                "detail" : "권한이 없습니다."
            }
            return Response(message, status=status.HTTP_403_FORBIDDEN)
    if request.method == 'DELETE':
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, article=article, main_comment=comment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
```
```python
@api_view(['POST',])
@permission_classes([IsAdminUser])
def create_dummy_article(request) :
    nums_article = int(request.data.get('nums_article', 10))
    num_comments_per_article = int(request.data.get('num_comments_per_article', 5))
    articles_to_create = []
    for _ in range(nums_article) :
        user = User.objects.order_by('?').first()

        article = Article(
            user=user,
            title=fake.sentence(nb_words=6),
            content=fake.text(),
        )
        article.save()
        articles_to_create.append(article)
    for article in articles_to_create:
        for _ in range(num_comments_per_article) :
            user = User.objects.order_by('?').first()
            comment = Comment(
                user=user,
                article=article,
                main_comment=None,
                content=fake.text(),
            )
            comment.save()

    message = {
        "status" : "success",
        "message" : f"{nums_article}개의 게시글이 생성되었습니다."
    }
    return Response(message, status=status.HTTP_201_CREATED)
```



![상품 추천](img/usage.png)

- pandas를 사용하여 로그인한 사용자와 비슷한 조건(나이, 연봉, 자산)의 사용자들이 어떠한 상품을 가입했는지 조회 후 추천
- 로그인한 사용자가 이미 가입한 상품은 추천하지 않음
- 조건을 나이 +-5, 연봉 +- 1000만원, 자산 +- 1억 으로 설정해놓음
- 전체 사용자의 나이 연봉 자산 필드의 값만 불러와서 dataframe으로 변환
- 변환된 dataframe을 활용하여 조건이 맞는 데이터만 추출
- 그 데이터프레임의 id 필드만 리스트로 추출
- 이미 내가 찜한 상품의 키 값을 가져와서 사용자와 비슷한 조건의 다른 사용자들이 찜한 상품들에서 내가 찜한 상품의 키 값과 일치하는 상품은 제외
- 추천 받은 상품들의 코드, 상품명, 예금 적금 타입, 은행명 필드만 추출해서 몇 명의 사용자가 그 상품에 가입했는지 나타내는 count 필드와 같이 반환
- count필드를 기준으로 내림차순 정렬

## 상품 추천 API
```python
@api_view(['GET',])
@permission_classes([IsAuthenticated])
def recommend_list(request) :
    user = request.user
    age = user.age
    assets = user.assets
    income = user.income
    if age is None or income is None or assets is None:
        return Response({'error': '나이, 연봉, 자산을 입력해 주세요.'}, status=status.HTTP_204_NO_CONTENT)
    all_users = User.objects.all().values('id', 'income', 'age', 'assets')
    df_users = pd.DataFrame(all_users)
    similar_users = df_users[
        (df_users['age'] >= age - 5) & (df_users['age'] <= age + 5) &
        (df_users["income"] >= income - 1000) & (df_users["income"] <= income + 1000) &
        (df_users['assets'] >= assets - 10000) & (df_users['assets'] <= assets + 10000)
    ]

    similar_users_ids = similar_users['id'].tolist()
    user_products_cd = UserProducts.objects.filter(user_id=user.id).values_list('fin_prdt_cd', flat=True)
    recommended_products = (UserProducts.objects.filter(user_id__in=similar_users_ids).exclude(fin_prdt_cd__in=user_products_cd))
    try :
        df_products = pd.DataFrame(list(recommended_products.values('fin_prdt_cd','fin_prdt_nm', 'product_type', 'kor_co_nm')))
        product_counts = df_products.groupby(['fin_prdt_cd','fin_prdt_nm', 'product_type', 'kor_co_nm']).size().reset_index(name='count')
    except KeyError as e:
        return Response({'error': "추천 상품이 없습니다"}, status=status.HTTP_204_NO_CONTENT)
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
```

![상품 CRU](img/usage.png)

- 금융상품통합비교공시 API를 활용해 데이터베이스에 저장한 예금, 적금 데이터들을 조회, 수정, 찜하기 기능
- 관리자만 금리 수정 가능
- 금리 수정 시 그 상품을 찜한 사용자에게 메일 발송

## 상품 CRU API
```python
@api_view(['GET',])
def deposit_list(request) :
    if request.method == 'GET':
        deposits = get_list_or_404(Deposit)
        paginator = DepositAndSavingsPagination()
        paginated_deposits = paginator.paginate_queryset(deposits, request)
        serializer = DepositListSerializer(paginated_deposits, many=True)
        return paginator.get_paginated_response(serializer.data)

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
@api_view(['PUT',])
@permission_classes([IsAdminUser])
def deposit_intr_rate_update(request, fin_prdt_cd, deposit_option_id) :
    deposit_option = get_object_or_404(DepositOptions, fin_prdt_cd=fin_prdt_cd, pk=deposit_option_id)
    serializer = DepositOptionsUpdateSerializer(deposit_option, data=request.data, partial=True)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        send_email(fin_prdt_cd, True)
        return Response(serializer.data, status=status.HTTP_200_OK)
```

![상품 검색](img/usage.png)

- 은행 이름과 저축기간을 기준으로 상품 검색

## 상품 검색
```python
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
```

![이메일 전송](img)

- 변경된 금리 정보를 담아 메일 발송
- 네이버 메일(SMTP)을 사용

## 금리 수정 시 이메일 전송을 위한 이메일 전송 함수
```python
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
```

![상품 찜하기 더미 데이터 생성](img)

- 상품 추천 기능을 확인하기 위해 더미 데이터가 필요함
- Faker 라이브러리를 사용하여 상품 찜하기 더미 데이터 생성
- 사용자 1명당 랜덤으로 5개의 상품 찜하기

## 상품 찜하기 더미 데이터 생성
```python
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
```

![위치 기반 은행 찾기 기능](img)

## 위치 기반 은행 찾기 기능

```js

```

![환율 계산기 기능](img)

- 한국수출입은행 환율정보 API를 활용하여 환율 정보를 받아오기
- 받아온 정보를 바탕으로 타국 통화와 원화 환율 계산

## 환율 계산기 기능

```python
@api_view(['GET',])
def get_exchange_rates(request):
    if request.method == 'GET':
        URL = 'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON'
        params = {
            "authkey" : API_KEY,
            "data" : "AP01"
        }
        response = requests.get(URL, params=params, verify=False).json()
        if response is None or len(response) == 0:
            today = datetime.today()
            for i in range(1, 31):  # 최대 30일 전까지 요청
                search_date = (today - timedelta(days=i)).strftime('%Y%m%d')
                params['searchdate'] = search_date
                response = requests.get(URL, params=params).json()

                if response is not None and len(response) > 0:
                    break

        return Response(response, status=status.HTTP_200_OK)
```

```js

```


# [4] AI Use

![챗봇](img/usage.png)

- OpenAI API를 활용하여 챗봇 기능을 구현하였습니다.
- openai 라이브러리를 사용하였습니다.
- 로그인한 사용자만 이용 가능하며, system 역할 즉, AI는 금융 전문가 역할을 하게 프롬프트를 작성하였습니다.
- 대화 대용을 저장하여 지속적으로 ai와 상호작용할 수 있게 구현하였습니다.
- 
## 챗봇 API
```python
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def chat(request) :
    user_message = request.data.get('message', '')
    client = OpenAI(api_key=openai_api_key)

    if not user_message:
        return Response({'error': '메세지를 입력해 주세요.'}, status=status.HTTP_400_BAD_REQUEST)

    try :
        conversation_history.append({"role" : "user", "content" : user_message})
        response = client.chat.completions.create(
            model = "gpt-4o-mini",
            messages = [
                {"role" : "system",
                 "content" : """You are a financial expert.
                 Answer the user's questions in Korean, providing clear and concise explanations.
                 Leverage your expertise in specific areas (such as investment, financial analysis, tax, etc.) to offer tailored advice based on the situation presented by the user.
                 Utilize the latest statistics and research findings to support your answers.
                 Enhance your explanations with real-life examples and case studies.
                 Adjust the depth of your responses according to the user's level of financial knowledge.
                 and keep your responses short and to the point."""},
                {"role": "user", "content" : user_message}
            ] + conversation_history,
        )
        bot_response = response.choices[0].message.content
        conversation_history.append({"role" : "assistant", "content" : bot_response})
        return Response({'conversation_history' : conversation_history,
                         'response': bot_response}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

```

# [5] Team
- [gahee](https://lab.ssafy.com/930_10) : 프론트엔드, 디자인, 어플리케이션 설계, ERD 작성
- [sungchan](https://lab.ssafy.com/myhamah) : 백엔드, 배포, 어플리케이션 설계, ERD 작성

# [6] Review

- 김성찬 : 
  - 팀원과 백, 프론트 부분을 철저하게 분리해서 깃 충돌 날 일이 거의 없었다. 그 때문에 한결 편하게 작업했다.
  - 혼자서 실습하고 관통 프로젝트를 할 때는 몰랐는데 백엔드 부분에서 데이터를 어떻게 반환할지 프론트엔드 부분과 많은 소통이 필요했다.
  - git과 ci/cd 파이프라인을 사용해서 push를 하면 자동으로 배포가 되게 해보고싶었지만 실패했다....
  - 팀원과 밤 늦게까지 코딩하면서 프로젝트를 완성해 가는 과정이 힘들기도 했지만 재미있는 부분이 더 컸다.
- 박가희 :
  - 2인의 소규모 프로젝트는 처음 해봤는데, 확실히 시간이 많이 들어 마감 기한을 맞추는게 어려웠습니다.
  - 프로젝트 중간에 kdt 해커톤에 참가해야 했어서, 일정 관리가 너무 어려웠습니다.
  - 그래서, 소통에 걸리는 시간을 줄이기 위해 팀원과 서로의 일정을 조율해가며 최대한 대면으로 만나서 개발에 힘썼습니다.
    디스코드나 전화 등으로 소통하는 것보다 직접 만나서 개발하니 정말 소통에 대한 시간이 줄었고, 훨씬 효율적으로 개발할 수 있었습니다.
  - 여러모로 배우는게 많은 프로젝트였습니다.

# [7] License
MIT 라이센스
라이센스에 대한 정보는 [`LICENSE`][license-url]에 있습니다.



<!--Url for Badges-->
[license-shield]: https://img.shields.io/github/license/dev-ujin/readme-template?labelColor=D8D8D8&color=04B4AE


<!--Url for Buttons-->
[readme-eng-shield]: https://img.shields.io/badge/-readme%20in%20english-2E2E2E?style=for-the-badge

<!--URLS-->
[license-url]: LICENSE.md
[contribution-url]: CONTRIBUTION.md
[readme-eng-url]: ../README.md


