# Generated by Django 5.1.6 on 2025-03-01 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slider', '0003_alter_slider_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slider',
            name='img',
            field=models.ImageField(default=None, unique=True, upload_to='media/slider_img/'),
        ),
    ]
