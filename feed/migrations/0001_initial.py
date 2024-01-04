# Generated by Django 4.2.6 on 2023-12-29 21:29

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.CharField(db_index=True, editable=False, max_length=200, primary_key=True, serialize=False)),
                ('caption', models.TextField(default='')),
                ('tags', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), blank=True, size=3)),
                ('media', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), size=None)),
            ],
            options={
                'verbose_name': 'Post',
                'verbose_name_plural': 'Post',
            },
        ),
        migrations.CreateModel(
            name='PostRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('posts', models.ManyToManyField(to='feed.post')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Post Record',
                'verbose_name_plural': 'Post Records',
            },
        ),
        migrations.CreateModel(
            name='PostConfig',
            fields=[
                ('id', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='feed.post')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('isPublic', models.BooleanField(default=True)),
                ('isPersonal', models.BooleanField(default=False)),
                ('isPrivate', models.BooleanField(default=False)),
                ('isHidden', models.BooleanField(default=False)),
                ('like', models.IntegerField(default=0)),
                ('dislike', models.IntegerField(default=0)),
                ('views', models.IntegerField(default=0)),
                ('share', models.IntegerField(default=0)),
                ('allowComments', models.BooleanField(default=True)),
                ('commentNo', models.IntegerField(default=0)),
                ('hiddenFrom', models.ManyToManyField(blank=True, related_name='hidden_from', to=settings.AUTH_USER_MODEL)),
                ('master', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('visibleTo', models.ManyToManyField(blank=True, related_name='visible_to', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Post Configuration',
                'verbose_name_plural': 'Post Configurations',
            },
        ),
    ]
