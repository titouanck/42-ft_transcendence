# Generated by Django 4.2 on 2024-04-06 18:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0010_alter_player_password_alter_player_password_hash'),
    ]

    operations = [
        migrations.RenameField(
            model_name='player',
            old_name='elo',
            new_name='player_elo',
        ),
        migrations.RenameField(
            model_name='player',
            old_name='rank',
            new_name='player_rank',
        ),
        migrations.RenameField(
            model_name='player',
            old_name='status',
            new_name='player_status',
        ),
        migrations.RemoveField(
            model_name='player',
            name='email',
        ),
        migrations.RemoveField(
            model_name='player',
            name='login_42',
        ),
        migrations.RemoveField(
            model_name='player',
            name='password',
        ),
        migrations.RemoveField(
            model_name='player',
            name='password_hash',
        ),
        migrations.RemoveField(
            model_name='player',
            name='permissions',
        ),
        migrations.RemoveField(
            model_name='player',
            name='profile_picture_url',
        ),
        migrations.RemoveField(
            model_name='player',
            name='username',
        ),
        migrations.AddField(
            model_name='player',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
