from django.utils import timezone
from django.db import models
from uuid import uuid4
from django.utils.translation import gettext_lazy as _
from .Player import Player

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