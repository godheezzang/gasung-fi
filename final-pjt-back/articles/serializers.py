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
        fields = ('id', 'user', 'content', )


class ArticleListSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Article
        fields = '__all__'

    def get_comments(self, obj):
        comments = obj.objects.filter(main_comment__isnull=True)
        return ArticleCommentsSerializer(comments, many=True).data


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('content',)
        read_only_fields = ('user', 'article', 'main_comment',)
