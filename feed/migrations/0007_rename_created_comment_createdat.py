# Generated by Django 4.2.6 on 2024-01-23 02:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0006_postreaction_commentreaction'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='created',
            new_name='createdAt',
        ),
    ]
