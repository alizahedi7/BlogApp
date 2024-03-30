from typing import List

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from ninja import NinjaAPI, Schema
from rest_framework import generics, permissions, viewsets

from .models import Comment, Post
from .serializers import (CommentSerializer, PostSerializer,
                          PostUpdateSerializer, CommentOnCommentSerializer)
from django.core.exceptions import ValidationError

# APIs Developed with Django Rest Framework
class PostListAPIView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

class CommentListAPIView(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

class PostRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

class PostCreateAPIView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

class CommentCreateAPIView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

class CommentsOnPostAPIView(generics.ListAPIView):
    serializer_class = CommentOnCommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        post_id = self.kwargs['pk']
        return Comment.objects.filter(post_id=post_id)
    
class CommentOnCommentCreateAPIView(generics.CreateAPIView):
    serializer_class = CommentOnCommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        post_id = self.kwargs.get('pk')
        serializer.save(post_id=post_id)
    

class PostUpdateAPIView(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]


# APIs Developed with Django Ninja
api = NinjaAPI()

class PostOutSchema(Schema):
    id : int
    title: str
    content: str

class PostInSchema(Schema):
    title: str = None
    content: str = None

class CommentSchema(Schema):
    post_id: int
    text: str
    email: str

class CommentOnCommentSchema(Schema):
    parent_comment_id: int
    text: str
    email: str

@api.get('/posts', response=List[PostOutSchema], tags=['posts'], description="List all posts")
@login_required()
def list_posts(request):
    queryset = Post.objects.all()
    return queryset

@api.get("/comments", response=List[CommentSchema], tags=['comments'], description="List all comments")
@login_required
def list_comments(request):
    queryset = Comment.objects.all()
    return queryset

@api.post("/posts", tags=['posts'])
@login_required
def create_post(request, payload: PostInSchema):
    """
    To create a post please provide:
    - **title** 
    - **content**
    """
    post = Post.objects.create(**payload.dict())
    return {"id": post.id}

@api.post("/comments", tags=['comments'])
@login_required
def create_comment(request, payload: CommentSchema):
    """
    To create a comment please provide:
    - **post_id**
    - **text**
    - **email**
    """
    comment = Comment.objects.create(**payload.dict())
    return {"id": comment.id}

@api.put("/posts/{int:post_id}", tags=['posts'])
@login_required
def update_post(request, post_id: int, payload: PostInSchema):
    """
    To update a post please provide:
    - **post_id**
    - **title**
    - **content**
    """
    post = get_object_or_404(Post, id=post_id)
    for attr, value in payload.dict().items():
        if value is not None:  
            setattr(post, attr, value)
    post.save()
    return {"success": True}

@api.get("/posts/{int:post_id}", response=PostOutSchema, tags=['posts'], description="Get a post")
@login_required
def get_post(request, post_id: int):
    post = get_object_or_404(Post, id=post_id)
    return post

@api.delete("/posts/{int:post_id}", tags=['posts'], description="Delete a post")
@login_required
def delete_post(request, post_id: int):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    return {"success": True}

@api.get("/posts/{int:post_id}/comments", response=List[CommentSchema] ,tags=['comments'], description="Get all comments on a post")
@login_required
def comments_on_post(request, post_id: int):
    comments = Comment.objects.filter(post_id=post_id)
    return comments

@api.post("/posts/{int:post_id}/comments/create", tags=['comments'])
@login_required
def create_comment_on_comment(request, post_id: int, payload: CommentOnCommentSchema):
    """
    To create a comment on comment please provide:
    - **parent_comment_id**
    - **text**
    - **email**
    """
    comment = Comment.objects.create(post_id=post_id, **payload.dict())
    return {"id": comment.id}