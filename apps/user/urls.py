from django.urls import path
from apps.user.views import (
    CustomTokenObtainView, 
    TokenRefreshView, 
    RegisterUserView,
    sign_out,
    auth_receiver,
    sign_in,
)

urlpatterns = [
    path('login/', CustomTokenObtainView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register-user/', RegisterUserView.as_view(), name='register-user'),

    # Oauth google
    path('sign-in/', sign_in, name='sign_in'),
    # path('sign-out', sign_out, name='sign_out'),
    path('auth-receiver/', auth_receiver, name='auth_receiver'),

]
