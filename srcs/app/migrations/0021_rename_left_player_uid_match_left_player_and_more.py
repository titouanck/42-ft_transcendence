# Generated by Django 4.2 on 2024-04-04 23:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_rename_lplayer_elo_delta_match_left_player_elo_delta_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='match',
            old_name='left_player_uid',
            new_name='left_player',
        ),
        migrations.RenameField(
            model_name='match',
            old_name='right_player_uid',
            new_name='right_player',
        ),
    ]