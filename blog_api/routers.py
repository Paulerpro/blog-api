from rest_framework import routers

from apps.blogpost.views import BlogPostViewset, CommentViewset
from apps.user.views import UserViewset

router = routers.DefaultRouter()

router.register(r"blogpost", BlogPostViewset, basename="blogpost")
router.register(r"user", UserViewset, basename="user")
router.register(r"comment", CommentViewset, basename="comment")