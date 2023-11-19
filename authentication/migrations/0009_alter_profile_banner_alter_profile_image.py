# Generated by Django 4.2.6 on 2023-11-10 16:47

import authentication.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0008_alter_profile_banner_alter_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='banner',
            field=models.ImageField(default='bannerImage/defaultBanner.png', upload_to=authentication.models.upload_to_banner),
        ),
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='userImage/defaultUser.png', upload_to=authentication.models.upload_to_user),
        ),
    ]