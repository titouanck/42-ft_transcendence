# Generated by Django 4.2 on 2024-04-06 03:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_rename_password_player_password_hash'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='password',
            field=models.TextField(blank=True, null=True),
        ),
    ]