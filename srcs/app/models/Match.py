from django.db import models
from uuid import uuid4
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from .Player import Player
from .Tournament import Tournament
from .TournamentRound import TournamentRound

from .choices import needed_length
from .choices import STATUS, STATUS_DEFAULT
from .choices import MATCH_TYPE, MATCH_TYPE_DEFAULT

# **************************************************************************** #

class Match(models.Model):
	uid = models.UUIDField(primary_key = True, default = uuid4, editable = False)

	match_type = models.CharField(max_length=needed_length(MATCH_TYPE), choices=MATCH_TYPE, default=MATCH_TYPE_DEFAULT)
	match_status = models.CharField(max_length=needed_length(STATUS), choices=STATUS, default=STATUS_DEFAULT)

	left_player = models.ForeignKey(Player, on_delete=models.SET_NULL, blank=True, null=True, related_name='match_left_player')
	left_player_score = models.IntegerField(default=0)
	left_player_elo_initial = models.IntegerField(default=0)
	left_player_elo_final = models.IntegerField(default=0)
	
	right_player = models.ForeignKey(Player, on_delete=models.SET_NULL, blank=True, null=True, related_name='match_right_player')
	right_player_score = models.IntegerField(default=0)
	right_player_elo_initial = models.IntegerField(default=0)
	right_player_elo_final = models.IntegerField(default=0)

	match_winner = models.ForeignKey(Player, on_delete=models.SET_NULL, blank=True, null=True, related_name='match_match_winner')
	match_looser = models.ForeignKey(Player, on_delete=models.SET_NULL, blank=True, null=True, related_name='match_match_looser')
	
	match_started_at = models.DateTimeField(blank=True, null=True)
	match_ended_at = models.DateTimeField(blank=True, null=True)
	
	tournament = models.ForeignKey(Tournament, on_delete=models.SET_NULL, blank=True, null=True, related_name='match_tournament')
	tournament_round = models.ForeignKey(TournamentRound, on_delete=models.SET_NULL, blank=True, null=True, related_name='match_tournament_round')
	
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	# **************************************************************************** #
	
	def __str__(self):
		left = self.left_player.get_username() if self.left_player and self.left_player.user else '...'
		right = self.right_player.get_username() if self.right_player and self.right_player.user else '...'
		return f'{self.match_status}: {left} VS {right} [{self.left_player_score} - {self.right_player_score}]'
	
	def clean(self):
		if self.left_player_id and self.left_player_id == self.right_player_id:
			raise ValidationError("Left player and right player must be different.")
		super().clean()

	# **************************************************************************** #
	