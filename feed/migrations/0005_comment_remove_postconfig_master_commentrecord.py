# Generated by Django 4.2.6 on 2024-01-20 03:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('feed', '0004_alter_postconfig_createdat'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.CharField(db_index=True, editable=False, max_length=1000, primary_key=True, serialize=False)),
                ('comment', models.TextField()),
                ('created', models.CharField(max_length=500)),
                ('master', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='feed.comment')),
                ('uploader', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Comment',
                'verbose_name_plural': 'Comments',
            },
        ),
        migrations.RemoveField(
            model_name='postconfig',
            name='master',
        ),
        migrations.CreateModel(
            name='CommentRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comments', models.ManyToManyField(to='feed.comment')),
                ('post', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='feed.post')),
            ],
            options={
                'verbose_name': 'Comment Record',
                'verbose_name_plural': 'Comment Records',
            },
        ),
    ]