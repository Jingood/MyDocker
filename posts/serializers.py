from rest_framework import serializers
from .models import Post, Comment
from django.contrib.auth import get_user_model

User = get_user_model()

class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ["id", "author", "title", "content", "created_at", "updated_at", "likes_count"]
    
    def get_likes_count(self, obj):
        return obj.likes.count()

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")
    likes_count = serializers.SerializerMethodField()
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ["id", "author", "post", "content", "created_at", "updated_at", "likes_count", "replies"]
        read_only_fields = ["post"]
    
    def get_likes_count(self, obj):
        return obj.likes.count()
    
    def get_replies(self, obj):
        if obj.replies.exists():
            return CommentSerializer(obj.replies.all(), many=True).data
        return []