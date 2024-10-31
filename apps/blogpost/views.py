from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from utils.general_utils.api_response_util import APIResponseUtil

from apps.blogpost.models import BlogPost, Comment
from apps.blogpost.serializers import BlogPostSerilaizer, CommentSerializer, PostLikersSerilaizer

from utils.general_utils.soft_delete import delete_instance

from django.contrib.auth.models import AnonymousUser
from django.shortcuts import get_object_or_404

from drf_spectacular.utils import extend_schema

class BlogPostViewset(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()

    @extend_schema()
    def get_serializer_class(self, *args, **kwargs):
        if self.action in ["get_post_likers"]:
            return PostLikersSerilaizer
        return BlogPostSerilaizer

    @extend_schema()
    @action(detail=True, methods=["get"], url_path="view-blogpost")
    def view_blogpost(self, request, pk=None): 
        obj = self.get_object()
        serializer = self.get_serializer(obj, many=False)
        return APIResponseUtil.success_response(200, "", serializer.data)
        
    @action(detail=False, methods=["post"], url_path="create-blogpost")
    def create_blogpost(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(): 
            serializer.save(user=request.user)
            return APIResponseUtil.success_response(201, "Blogpost created successfully", {})
        return Response(serializer.errors, 400)

    @action(detail=True, methods=["put"], url_path="edit-blogpost")
    def edit_blogpost(self, request, pk=None):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(
                instance, data=request.data, partial=True
                )
            if serializer.is_valid():
                serializer.save()
                return APIResponseUtil.success_response(204, "Blogpost updated successfully")
            return Response(serializer.errors, 400)
        except:
            return Response({"Blogpost not found"}, 401)
    
    @action(detail=True, methods=["delete"], url_path="delete-blogpost")
    def delete_blogpost(self, request, pk=None):
        try:
            instance = self.get_object()
            return delete_instance(instance)
        except:
            return Response({"Blogpost not found/already deleted"}, 404)

    @action(detail=False, methods=["get"], url_path="get-blogposts-by-user")
    def get_blogposts_by_user(self, request) -> list:
        try:
            queryset = self.get_queryset().filter(user=request.user)
            serializer = self.get_serializer(queryset, many=True)
            return APIResponseUtil.success_response(200, "", serializer.data)
        except Exception as e:
            return Response(f'{e}', 404)
        
    @action(detail=False, methods=["put"], url_path="like-or-unlike-post")
    def like_post_or_unlike_post(self, request):
        action = request.GET.get("action", None)
        user = request.user
        post_id = request.GET.get("post_id", None)
        post = get_object_or_404(BlogPost, pk=post_id)
        if action == "1":
            post.likes.add(user)
            return APIResponseUtil.success_response(204, "Post liked succesfully", {})
        post.likes.remove(user)
        return APIResponseUtil.success_response(204, "Post unliked succesfully", {})
    
    @action(detail=True, methods=["get"], url_path="get-post-likers")
    def get_post_likers(self, request, pk=None):
        post = get_object_or_404(BlogPost, pk=pk)
        serializer = self.get_serializer(post)
        return APIResponseUtil.success_response(200, "", serializer.data)

class CommentViewset(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    @action(detail=False, methods=["post"], url_path="create-comment")
    def create_comment(self, request):
        serializer = self.serializer_class(data=request.data)
        parent_id = request.data.get("parent", None)
        
        if serializer.is_valid():
            parent_comment = self.get_queryset().filter(id=parent_id)[0] if parent_id else None
            serializer.save(user=request.user, parent=parent_comment)
            return APIResponseUtil.success_response(201, "comment created")
        return Response(serializer.errors)
    
    @action(detail=False, methods=["get"], url_path="get-user-comments")
    def get_user_comments(self, request):
        if isinstance(request.user, AnonymousUser):
            return Response({"Log in for this action"})
        comments = self.get_queryset().filter(user=request.user)
        serializer = self.get_serializer(comments, many=True)
        return APIResponseUtil.success_response(200, "", serializer.data)

    # get comments by blogpost
    @action(detail=True, methods=["get"], url_path="get-blogpost-comments")
    def get_blogpost_comment(self, request, pk=None):
        try:
            blogpost = BlogPost.objects.get(id=pk)
            parent_id = request.GET.get("parent_id", None)
            if parent_id:
                parent_comments = self.get_queryset().filter(
                    id=parent_id
                    )
                comments = self.get_queryset().filter(
                    blog_post=blogpost, 
                    parent__in=parent_comments
                    )
            else:
                comments = self.get_queryset().filter(
                    blog_post=blogpost, 
                    parent=None
                    )

            serializer = self.get_serializer(comments, many=True)
            return APIResponseUtil.success_response(200, "", serializer.data)
        except Exception as e:
            return Response(f"{e}", 400)

    # edit comment 
    def partial_update(self, request, pk=None):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(
                instance, 
                data=request.data, 
                partial=True
                )
            if serializer.is_valid():
                serializer.save()
                return APIResponseUtil.success_response(204, "comment updated successfully", {})
            return Response(serializer.errors, 400)
        except:
            return Response({"comment not found"}, 404)
    
    # delete user comment by id
    def destroy(self, request, pk=None):
        try:
            instance = self.get_object()
            return delete_instance(instance)
        except:
            return Response({"Comment's not found/already deleted"}, 404)