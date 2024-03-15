from django.db import models
from uuid import uuid4
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Pongtoken(models.Model):
	uid = models.UUIDField(primary_key = True, default = uuid4, editable = False)
	created_at = models.DateTimeField(auto_now_add = True, editable = False)
	expires_at = models.DateTimeField()

class Player(models.Model):
	uid = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True)
	username = models.SlugField(max_length=24, unique=True)
	pic = models.TextField(null=True, blank=True)
	email = models.EmailField(null=True, blank=True)
	login_42 = models.SlugField(max_length=12, unique=True, null=True, blank=True)
	pongtoken = models.ForeignKey(Pongtoken, on_delete=models.SET_NULL, null=True, blank=True)
	
	class Status(models.IntegerChoices):
		OFFLINE = 0, 'Offline'
		ONLINE = 1, 'Online'
		PLAYING = 2, 'Playing'
	status = models.IntegerField(choices=Status.choices, default=Status.OFFLINE)
	
	class Rank(models.TextChoices):
		UNRANKED = "UNRANKED", _("UNRANKED")
		BRONZE = "BRONZE", _("BRONZE")
		SILVER = "SILVER", _("SILVER")
		GOLD = "GOLD", _("GOLD")
		PLATINIUM = "PLATINIUM", _("PLATINIUM")
		DIAMOND = "DIAMOND", _("DIAMOND")
		ELITE = "ELITE", _("ELITE")
		CHAMPION = "CHAMPION", _("CHAMPION")
		UNREAL = "UNREAL", _("UNREAL")
	rank = models.TextField(choices=Rank.choices, default=Rank.UNRANKED)
	
	elo = models.IntegerField(default=0)
	victories = models.IntegerField(default=0)
	defeats = models.IntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
