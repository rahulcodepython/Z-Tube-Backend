from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
import uuid

User = get_user_model()


class Post(models.Model):
    id = models.CharField(max_length=1000, primary_key=True,
                          editable=False, db_index=True)
    caption = models.TextField(default="")
    tags = ArrayField(models.CharField(max_length=100), size=3, blank=True)
    media = ArrayField(models.CharField(max_length=5000))

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Post'

    def __str__(self) -> str:
        return f"{self.id}"

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = uuid.uuid4()
            return super().save(*args, **kwargs)


REACTION_CHOICE = [
    ("0", "Like"),
    ("1", "Heart"),
    ("2", "Care"),
    ("3", "Laugh"),
    ("4", "Amazed"),
    ("5", "Cry"),
    ("6", "Angry"),
]


class PostConfig(models.Model):
    id = models.OneToOneField(
        Post, on_delete=models.CASCADE, primary_key=True, editable=False)
    master = models.ForeignKey(User, on_delete=models.CASCADE)
    createdAt = models.CharField(max_length=500)
    isPublic = models.BooleanField(default=False)
    isProtected = models.BooleanField(default=False)
    isPersonal = models.BooleanField(default=False)
    isHidden = models.BooleanField(default=False)
    isPrivate = models.BooleanField(default=False)
    visibleTo = models.ManyToManyField(
        User, related_name='visible_to', blank=True)
    hiddenFrom = models.ManyToManyField(
        User, related_name='hidden_from', blank=True)
    likeNo = models.IntegerField(default=0)
    viewsNo = models.IntegerField(default=0)
    share = models.IntegerField(default=0)
    allowComments = models.BooleanField(default=True)
    commentNo = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Post Configuration'
        verbose_name_plural = 'Post Configurations'

    def __str__(self) -> str:
        return f"{self.id}"


class PostRecord(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    posts = models.ManyToManyField(Post)

    class Meta:
        verbose_name = 'Post Record'
        verbose_name_plural = 'Post Records'
