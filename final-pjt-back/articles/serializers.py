from rest_framework import serializers
from .models import Article, Comment

class ArticleCreateSerializer(serializers.ModelSerializer):
    article_id = serializers.IntegerField(source="id", read_only=True)
    class Meta:
        model = Article
        fields = ("article_id",'title', 'content',)
        read_only_fields = ('user',)
class ArticleCommentsSerializer(serializers.ModelSerializer):
    comment_id = serializers.IntegerField(source="id", read_only=True)
    user = serializers.SerializerMethodField()
    replies = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = ('user', 'content', "comment_id", 'replies',)

    def get_replies(self, obj):
        replies = Comment.objects.filter(main_comment=obj)
        return ArticleCommentsSerializer(replies, many=True).data

    def get_user(self, obj):
        return obj.user.username


class ArticleListSerializer(serializers.ModelSerializer):
    article_id = serializers.IntegerField(source="id", read_only=True)
    comments = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    class Meta:
        model = Article
        exclude = ("id",)
    def get_user(self, obj):
        return obj.user.username

    def get_comments(self, obj):
        comments = Comment.objects.filter(article = obj, main_comment__isnull=True)
        return ArticleCommentsSerializer(comments, many=True).data

    def get_comment_count(self, obj):
        return Comment.objects.filter(article = obj).count()


class CommentSerializer(serializers.ModelSerializer):
    comment_id = serializers.IntegerField(source="id", read_only=True)
    class Meta:
        model = Comment
        fields = ("comment_id",'content',)
        read_only_fields = ('user', 'article', 'main_comment',)
