from rest_framework import serializers

from social.models import Comment, Post, SocialUser


class SocialUserSerializer(serializers.ModelSerializer):
    posts_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = SocialUser
        fields = [
            "id",
            "external_id",
            "username",
            "email",
            "name",
            "posts_count",
            "created_at",
        ]


class PostSerializer(serializers.ModelSerializer):
    author = SocialUserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "external_id",
            "title",
            "body",
            "author",
            "created_at",
        ]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "external_id", "body", "author_email", "created_at"]
