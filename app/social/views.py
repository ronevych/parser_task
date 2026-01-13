from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count

from social.models import SocialUser, Post, Comment
from social.serializers import SocialUserSerializer, PostSerializer, CommentSerializer

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class SocialUserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint для перегляду користувачів.
    """
    serializer_class = SocialUserSerializer
    pagination_class = StandardResultsSetPagination
    # Підключаємо фільтри та пошук
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['username', 'email', 'name']
    ordering_fields = ['created_at', 'username']

    def get_queryset(self):
        # ОПТИМІЗАЦІЯ: annotate додає колонку posts_count прямо в SQL запит.
        # Це дозволяє серіалізатору не робити зайвих запитів.
        return SocialUser.objects.annotate(posts_count=Count('posts')).order_by('-id')

class PostViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint для перегляду постів.
    """
    serializer_class = PostSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    # Фільтрація по exact match (наприклад ?author=1)
    filterset_fields = ['author', 'external_id']
    # Пошук по тексту (ILIKE)
    search_fields = ['title', 'body']
    ordering_fields = ['created_at', 'title']

    def get_queryset(self):
        # ОПТИМІЗАЦІЯ: select_related('author') робить SQL JOIN.
        # Ми отримуємо дані поста та автора за ОДИН запит.
        return Post.objects.select_related('author').all().order_by('-id')
    
class CommentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint для перегляду коментарів.
    Можна фільтрувати по post_id.
    """
    queryset = Comment.objects.select_related('post').all().order_by('-id')
    serializer_class = CommentSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    
    # Фільтрація: /api/comments/?post=10
    filterset_fields = ['post', 'post__external_id'] 
    ordering_fields = ['created_at']