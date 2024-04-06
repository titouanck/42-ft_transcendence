from django.db import models
from uuid import uuid4
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from .Player import Player

from .choices import needed_length
from .choices import MATCH_STATUS, MATCH_STATUS_DEFAULT
from .choices import MATCH_TYPE, MATCH_TYPE_DEFAULT

# **************************************************************************** #

class Match(models.Model):
	uid = models.UUIDField(primary_key = True, default = uuid4, editable = False)

	match_status = models.CharField(max_length=needed_length(MATCH_STATUS), choices=MATCH_STATUS, default=MATCH_STATUS_DEFAULT)
	match_type = models.CharField(max_length=needed_length(MATCH_TYPE), choices=MATCH_TYPE, default=MATCH_TYPE_DEFAULT)

	scheduled_at = models.DateTimeField(blank=True, null=True)
		
	left_player = models.ForeignKey(Player, on_delete=models.SET_NULL, blank=True, null=True, related_name='left_player_uid')
	left_player_score = models.IntegerField(default=0)
	left_player_elo_initial = models.IntegerField(default=0)
	left_player_elo_final = models.IntegerField(default=0)
	
	right_player = models.ForeignKey(Player, on_delete=models.SET_NULL, blank=True, null=True, related_name='right_player_uid')
	right_player_score = models.IntegerField(default=0)
	right_player_elo_initial = models.IntegerField(default=0)
	right_player_elo_final = models.IntegerField(default=0)

	match_winner = models.ForeignKey(Player, on_delete=models.SET_NULL, blank=True, null=True, related_name='match_winner_uid')
	match_looser = models.ForeignKey(Player, on_delete=models.SET_NULL, blank=True, null=True, related_name='match_looser_uid')
	
	match_started_at = models.DateTimeField(blank=True, null=True)
	match_ended_at = models.DateTimeField(blank=True, null=True)
	
	# tournament = models.ForeignKey(Tournament, on_delete=models.SET_NULL, blank=True, null=True, related_name='tournament_uid')
	
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	# **************************************************************************** #
	
	def __str__(self):
		left = self.left_player.username if self.left_player else '...'
		right = self.right_player.username if self.right_player else '...'
		return f'{self.match_status}: {left} VS {right} [{self.left_player_score} - {self.right_player_score}]'
	
	def clean(self):
		if self.left_player_id and self.left_player_id == self.right_player_id:
			raise ValidationError("Left player and right player must be different.")
		super().clean()

	# **************************************************************************** #
	# def is_part_of_tournament(self):
	# 	return self.tournament

	# def get_tournament_uid(self):
		# if self.tournament:
		# 	return self.tournament.uid
		# return None
	
	# def get_left_player_uid(self):
	# 	if self.left_player:
	# 		return self.left_player.uid
	# 	return None
	
	# def get_right_player_uid(self):
	# 	if self.right_player:
	# 		return self.right_player.uid
	# 	return None

	# def get_left_player_username(self):
	# 	if self.left_player:
	# 		return self.left_player.username
	# 	return None
	
	# def get_right_player_username(self):
	# 	if self.right_player:
	# 		return self.right_player.username
	# 	return None
	
	# def get_match_winner_uid(self):
	# 	if self.match_winner:
	# 		return self.match_winner.uid
	# 	return None

	# def get_match_looser_uid(self):
	# 	if self.match_looser:
	# 		return self.match_looser.uid
	# 	return None
	
	# def get_left_player_elo_delta(self):
	# 	return self.left_player_elo_final - self.left_player_elo_initial
	
	# def get_right_player_elo_delta(self):
	# 	return self.right_player_elo_final - self.right_player_elo_initial

	# **************************************************************************** #

	def publicData(self, request):

		data = {
			# 'uid' : self.uid,
			# 'match_status' : self.match_status,
			# 'match_type' : self.match_type,
			# 'match_tournament' : self.get_tournament_uid(),
			# 'scheduled_at' : self.scheduled_at,
			# 'left_player_uid' : self.get_left_player_uid(),
			# 'left_player_username' : self.get_left_player_username(),
			# 'left_player_score' : self.left_player_score,
			# 'left_player_elo_initial' : self.left_player_elo_initial,
			# 'left_player_elo_final' : self.left_player_elo_initial,
			# 'left_player_elo_delta' : self.get_left_player_elo_delta(),
			# 'right_player_uid' : self.get_right_player_uid(),
			# 'right_player_username' : self.get_right_player_username(),
			# 'right_player_score' : self.right_player_score,
			# 'right_player_elo_initial' : self.right_player_elo_initial,
			# 'right_player_elo_final' : self.right_player_elo_initial,
			# 'right_player_elo_delta' : self.get_right_player_elo_delta(),
			# 'match_started_at' : self.match_started_at,
			# 'match_ended_at' : self.match_ended_at,
			# 'match_winner_uid' : self.get_match_winner_uid(),
			# 'match_looser_uid' : self.get_match_looser_uid()
		}

		# if self.match_type == 'Casual':
		# 	del data['left_player_elo_initial'], data['left_player_elo_final'], data['left_player_elo_delta']
		# 	del data['right_player_elo_initial'], data['right_player_elo_final'], data['right_player_elo_delta']
		# if self.match_type != 'Tournament':
		# 	del data['match_tournament']
		# return data


# """
# tournamentround1:
# 	1
# 	T42
# 	R1
# 	M1

# 	1
# 	T42
# 	R1
# 	M2


# """