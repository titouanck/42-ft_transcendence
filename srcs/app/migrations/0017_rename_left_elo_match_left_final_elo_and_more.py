# Generated by Django 4.2 on 2024-04-04 22:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_pongtoken_invalidated'),
    ]

    operations = [
        migrations.RenameField(
            model_name='match',
            old_name='left_elo',
            new_name='left_final_elo',
        ),
        migrations.RenameField(
            model_name='match',
            old_name='right_elo',
            new_name='left_initial_elo',
        ),
        migrations.AddField(
            model_name='match',
            name='right_final_elo',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='match',
            name='right_initial_elo',
            field=models.IntegerField(default=0),
        ),
    ]
