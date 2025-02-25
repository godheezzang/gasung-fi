from rest_framework import serializers
from .models import Article, Comment

class ArticleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ("id",'title', 'content', 'image',)
        read_only_fields = ('user',)
class ArticleCommentsSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ("id",'username', 'content', 'email', 'replies', )

    def get_replies(self, obj):
        replies = Comment.objects.filter(main_comment=obj)
        return ArticleCommentsSerializer(replies, many=True).data

    def get_username(self, obj):
        return obj.user.username

    def get_email(self, obj):
        return obj.user.email


class ArticleListSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    class Meta:
        model = Article
        fields = '__all__'
    def get_username(self, obj):
        return obj.user.username

    def get_comments(self, obj):
        comments = Comment.objects.filter(article = obj, main_comment__isnull=True)
        return ArticleCommentsSerializer(comments, many=True).data

    def get_comment_count(self, obj):
        return Comment.objects.filter(article = obj).count()

    def get_email(self, obj):
        return obj.user.email


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("id",'content',)
        read_only_fields = ('user', 'article', 'main_comment',)
