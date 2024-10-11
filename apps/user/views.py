from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.user.models import User
from apps.user.serializers import (
    UserSerializer, 
    CustomTokenObtainPairSerializer, 
    FollowersSerilaizer
    )

from utils.general_utils.soft_delete import delete_instance

from django.contrib.auth.models import AnonymousUser
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CustomTokenObtainView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):

        if self.action in [
            "list_users",
            "view_user_profile",
            "edit_user_profile",
        ]:
            return UserSerializer
        # return super().get_serializer_class()


    @action(detail=False, methods=["get"], url_path="list-users")
    def list_users(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, 200)
    
    @action(detail=True, methods=["get"], url_path="view-user-profile")
    def view_user_profile(self, request, pk=None):
        user = self.get_object()
        serializer = self.get_serializer(user)
        return Response(serializer.data, 200)

    @action(detail=False, methods=["put"], url_path="edit-user-profile")
    def edit_user_profile(self, request):
        if isinstance(request.user, AnonymousUser):
            return Response({"Login to update profile"}, 401)
        user = request.user
        serializer = self.get_serializer(
            instance=user, data=request.data, partial=True
            )
        if serializer.is_valid():
            serializer.save()
            return Response({"user updated successfully"})
        return Response(serializer.errors, 400)
    
    @action(detail=True, methods=["delete"], url_path="delete-user")
    def delete_user(self, request, pk=None):
        try:
            instance = self.get_object()
            return delete_instance(instance)
        except Exception as e:
            return Response(f"{e}")

    @action(detail=False, methods=["put"], url_path="activate-or-deactivate-account")
    def activate_or_deactivate_account(self, request):
        instance = self.get_object()
        action = request.data.get("action")

        if action and instance.status != "ACTIVE":
            instance.status = "ACTIVE"
            instance.save()
            return Response({"User reactivated successfully"}, 200)

        instance.status = "INACTIVE"
        instance.save()
        return Response({"User deactivated successfully"}, 200)
    
    @action(detail=False, methods=["get"], url_path="get-followers-and-following-stat")
    def get_followers_and_following_stat(self, request):
        user_id = request.GET.get("user_id", None)
        try:
            user = User.objects.get(id=user_id)
            data = {
                "user": user
            }

            serializer = FollowersSerilaizer(data, context=user_id)

            return Response(serializer.data, 200)
        except User.DoesNotExist:
            return Response({"User does not exist"}, 404)

    @action(detail=False, methods=["post"], url_path="follow-user")
    def follow_user(self, request):
        try:
            follower = request.user
            following_id = request.data.get("following_id", None)
            following = User.objects.get(id=following_id)
            action = request.data.get("action", None)

            if action:
                follower.following.add(following)
                following.followers.add(follower)

                follower.save()
                following.save()
                return Response({"User followed successfully"}, 200)
            
            if not action:
                follower.following.remove(following)
                following.followers.remove(follower)

                follower.save()
                following.save()

            return Response({"User unfollowed successfully"}, 200)
        
        except Exception as e:
            return Response({f"{e}"})


@csrf_exempt
def sign_in(request):
    return render(request, 'templates/sign_in.html')