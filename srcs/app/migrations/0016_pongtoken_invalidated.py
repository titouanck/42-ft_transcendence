# Generated by Django 4.2 on 2024-04-04 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_match_scheduled_at_match_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='pongtoken',
            name='invalidated',
            field=models.BooleanField(default=False),
        ),
    ]
