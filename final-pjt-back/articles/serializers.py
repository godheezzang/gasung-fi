from rest_framework import serializers
from .models import Article, Comment

class ArticleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('title', 'content',)
        read_only_fields = ('user',)
class ArticleCommentsSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Comment
        fields = ('id', 'user', 'content', 'main_comment', )


class ArticleListSerializer(serializers.ModelSerializer):
    comments = ArticleCommentsSerializer(source="comment_set", many=True)
    user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Article
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('content',)
        read_only_fields = ('user', 'article', 'main_comment',)
