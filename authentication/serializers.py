from djoser.serializers import UserSerializer, UserCreateSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from . import create_username, models
from djoser.conf import settings

User = get_user_model()


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


class UserDataSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['username', 'is_superuser', 'image']

    def get_image(self, obj):
        return models.Profile.objects.get(
            user=User.objects.get(email=obj.email)).image


class ProfileSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    banner = serializers.ImageField(required=False)
    user = serializers.SerializerMethodField()
    isFriend = serializers.SerializerMethodField()

    class Meta:
        model = models.Profile
        fields = ["user", "bio", "image", "banner", "tags",
                  "isLocked", "posts", "followers", "followings", "isVerified", "isFriend"]
        read_only_fields = ["posts", "followers",
                            "followings", "isVerified", "user", "isFriend"]

    def get_isFriend(self, obj):
        if self.context["request"] and self.context["request"].user.is_authenticated:
            if self.context["request"].user in obj.Connections.all():
                return True
            else:
                return False

    def get_user(self, obj):
        user = User.objects.get(email=obj.user.email)
        return UserSerializer(user).data
