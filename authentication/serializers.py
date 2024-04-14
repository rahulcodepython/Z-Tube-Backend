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


class GoogleAuthSerializer(serializers.Serializer):
    code = serializers.CharField(required=False)
    error = serializers.CharField(required=False)


class UserCreateSerializer(UserCreateSerializer):
    def create(self, validated_data):
        user = super().create(validated_data)
        user.username = create_username.create_username(validated_data['email'].split(
            '@')[0])
        user.save()
        models.Profile.objects.create(user=user)
        models.ProfileConfig.objects.create(user=user)
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
    image = serializers.URLField()
    banner = serializers.URLField()

    class Meta:
        model = models.Profile
        fields = ["bio", "image", "banner", "tags",
                  "posts", "followers", "followings", "isLocked", "isVerified"]
        read_only_fields = ["posts", "followers", "followings", "isVerified"]
