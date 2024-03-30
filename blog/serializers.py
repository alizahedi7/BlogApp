from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Comment, Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'post', 'text', 'email']

class PostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'content']

class CommentOnCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'parent_comment', 'text', 'email']

    def validate_parent_comment(self, value):
        post_id = self.context['view'].kwargs.get('pk')
        if value.post_id != post_id:
            raise ValidationError("The parent comment does not belong to the specified post")
        return value