# Generated by Django 4.2 on 2024-03-28 17:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_alter_player_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='player',
            old_name='admin',
            new_name='operator',
        ),
    ]
