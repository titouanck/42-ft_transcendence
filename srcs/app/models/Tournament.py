# from django.db import models
# from uuid import uuid4
# from django.utils.translation import gettext_lazy as _
# from .Match import Match
# from .Player import Player

# class Tournament(models.Model):
# 	uid = models.UUIDField(primary_key = True, default = uuid4, editable = False)
	
# 	tournament_winner = models.ForeignKey(Player, on_delete=models.SET_NULL, blank=True, null=True, related_name='tournament_winner_uid')
# 	tournament_looser = models.ForeignKey(Player, on_delete=models.SET_NULL, blank=True, null=True, related_name='tournament_looser_uid')

# 	rank_min = 

# 	tournament_started_at = models.DateTimeField(blank=True, null=True)
# 	tournament_ended_at = models.DateTimeField(blank=True, null=True)


# 	created_at = models.DateTimeField(auto_now_add=True)
# 	updated_at = models.DateTimeField(auto_now=True)


# class TournamentRound(models.Model):
# 	uid = models.UUIDField(primary_key = True, default = uuid4, editable = False)

# 	tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, blank=True, null=True, related_name='tournament_uid')
# 	round_number = models.IntegerField(default=0)

# 	round_started_at = models.DateTimeField(blank=True, null=True)
# 	round_ended_at = models.DateTimeField(blank=True, null=True)

	
# 	created_at = models.DateTimeField(auto_now_add=True)
# 	updated_at = models.DateTimeField(auto_now=True)

