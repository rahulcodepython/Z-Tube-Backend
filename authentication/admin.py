from django.contrib.auth.models import Group
from django.contrib import admin
from . import models

admin.site.unregister(Group)


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name',
                    'username', 'is_active', 'is_superuser']


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'posts',
                    'followers', 'followings']


@admin.register(models.ProfileConfig)
class ProfileConfigAdmin(admin.ModelAdmin):
    list_display = ['user', 'isVerified', 'isLocked']
