from django.urls import path
from apps.user.views import (
    CustomTokenObtainView, 
    TokenRefreshView, 
    RegisterUserView,
    sign_in,
)

urlpatterns = [
    path('login/', CustomTokenObtainView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register-user/', RegisterUserView.as_view(), name='register-user'),

    # Oauth google test
    path('sign-in/', sign_in, name='sign_in'),
]
