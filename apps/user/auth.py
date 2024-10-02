# from django.contrib.auth.backends import ModelBackend
# # from django.contrib.auth.models import User
# from apps.user.models import User

# class EmailBackend(ModelBackend):
#     def authenticate(self, request, email=None, password=None, **kwargs):
#         if email is None:
#             email = kwargs.get("email")
#         try:
#             user = User.objects.get(email=email)
#         except User.DoesNotExist:
#             return None
#         else:
#             if user.check_password(password) and self.user_can_authenticate(user):
#                 return user
#         return None