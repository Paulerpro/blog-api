from rest_framework import serializers

from apps.blogpost.models import BlogPost, Comment
from apps.user.models import User

class BlogPostSerilaizer(serializers.ModelSerializer):

    class Meta:
        model = BlogPost
        # fields = "__all__"
        exclude = ['likes']
        read_only_fields = [
            "user",
            "created_at",
            "updated_at",
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        comm_count = instance.comments.count()
        likes_count = instance.likes.count()
        representation["comments_count"] = comm_count
        representation["likes_count"] = likes_count
        return representation
    

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = [
            "blogpost",
            "user",
            "created_at",
            "updated_at",
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        nested_comments_count = Comment.objects.filter(parent=instance).count() or 0
        representation["nested_comm_count"] = nested_comments_count

        return representation


class PostLikersSerilaizer(serializers.Serializer):
    
    def to_representation(self, instance):
        
        likers = instance.likes.values_list("id", "first_name", "bio")
        representation = {
            "likers": likers,
        }

        return representation

