# Generated by Django 4.2.6 on 2024-01-19 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0003_rename_like_postconfig_likeno_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postconfig',
            name='createdAt',
            field=models.CharField(max_length=500),
        ),
    ]