# Generated by Django 5.0.4 on 2024-05-14 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='availibile_quantity',
            field=models.IntegerField(default=0),
        ),
    ]
