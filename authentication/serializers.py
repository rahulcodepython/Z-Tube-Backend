from djoser.serializers import UserSerializer, UserCreateSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from . import create_username, models
from djoser.conf import settings
from dotenv import load_dotenv
import os

User = get_user_model()
load_dotenv()

BACKEND_DOMAIN_ENV = os.environ.get('BACKEND_DOMAIN')


class UserSerializer(UserSerializer):
    is_superuser = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + \
            (settings.LOGIN_FIELD, "is_superuser")


class UserCreateSerializer(UserCreateSerializer):
    def create(self, validated_data):
        user = super().create(validated_data)
        user.username = create_username.create_username(validated_data['email'].split(
            '@')[0])
        user.save()
        models.Profile.objects.create(user=user)
        return user


class ProfileSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    banner = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField(read_only=True)
    isFriend = serializers.SerializerMethodField()

    class Meta:
        model = models.Profile
        fields = ["user", "bio", "image", "banner", "tags",
                  "isLocked", "posts", "followers", "followings", "isVerified", "isFriend"]
        read_only_fields = ["posts", "followers", "followings", "isVerified"]

    def get_isFriend(self, obj):
        if self.context["request"] and self.context["request"].user.is_authenticated:
            if self.context["request"].user in obj.Connections.all():
                return True
            else:
                return False

    def get_image(self, obj):
        if obj.image:
            image_url = f"{BACKEND_DOMAIN_ENV}{obj.image.url}"
            return image_url

    def get_banner(self, obj):
        if obj.banner:
            image_url = f"{BACKEND_DOMAIN_ENV}{obj.banner.url}"
            return image_url

    def get_user(self, obj):
        user = User.objects.get(email=obj.user.email)
        return UserSerializer(user).data

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
