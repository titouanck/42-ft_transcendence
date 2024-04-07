from django.db import models
from uuid import uuid4
from .Player import Player

class Tournament(models.Model):
	uid = models.UUIDField(primary_key = True, default = uuid4, editable = False)

	elo_min = models.IntegerField(default=None, null=True, blank=True)
	elo_max = models.IntegerField(default=None, null=True, blank=True)

	tournament_winner = models.ForeignKey(Player, on_delete=models.SET_NULL, blank=True, null=True, related_name='tournament_tournament_winner_uid')
	tournament_started_at = models.DateTimeField(blank=True, null=True)
	tournament_ended_at = models.DateTimeField(blank=True, null=True)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
