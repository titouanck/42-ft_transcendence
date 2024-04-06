from django.utils import timezone
from django.db import models
from uuid import uuid4
from django.utils.translation import gettext_lazy as _
from .Player import Player

# **************************************************************************** #

class Pongtoken(models.Model):
	uid = models.UUIDField(primary_key = True, default = uuid4, editable = False)
	user = models.ForeignKey(Player, on_delete=models.CASCADE)
	valid = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add = True, editable = False)
	expires_at = models.DateTimeField()

	# **************************************************************************** #
	
	def update_validity(self):
		if timezone.now() > self.expires_at:
			self.valid = False

	def invalidate(self):
		if self.valid:
			self.expires_at = timezone.now()
			self.update_validity()

	def is_valid(self):
		if self.valid:
			self.update_validity()
		return self.valid

	# **************************************************************************** #

	def __str__(self):
		if self.is_valid():
			return f'{self.uid}, {self.user.username} (valid until {self.expires_at})'
		else:
			return f'{self.uid}, {self.user.username} (expired)'
