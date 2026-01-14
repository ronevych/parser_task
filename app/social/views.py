from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.pagination import PageNumberPagination

from social.models import Comment, Post, SocialUser
from social.serializers import CommentSerializer, PostSerializer, SocialUserSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class SocialUserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint для перегляду користувачів.
    """

    serializer_class = SocialUserSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = ["username", "email", "name"]
    ordering_fields = ["created_at", "username"]

    def get_queryset(self):
        return SocialUser.objects.annotate(posts_count=Count("posts")).order_by("-id")


class PostViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint для перегляду постів.
    """

    serializer_class = PostSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = ["author", "external_id"]
    search_fields = ["title", "body"]
    ordering_fields = ["created_at", "title"]

    def get_queryset(self):
        return Post.objects.select_related("author").all().order_by("-id")


class CommentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint для перегляду коментарів.
    Можна фільтрувати по post_id.
    """

    queryset = Comment.objects.select_related("post").all().order_by("-id")
    serializer_class = CommentSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]

    filterset_fields = ["post", "post__external_id"]
    ordering_fields = ["created_at"]
