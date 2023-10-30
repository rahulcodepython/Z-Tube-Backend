from djoser.serializers import UserSerializer, UserCreateSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from djoser.conf import settings
from . import create_username, models

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


class ProfileSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    banner = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Profile
        fields = ["user", "bio", "image", "banner", "tags", "isLocked"]

    def get_image(self, obj):
        return obj.image.url

    def get_banner(self, obj):
        return obj.banner.url

    def get_user(self, obj):
        user = User.objects.get(email=obj.user.email)
        return UserSerializer(user).data

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
