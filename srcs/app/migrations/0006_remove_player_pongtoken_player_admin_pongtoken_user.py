# Generated by Django 4.2 on 2024-03-18 14:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_player_rank'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='pongtoken',
        ),
        migrations.AddField(
            model_name='player',
            name='admin',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='pongtoken',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='app.player'),
            preserve_default=False,
        ),
    ]
