from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.conf import settings

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "image",
            "banner",
            "tags",
            "posts",
            "followers",
            "followings",
            "isVerified",
            "isLocked",
            "is_superuser",
        ]


class UserPeekSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "image", "is_superuser"]


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = list(User.REQUIRED_FIELDS) + [
            settings.AUTH_CONFIG["LOGIN_FIELD"],
            "password",
        ]

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "bio",
            "image",
            "banner",
            "tags",
            "isLocked",
        ]

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
