from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CommentCreateAPIView, CommentListAPIView,
                    PostCreateAPIView, PostListAPIView, PostRetrieveAPIView,
                    PostUpdateAPIView, PostViewSet, CommentsOnPostAPIView ,CommentOnCommentCreateAPIView, api)

router = DefaultRouter()
router.register(r'articles', PostViewSet)

urlpatterns = [
    path('posts/', PostListAPIView.as_view(), name='post-list'),
    path('comments/', CommentListAPIView.as_view(), name='comment-list'),
    path('posts/<int:pk>/', PostRetrieveAPIView.as_view(), name='post-detail'),
    path('posts/create/', PostCreateAPIView.as_view(), name='post-create'),
    path('comments/create/', CommentCreateAPIView.as_view(), name='comment-create'),
    path('posts/<int:pk>/update/', PostUpdateAPIView.as_view(), name='post-update'),
    path('posts/<int:pk>/comments/', CommentsOnPostAPIView.as_view(), name='comment-on-comment-create'),
    path('posts/<int:pk>/comments/create/', CommentOnCommentCreateAPIView.as_view(), name='comment-on-comment-create'),
]


urlpatterns += router.urls

urlpatterns += [
    path('ninja/', api.urls),
]