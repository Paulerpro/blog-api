from django.db import models
from classes.base_model import BaseModel

from apps.blogpost.managers import PostManager


class BlogPost(BaseModel):
    title = models.CharField(max_length=60)
    body = models.TextField()
    user = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True, blank=True)
    likes = models.ManyToManyField('user.User', blank=True, related_name="post_likes")

    objects = PostManager()

#     # Tags/Categories: Keywords or classifications to organize and group posts.
#     # Status: The current state of the post (e.g., draft, published, archived).
#     # Slug: A URL-friendly version of the title, used for web addresses.
#     # Summary/Excerpt: A brief overview or snippet of the post content.

class Comment(BaseModel):
    blog_post = models.ForeignKey('BlogPost', on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    text = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True) # research and undertsand more bout field
    
# can be liked/unliked
#     # Status: The current state of the comment (e.g., approved, pending, spam).


# class Like(BaseModel):
#     user = models.ForeignKey('user.User', on_delete=models.CASCADE)
#     blog_post = models.ForeignKey('BlogPost', on_delete=models.CASCADE)

#     # Unique Constraint: Ensures that a user can only like a particular blog post once to avoid duplicate likes.
#     # implement system to like comments
