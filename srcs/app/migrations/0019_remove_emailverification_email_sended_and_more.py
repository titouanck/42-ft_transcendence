# Generated by Django 4.2 on 2024-04-07 08:26

import app.utils
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0018_emailverification_delete_confirmationemail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emailverification',
            name='email_sended',
        ),
        migrations.RemoveField(
            model_name='player',
            name='email_confirmed',
        ),
        migrations.AddField(
            model_name='emailverification',
            name='email',
            field=models.EmailField(max_length=254, null=True, validators=[app.utils.isEmailValid]),
        ),
        migrations.AlterField(
            model_name='emailverification',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='emailverification_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
