from django.shortcuts import render, get_object_or_404
from faker import Faker
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .models import Article, Comment
from .serializers import (ArticleCreateSerializer,
                          CommentSerializer,
                          ArticleListSerializer)
# Create your views here.
fake = Faker()
User = get_user_model()
class ArticlesPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
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









