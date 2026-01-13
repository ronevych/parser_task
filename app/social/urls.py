from django.urls import path, include
from rest_framework.routers import DefaultRouter
from social.views import SocialUserViewSet, PostViewSet, CommentViewSet

# Router автоматично створює URL-и: /users/, /users/{id}/, /posts/...
router = DefaultRouter()
router.register(r'users', SocialUserViewSet, basename='user')
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
]