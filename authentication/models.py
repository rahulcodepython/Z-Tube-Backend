from django.db import models
from . import manager as self_manager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.postgres.fields import ArrayField


class User(AbstractBaseUser, PermissionsMixin):
    id = models.BigAutoField(auto_created=True, primary_key=True,
                             serialize=False, verbose_name='ID', db_index=True)
    email = models.EmailField(
        unique=True, max_length=254)
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


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    bio = models.TextField(default='', blank=True)
    image = models.URLField(default='', blank=True, max_length=10000)
    banner = models.URLField(default='', blank=True, max_length=10000)
    tags = ArrayField(models.CharField(
        max_length=100, blank=True), size=5, blank=True, default=list)
    posts = models.IntegerField(default=0)
    followers = models.IntegerField(default=0)
    followings = models.IntegerField(default=0)
    Connections = models.ManyToManyField(
        User, related_name='Connections', blank=True)

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def __str__(self) -> str:
        return self.user.email


class ProfileConfig(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    isVerified = models.BooleanField(default=False)
    isLocked = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Profile Configuration'
        verbose_name_plural = 'Profile Configurations'

    def __str__(self) -> str:
        return self.user.email
