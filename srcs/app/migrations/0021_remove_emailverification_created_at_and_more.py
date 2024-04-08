# Generated by Django 4.2.11 on 2024-04-08 17:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0020_alter_emailverification_expires_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emailverification',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='emailverification',
            name='expires_at',
        ),
        migrations.RemoveField(
            model_name='emailverification',
            name='verification_slug',
        ),
        migrations.AddField(
            model_name='emailverification',
            name='sended_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='emailverification',
            name='verification_link',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='emailverification',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
