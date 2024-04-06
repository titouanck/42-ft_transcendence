# Generated by Django 4.2 on 2024-04-06 00:56

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('username', models.SlugField(max_length=24, unique=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='user_data/profile_picture/')),
                ('profile_picture_url', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('Offline', 'Offline'), ('Online', 'Online'), ('Playing', 'Playing')], default='Offline', max_length=22)),
                ('elo', models.IntegerField(default=0)),
                ('rank', models.CharField(choices=[('UNRANKED', 'UNRANKED'), ('BRONZE', 'BRONZE'), ('SILVER', 'SILVER'), ('GOLD', 'GOLD'), ('PLATINIUM', 'PLATINIUM'), ('DIAMOND', 'DIAMOND'), ('ELITE', 'ELITE'), ('CHAMPION', 'CHAMPION'), ('UNREAL', 'UNREAL')], default='UNRANKED', max_length=26)),
                ('total_victories', models.IntegerField(default=0)),
                ('total_defeats', models.IntegerField(default=0)),
                ('login_42', models.SlugField(blank=True, max_length=12, null=True, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserPermission',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('system_logs', models.SmallIntegerField(default=0)),
                ('own_profile', models.SmallIntegerField(default=0)),
                ('any_visible_profile', models.SmallIntegerField(default=2)),
                ('any_invisible_profile', models.SmallIntegerField(default=0)),
                ('own_private_data', models.SmallIntegerField(default=0)),
                ('any_private_data', models.SmallIntegerField(default=0)),
                ('outgoing_message_to_friends', models.SmallIntegerField(default=0)),
                ('outgoing_message_to_any', models.SmallIntegerField(default=0)),
                ('incoming_message_from_friends', models.SmallIntegerField(default=0)),
                ('incoming_message_from_any', models.SmallIntegerField(default=0)),
                ('any_message', models.SmallIntegerField(default=0)),
                ('own_relationships', models.SmallIntegerField(default=0)),
                ('any_relationship', models.SmallIntegerField(default=0)),
                ('own_permissions', models.SmallIntegerField(default=0)),
                ('other_permissions', models.SmallIntegerField(default=0)),
                ('ignore_recipient_message_restriction', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Pongtoken',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('invalidated', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('expires_at', models.DateTimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.player')),
            ],
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('match_status', models.CharField(choices=[('Pending', 'Pending'), ('Scheduled', 'Scheduled'), ('In progress', 'In progress'), ('Completed', 'Completed'), ('Abandoned', 'Abandoned')], default='Pending', max_length=30)),
                ('match_type', models.CharField(choices=[('Ranked', 'Ranked'), ('Casual', 'Casual'), ('Tournament', 'Tournament')], default='Ranked', max_length=28)),
                ('scheduled_at', models.DateTimeField(blank=True, null=True)),
                ('left_player_score', models.IntegerField(default=0)),
                ('left_player_elo_initial', models.IntegerField(default=0)),
                ('left_player_elo_final', models.IntegerField(default=0)),
                ('right_player_score', models.IntegerField(default=0)),
                ('right_player_elo_initial', models.IntegerField(default=0)),
                ('right_player_elo_final', models.IntegerField(default=0)),
                ('match_started_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('left_player', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='left_player_uid', to='app.player')),
                ('match_looser', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='match_looser_uid', to='app.player')),
                ('match_winner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='match_winner_uid', to='app.player')),
                ('right_player', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='right_player_uid', to='app.player')),
            ],
        ),
    ]
