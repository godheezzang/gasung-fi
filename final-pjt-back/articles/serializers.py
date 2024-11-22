from rest_framework import serializers
from .models import Article, Comment

class ArticleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('title', 'content',)
        read_only_fields = ('user',)
class ArticleCommentsSerializer(serializers.ModelSerializer):
    comment_id = serializers.IntegerField(source="id", read_only=True)
    user = serializers.StringRelatedField(read_only=True)
    replies = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = ('user', 'content', "comment_id", 'replies',)

    def get_replies(self, obj):
        replies = Comment.objects.filter(main_comment=obj)
        return ArticleCommentsSerializer(replies, many=True).data


class ArticleListSerializer(serializers.ModelSerializer):
    article_id = serializers.IntegerField(source="id", read_only=True)
    comments = serializers.SerializerMethodField()
    user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Article
        exclude = ("id",)

    def get_comments(self, obj):
        comments = Comment.objects.filter(article = obj, main_comment__isnull=True)
        return ArticleCommentsSerializer(comments, many=True).data


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("id",'content',)
        read_only_fields = ('user', 'article', 'main_comment',)
