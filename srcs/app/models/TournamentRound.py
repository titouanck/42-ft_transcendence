from django.db import models
from uuid import uuid4
from .Tournament import Tournament

class TournamentRound(models.Model):
	uid = models.UUIDField(primary_key = True, default = uuid4, editable = False)
	tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, null=True, related_name='tournamentround_tournament')

	round_number = models.IntegerField(default=0)
	round_started_at = models.DateTimeField(blank=True, null=True)
	round_ended_at = models.DateTimeField(blank=True, null=True)
	
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
