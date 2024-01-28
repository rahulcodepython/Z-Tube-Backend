# Generated by Django 4.2.6 on 2024-01-27 08:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('feed', '0008_postconfig_uploader'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='postreaction',
            name='angry',
        ),
        migrations.RemoveField(
            model_name='postreaction',
            name='care',
        ),
        migrations.RemoveField(
            model_name='postreaction',
            name='cry',
        ),
        migrations.RemoveField(
            model_name='postreaction',
            name='heart',
        ),
        migrations.RemoveField(
            model_name='postreaction',
            name='laugh',
        ),
        migrations.RemoveField(
            model_name='postreaction',
            name='like',
        ),
        migrations.RemoveField(
            model_name='postreaction',
            name='wow',
        ),
        migrations.AddField(
            model_name='postreaction',
            name='reaction',
            field=models.CharField(blank=True, choices=[('like', 'Like'), ('heart', 'Heart'), ('care', 'Care'), ('laugh', 'Laugh'), ('wow', 'Wow'), ('cry', 'Cry'), ('angry', 'Angry')], default=None, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='postreaction',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='postreaction',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='feed.post'),
        ),
    ]
