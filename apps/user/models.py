from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from classes.base_model import BaseModel
from apps.user.managers import UserManager


READER_TYPES = (
    ('MEMBER', 'Member'),
    ('PREMIUM', 'Premium')
)

class User(BaseModel, AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField(max_length=350, null=True, blank=True)
    subscription_type = models.CharField(choices=READER_TYPES, null=True, blank=True) # looks better in a Reader Model
    following = models.ManyToManyField('user.User', blank=True, related_name="user_following")
    followers = models.ManyToManyField('user.User', blank=True, related_name="user_followers")
    date_of_birth = models.DateField(blank=True, null=True)
    groups = models.ManyToManyField(Group, related_name="custom_user_set")
    user_permissions = models.ManyToManyField(Permission, related_name="custom_user_set")
    # follwers_count = models.PositiveIntegerField(default=0) # is creating a field for this performance okay? or doing the count upon request?
    #     Website/Blog URL: The URL to the blogger's personal or professional website.
    # Social Media Links: Links to the blogger's social media profiles.
    # otp = models.CharField(max_length=6, null=True, blank=True)
    # otp_created_at = models.DateTimeField(auto_now_add=True)
    # email_verified = models.BooleanField(default=False)
    # phone_number_verified = models.BooleanField(default=False)
    # profile_pic(base64 or static filed locally),

    objects = UserManager() # if  else NonActiveObjectsManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self) -> str:
        return self.email
    