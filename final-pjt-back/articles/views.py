from django.shortcuts import render, get_object_or_404, get_list_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Article, Comment
from .serializers import (ArticleCreateSerializer,
                          CommentSerializer,
                          ArticleListSerializer,
                          )
# Create your views here.
@api_view(['GET', 'POST',])
def create_or_list_articles(request):
    if request.method == 'GET':
        articles = Article.objects.all()
        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = ArticleCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT','DELETE',])
def article_detail(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
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
def create_comments(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    if request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, article=article)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['DELETE', 'PUT', 'POST'])
def comment_detail(request, article_id, comment_id):
    article = get_object_or_404(Article, pk=article_id)
    comment = get_object_or_404(Comment, pk=comment_id)
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







