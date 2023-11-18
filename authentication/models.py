import json
from django.db import models
from . import manager as self_manager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, max_length=254)
    first_name = models.CharField(max_length=1000, blank=True)
    last_name = models.CharField(max_length=1000, blank=True)
    username = models.CharField(max_length=1000, blank=True)
    # password .....

    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    groups = None
    user_permissions = None
    last_login = None

    objects = self_manager.UserManager()

    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']

    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['email']

    def __str__(self) -> str:
        return self.email


def upload_to_user(instance, filename):
    return 'userImage/{filename}'.format(filename=filename)


def upload_to_banner(instance, filename):
    return 'bannerImage/{filename}'.format(filename=filename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(default='', blank=True)
    image = models.ImageField(upload_to=upload_to_user,
                              default='userImage/defaultUser.png')
    banner = models.ImageField(
        upload_to=upload_to_banner, default='bannerImage/defaultBanner.png')
    isVerified = models.BooleanField(default=False)
    tags = models.CharField(max_length=100, blank=True)
    posts = models.IntegerField(default=0)
    followers = models.IntegerField(default=0)
    followings = models.IntegerField(default=0)
    isLocked = models.BooleanField(default=False)
    Connections = models.ManyToManyField(
        User, related_name='Connections', blank=True)

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def __str__(self) -> str:
        return self.user.email
