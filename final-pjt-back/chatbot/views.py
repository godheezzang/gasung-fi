from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from gasung_fi import my_settings
from openai import OpenAI
# Create your views here.

openai_api_key = my_settings.OPENAI_API_KEY
conversation_history = []
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def chat(request) :
    user_message = request.data.get('message', '')
    client = OpenAI(api_key=openai_api_key)

    if not user_message:
        return Response({'error': '메세지를 입력해 주세요.'}, status=status.HTTP_400_BAD_REQUEST)

    if not is_financial_question(user_message):
        return Response({'response': """안녕하세요! 저는 금융과 경제와 관련된 질문을 도와드리기 위해 여기 있어요.\n 혹시 그와 관련된 궁금한 점이나 도움이 필요하신 부분이 있다면 정말 기쁘게 답변해드릴게요.\n 😊\n만약 다른 주제에 대해 질문하고 싶으신 거라면, 그 부분은 제가 잘 알지 못할 수도 있어서요.\n 금융이나 경제에 관한 이야기라면 더욱 성심껏 도와드릴 수 있으니, 편하게 질문해 주세요!\n 언제든 열심히 도와드리겠습니다. 감사합니다!"""}, status=status.HTTP_200_OK)

    try :
        conversation_history.append({"role" : "user", "content" : user_message})
        response = client.chat.completions.create(
            model = "gpt-4o-mini",
            messages = [
                {"role" : "system",
                 "content" : """You are a financial expert. 
                You should answer the user's questions in Korean,
                 providing clear and concise explanations. 
                 Use professional terminology whenever possible, 
                 but explain it in an easy-to-understand manner. 
                 If necessary, 
                 provide examples and support your answers with statistics or evidence , 
                 Please add a line break at the end of each sentence, using the tag \n., 
                 Shortly"""},
                {"role": "user", "content" : user_message}
            ] + conversation_history,
        )
        bot_response = response.choices[0].message.content
        conversation_history.append({"role" : "assistant", "content" : bot_response})
        return Response({'conversation_history' : conversation_history,
                         'response': bot_response}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def is_financial_question(message):
    financial_keywords = ['주식', '경제', '금리', '투자', '재무', '채권', '환율', '자산', '부동산', '인플레이션', '물가',
                          '디플레이션', '세금', '신용', '보험', '기업', '암호화폐', '리스크', 'GDP', 'CPI', 'PPI', '실업률',
                          '거래', '국채', '회사채', '지표', '정책', '대출', '외환', '펀드', 'ETF', '옵션', '선물',
                          '증권', '비트코인', '금융']

    return any(keyword in message for keyword in financial_keywords)
