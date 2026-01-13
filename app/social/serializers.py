from rest_framework import serializers
from social.models import SocialUser, Post, Comment

class SocialUserSerializer(serializers.ModelSerializer):
    # Це поле буде заповнене через annotate у ViewSet (оптимізація)
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
            "created_at"
        ]

class PostSerializer(serializers.ModelSerializer):
    # Nested Serializer: замість простого ID (1), ми покажемо об'єкт юзера.
    # read_only=True, бо ми тільки читаємо дані, а не створюємо пости через API.
    author = SocialUserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = [
            "id", 
            "external_id", 
            "title", 
            "body", 
            "author",  # Тепер тут буде повна інфа про автора
            "created_at"
        ]

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "external_id", "body", "author_email", "created_at"]