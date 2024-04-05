# Generated by Django 4.2 on 2024-03-15 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_player_rank'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='rank',
            field=models.TextField(choices=[('UNRANKED', 'UNRANKED'), ('BRONZE', 'BRONZE')], default='UNRANKED'),
        ),
    ]