# Generated by Django 4.2 on 2024-04-03 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_player_image_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='user_data/profile_picture/'),
        ),
    ]
