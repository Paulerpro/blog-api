from apps.user.models import User
from utils.user_utils.user import UserUtils

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django.db.models import Q

class UserSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(required=False, allow_blank=True)
    username = serializers.CharField(required=False, allow_blank=True)
    location = serializers.CharField(required=False, allow_blank=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "location",
            'password',
            "followers",
            "following",
            "bio",
            "meta",
            "username",
        )
        read_only = ['created_at', 'updated_at']

    def validate_email(self, email):
        if not email:
            raise serializers.ValidationError("Email must not be empty")
        if User.objects.does_user_exist({"email__iexact": email}):
            raise serializers.ValidationError("Email already exists")
        return email

    def validate_phone_number(self, phone_number):
        if phone_number and not phone_number.isdigit():
            raise serializers.ValidationError("phone number should only be digits")
        if phone_number and User.objects.does_user_exist({"meta__phone_number": phone_number}):
            raise serializers.ValidationError("Phone number already exists")
        return phone_number

    def create(self, validated_data):
        meta = {}
        phone_number = self.validate_phone_number(validated_data.get("phone_number", None))
        email = self.validate_email(validated_data.get("email", None))
        username = email if not validated_data.get("username", None) else validated_data["username"]

        if phone_number:
            meta["phone_number"] = phone_number

        user = User.objects.create_user(
            email=email,
            password=validated_data["password"],
            username=username,
            meta=meta,
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"]
        )

        user.save()
        return user
    
    def update(self, instance, validated_data):
        phone_number = self.validate_phone_number(validated_data.get("phone_number", None))
        location = validated_data.get("location", None)

        if phone_number:
            instance.meta["phone_number"] = phone_number

        if location:
            instance.meta["location"] = location

        # updates all fields provided
        instance = super().update(instance, validated_data)

        instance.save()

        return instance


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField(required=False)
    phone_number = serializers.CharField(required=False)
    
    def validate(self, attrs):
        email = attrs.get("email", None)
        phone_number = attrs.get("phone_number", None)
        password = attrs.get("password", None)

        if not email and not phone_number:
            raise serializers.ValidationError("Either email or phone number must be provided")

        credentials = email or phone_number

        try:
            user = User.objects.get(
                Q(meta__phone_number=credentials) | Q(email=credentials)
            )
            print(user)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid login credentials")
        
        if not user.check_password(password):
            raise serializers.ValidationError("Invalid login credentials")
        
        # if user.status == DisABLED:
        #     pass

        refresh = self.get_token(user)

        token = {
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }

        data = UserUtils.get_user_login_data(user, token)

        return data


    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token["email"] = user.email
        return token
    

class FollowersSerilaizer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField(required=False)
    following_count = serializers.SerializerMethodField(required=False)

    class Meta:
        model = User
        fields = ["followers", "following", "followers_count", "following_count"]

    def to_representation(self, instance):
        instance = instance.get("user", None)
        followers_details = instance.followers.values_list("first_name", "last_name", "bio")
        following_details = instance.following.values_list("first_name", "last_name", "bio")

        representation = {
            "followers_count": instance.followers.count(),
            "following_count": instance.following.count(),
            "followers": followers_details,
            "following": following_details,
        }

        return representation


