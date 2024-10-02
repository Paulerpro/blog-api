from django.contrib import admin
from apps.user.models import User


admin.site.register(User)
# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# # from .models import User

# class CustomUserAdmin(UserAdmin):
#     model = User
#     # Adjust fieldsets as needed
#     fieldsets = UserAdmin.fieldsets + (
#         (None, {'fields': ('bio', 'subscription_type', 'following')}),
#     )
#     add_fieldsets = UserAdmin.add_fieldsets + (
#         (None, {'fields': ('bio', 'subscription_type', 'following')}),
#     )
#     list_display = ['email', 'is_staff', 'is_superuser']
#     search_fields = ['email']
#     ordering = ['email']

# admin.site.register(User, CustomUserAdmin)



