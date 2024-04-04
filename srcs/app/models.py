from django.utils import timezone
from django.db import models
from uuid import uuid4
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

class Player(models.Model):
	uid = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True)
	operator = models.BooleanField(default=False)
	username = models.SlugField(max_length=24, unique=True)
	image_url = models.TextField(null=True, blank=True)
	image = models.ImageField(upload_to='user_data/profile_picture/', null=True, blank=True)
	email = models.EmailField(null=True, blank=True)
	login_42 = models.SlugField(max_length=12, unique=True, null=True, blank=True)
	
	class Status(models.TextChoices):
		OFFLINE = 'Offline', _('Offline')
		ONLINE = 'Online', _('Online')
		PLAYING = 'Playing', _('Playing')
	status = models.TextField(choices=Status.choices, default=Status.OFFLINE)
	
	class Rank(models.TextChoices):
		UNRANKED = 'UNRANKED', _('UNRANKED')
		BRONZE = 'BRONZE', _('BRONZE')
		SILVER = 'SILVER', _('SILVER')
		GOLD = 'GOLD', _('GOLD')
		PLATINIUM = 'PLATINIUM', _('PLATINIUM')
		DIAMOND = 'DIAMOND', _('DIAMOND')
		ELITE = 'ELITE', _('ELITE')
		CHAMPION = 'CHAMPION', _('CHAMPION')
		UNREAL = 'UNREAL', _('UNREAL')
	rank = models.TextField(choices=Rank.choices, default=Rank.UNRANKED)
	
	elo = models.IntegerField(default=0)
	victories = models.IntegerField(default=0)
	defeats = models.IntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f'{self.username}, {self.uid}'
	
	def clean(self):
		forbidden_usernames = ['me', 'anonymous', 'guest', 'null', 'none']
		if self.username in forbidden_usernames:
			raise ValidationError("Forbidden username")
		super().clean()

	def get_image_url(self, request):
		if self.image_url.startswith('local.'):
			return f'{request.scheme}://{request.get_host()}/api/users/{self.uid}/image/'
		else:
			return self.image_url
		
	def publicData(self, request):
		return {
			'uid' : self.uid,
			'username' : self.username,
			'status' : self.status,
			'image_url' : self.get_image_url(request),
			'rank' : self.rank,
			'elo' : self.elo,
			'victories' : self.victories,
			'defeats' : self.defeats,
		}
	
	def privateData(self, request):
		return {
			'uid' : self.uid,
			'username' : self.username,
			'status' : self.status,
			'image_url' : self.get_image_url(request),
			'rank' : self.rank,
			'elo' : self.elo,
			'victories' : self.victories,
			'defeats' : self.defeats,
			'operator' : self.operator,
			'email' :  self.email,
			'login_42' :  self.login_42,
			'created_at' :  self.created_at,
			'updated_at' :  self.updated_at,
		}

class Pongtoken(models.Model):
	uid = models.UUIDField(primary_key = True, default = uuid4, editable = False)
	user = models.ForeignKey(Player, on_delete=models.CASCADE)
	invalidated = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add = True, editable = False)
	expires_at = models.DateTimeField()

	def is_expired(self):
		if timezone.now() > self.expires_at or self.invalidated:
			return True
		return False

	def __str__(self):
		if self.is_expired():
			return f'{self.uid}, {self.user.username} (expired)'
		else:
			return f'{self.uid}, {self.user.username} (valid until {self.expires_at})'

class Match(models.Model):
	uid = models.UUIDField(primary_key = True, default = uuid4, editable = False)

	class Status(models.TextChoices):
		PENDING = 'Pending', _('Pending')
		SCHEDULED = 'Scheduled', _('Scheduled')
		IN_PROGRESS = 'In progress', _('In progress')
		COMPLETED = 'Completed', _('Completed')
		ABANDONED = 'Abandoned', _('Abandoned')
	match_status = models.TextField(choices=Status.choices, default=Status.PENDING)
	scheduled_at = models.DateTimeField(blank=True, null=True)
	
	left_player = models.ForeignKey(Player, on_delete=models.SET_NULL, blank=True, null=True, related_name='left_player_uid')
	left_player_score = models.IntegerField(default=0)
	left_player_elo_initial = models.IntegerField(default=0)
	left_player_elo_final = models.IntegerField(default=0)
	
	right_player = models.ForeignKey(Player, on_delete=models.SET_NULL, blank=True, null=True, related_name='right_player_uid')
	right_player_score = models.IntegerField(default=0)
	right_player_elo_initial = models.IntegerField(default=0)
	right_player_elo_final = models.IntegerField(default=0)
	
	match_started_at = models.DateTimeField(blank=True, null=True)
	match_ended_at = models.DateTimeField(blank=True, null=True)
	
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		left = self.left_player.username if self.left_player else '...'
		right = self.right_player.username if self.right_player else '...'
		return f'{self.match_status}: {left} VS {right} [{self.left_player_score} - {self.right_player_score}]'
	
	def clean(self):
		if self.left_player_id and self.left_player_id == self.right_player_id:
			raise ValidationError("Left player and right player must be different.")
		super().clean()

	def get_left_player_uid(self):
		if self.left_player:
			return self.left_player.uid
		return None
	
	def get_right_player_uid(self):
		if self.right_player:
			return self.right_player.uid
		return None

	def get_left_player_username(self):
		if self.left_player:
			return self.left_player.username
		return None
	
	def get_right_player_username(self):
		if self.right_player:
			return self.right_player.username
		return None

	def publicData(self, request):
		match_winner_uid = None
		match_looser_uid = None
		print(self.match_status)
		if self.match_status == 'Completed':
			if self.left_player_score > self.right_player_score:
				match_winner_uid = self.left_player.uid
				match_looser_uid = self.right_player.uid
			elif self.right_player_score > self.left_player_score:
				match_winner_uid = self.right_player.uid
				match_looser_uid = self.left_player.uid

		left_player_elo_delta = self.left_player_elo_final - self.left_player_elo_initial
		right_player_elo_delta = self.right_player_elo_final - self.right_player_elo_initial

		return {
			'uid' : self.uid,
			'match_status' : self.match_status,
			'scheduled_at' : self.scheduled_at,
			'left_player_uid' : self.get_left_player_uid(),
			'left_player_username' : self.get_left_player_username(),
			'left_player_score' : self.left_player_score,
			'left_player_elo_initial' : self.left_player_elo_initial,
			'left_player_elo_final' : self.left_player_elo_initial,
			'left_player_elo_delta' : left_player_elo_delta,
			'right_player_uid' : self.get_right_player_uid(),
			'right_player_username' : self.get_right_player_username(),
			'right_player_score' : self.right_player_score,
			'right_player_elo_initial' : self.right_player_elo_initial,
			'right_player_elo_final' : self.right_player_elo_initial,
			'right_player_elo_delta' : right_player_elo_delta,
			'match_started_at' : self.match_started_at,
			'match_ended_at' : self.match_ended_at,
			'match_winner_uid' : match_winner_uid,
			'match_looser_uid' : match_looser_uid,
		}