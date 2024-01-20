from django.contrib import admin
from . import models


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'caption']


@admin.register(models.PostConfig)
class PostConfigAdmin(admin.ModelAdmin):
    list_display = ['id']


@admin.register(models.PostRecord)
class PostRecordAdmin(admin.ModelAdmin):
    list_display = ['user']


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'master', 'uploader']


@admin.register(models.CommentRecord)
class CommentRecordAdmin(admin.ModelAdmin):
    list_display = ['post']
