from django.db import models
from uuid import uuid4
from django.utils.translation import gettext_lazy as _

class Player(models.Model):
	uid = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True)
	admin = models.BooleanField(default=False)
	username = models.SlugField(max_length=24, unique=True)
	pic = models.TextField(null=True, blank=True)
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

class Pongtoken(models.Model):
	uid = models.UUIDField(primary_key = True, default = uuid4, editable = False)
	user = models.ForeignKey(Player, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add = True, editable = False)
	expires_at = models.DateTimeField()