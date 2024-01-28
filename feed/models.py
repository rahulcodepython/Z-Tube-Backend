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
    ("like", "Like"),
    ("heart", "Heart"),
    ("care", "Care"),
    ("laugh", "Laugh"),
    ("wow", "Wow"),
    ("cry", "Cry"),
    ("angry", "Angry"),
]


class PostConfig(models.Model):
    id = models.OneToOneField(
        Post, on_delete=models.CASCADE, primary_key=True, editable=False)
    uploader = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
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


class Comment(models.Model):
    id = models.CharField(max_length=1000, primary_key=True,
                          editable=False, db_index=True)
    master = models.ForeignKey(
        "self", on_delete=models.CASCADE, related_name="+", null=True, blank=True)
    uploader = models.ForeignKey(
        User, on_delete=models.SET_DEFAULT, default=None, null=True)
    comment = models.TextField()
    createdAt = models.CharField(max_length=500)

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self) -> str:
        return f"{self.id}"


class CommentRecord(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE)
    comments = models.ManyToManyField(Comment)

    class Meta:
        verbose_name = 'Comment Record'
        verbose_name_plural = 'Comment Records'


class PostReaction(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reaction = models.CharField(
        max_length=100, choices=REACTION_CHOICE, default=None, blank=True, null=True)

    class Meta:
        verbose_name = 'Post Reaction'
        verbose_name_plural = 'Post Reactions'


class CommentReaction(models.Model):
    comment = models.OneToOneField(Comment, on_delete=models.CASCADE)
    like = models.ManyToManyField(User, related_name="like_comment")
    heart = models.ManyToManyField(User, related_name="heart_comment")
    care = models.ManyToManyField(User, related_name="care_comment")
    laugh = models.ManyToManyField(User, related_name="laugh_comment")
    wow = models.ManyToManyField(User, related_name="wow_comment")
    cry = models.ManyToManyField(User, related_name="cry_comment")
    angry = models.ManyToManyField(User, related_name="angry_comment")

    class Meta:
        verbose_name = 'Comment Reaction'
        verbose_name_plural = 'Comment Reactions'
