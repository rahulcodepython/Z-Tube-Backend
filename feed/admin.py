from django.contrib import admin
from . import models


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'caption', 'uploader', 'isPublic', 'isProtected', 'isPersonal',
                    'isHidden', 'isPrivate', 'likeNo', 'allowComments', 'commentNo']


@admin.register(models.PostRecord)
class PostRecordAdmin(admin.ModelAdmin):
    list_display = ['user']


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'master', 'uploader']


@admin.register(models.CommentRecord)
class CommentRecordAdmin(admin.ModelAdmin):
    list_display = ['post']


@admin.register(models.PostReaction)
class PostReactionAdmin(admin.ModelAdmin):
    list_display = ['post', 'user', 'reaction']
