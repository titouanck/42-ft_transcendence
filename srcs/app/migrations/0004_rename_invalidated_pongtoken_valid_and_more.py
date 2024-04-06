# Generated by Django 4.2 on 2024-04-06 02:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_match_match_ended_at'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pongtoken',
            old_name='invalidated',
            new_name='valid',
        ),
        migrations.AddField(
            model_name='player',
            name='total_matches',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='player',
            name='elo',
            field=models.IntegerField(default=-1),
        ),
    ]