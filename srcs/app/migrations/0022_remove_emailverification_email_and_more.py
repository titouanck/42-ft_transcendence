# Generated by Django 4.2.11 on 2024-04-08 17:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0021_remove_emailverification_created_at_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emailverification',
            name='email',
        ),
        migrations.RemoveField(
            model_name='emailverification',
            name='sended_at',
        ),
        migrations.RemoveField(
            model_name='emailverification',
            name='user',
        ),
        migrations.RemoveField(
            model_name='emailverification',
            name='verification_link',
        ),
        migrations.RemoveField(
            model_name='emailverification',
            name='verification_status',
        ),
    ]
