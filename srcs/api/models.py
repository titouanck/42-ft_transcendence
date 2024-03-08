from django.db import models
from uuid import uuid4

# Create your models here.
class FortyTwoToken(models.Model):
	uid = models.UUIDField(primary_key = True, default = uuid4, editable = False)
	access_token = models.TextField()
	refresh_token = models.TextField(editable = False, null=True, blank=True)
	login = models.CharField(max_length=10, null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add = True, editable = False)
	access_expires_at = models.DateTimeField(null=True, blank=True)
	secret_expires_at = models.DateTimeField(editable = False, null=True, blank=True)

class Player(models.Model):
	uid = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True)
	username = models.SlugField(max_length=24, unique=True)
	login_42 = models.SlugField(max_length=12, unique=True, null=True, blank=True)
	pic = models.TextField(null=True, blank=True)
	email = models.EmailField(null=True, blank=True)
	token_42 = models.ForeignKey(FortyTwoToken, on_delete=models.SET_NULL, null=True, blank=True)
	
	class Status(models.IntegerChoices):
		OFFLINE = 0, 'Offline'
		ONLINE = 1, 'Online'
		PLAYING = 2, 'Playing'
	status = models.IntegerField(choices=Status.choices, default=Status.OFFLINE)
	
	elo = models.IntegerField(default=0)
	victories = models.IntegerField(default=0)
	defeats = models.IntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
