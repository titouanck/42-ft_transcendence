from PIL import Image
import os
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

	def delete_image(self):
		try:
			os.remove(self.image.path)
			self.image.delete()
		except Exception as e:
			print(f"Error: {e.strerror}")

	def upload_image(self, uploadedImage):
		try:
			img = Image.open(uploadedImage)
			img.verify()
			width, height = img.size
			aspect_ratio = width / height
			if aspect_ratio < 9/10 or aspect_ratio > 4/3:
				raise Exception('Image aspect ratio must be between 9:10 and 4:3')
			original_filename, original_extension = os.path.splitext(uploadedImage.name)
			timestamp = f"{str(timezone.now()).replace('-', '').replace(' ', '').replace(':', '')[:len('YYYYMMDDHHMMSS')]}UTC"
			new_filename = f'{self.uid}_{timestamp}{original_extension}'
			self.image_url = None
			self.delete_image()
			self.image.save(new_filename, uploadedImage)
		except Exception as e:
			raise e

	def get_image_url(self, request):
		if self.image:
			return f'{request.scheme}://{request.get_host()}/api/users/{self.uid}/image/'
		elif self.image_url:
			return self.image_url
		else:
			return None
		
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
