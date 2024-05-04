from django.db import models
from . import manager as self_manager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.postgres.fields import ArrayField


AUTH_METHOD = (
    ('Credentials', 'Credentials'),
    ('Google', 'Google'),
    ('Github', 'Github'),
)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.BigAutoField(auto_created=True, primary_key=True,
                             serialize=False, verbose_name='ID', db_index=True)
    username = models.CharField(max_length=1000, unique=True)
    email = models.EmailField(unique=True, max_length=254, blank=True, null=True)
    first_name = models.CharField(max_length=1000, blank=True)
    last_name = models.CharField(max_length=1000, blank=True)
    method = models.CharField(max_length=50, default="Credentials", choices=AUTH_METHOD)
    bio = models.TextField(default='', blank=True)
    image = models.URLField(default='', blank=True, max_length=10000)
    banner = models.URLField(default='', blank=True, max_length=10000)
    tags = ArrayField(models.CharField(
        max_length=100, blank=True), size=5, blank=True, default=list)
    posts = models.IntegerField(default=0)
    followers = models.IntegerField(default=0)
    followings = models.IntegerField(default=0)
    connections = models.ManyToManyField(
        "self", blank=True)
    isVerified = models.BooleanField(default=False)
    isLocked = models.BooleanField(default=False)
    # password .....

    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    groups = None
    user_permissions = None
    last_login = None

    objects = self_manager.UserManager()

    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    USERNAME_FIELD = 'username'

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['first_name']

    def __str__(self) -> str:
        return self.username


class ActivationCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    uid = models.IntegerField(default=0)
    token = models.IntegerField(default=0)
    created_at = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Activation Code'
        verbose_name_plural = 'Activation Codes'

    def __str__(self) -> str:
        return self.user.username


class ResetPasswordCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    uid = models.IntegerField(default=0)
    token = models.IntegerField(default=0)
    created_at = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Reset Password Code'
        verbose_name_plural = 'Reset Password Codes'

    def __str__(self) -> str:
        return self.user.username


class ResetEmailCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.CharField(max_length=254)
    uid = models.IntegerField(default=0)
    token = models.IntegerField(default=0)
    created_at = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Reset Email Code'
        verbose_name_plural = 'Reset Email Codes'

    def __str__(self) -> str:
        return self.user.username
