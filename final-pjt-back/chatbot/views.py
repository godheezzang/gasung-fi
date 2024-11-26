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
