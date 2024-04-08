from PIL import Image
import os
from django.db import models
from uuid import uuid4
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .EmailVerification import EmailVerification

import secrets
import string

from app import utils

from .choices import needed_length
from .choices import PLAYER_STATUS, PLAYER_STATUS_DEFAULT
from .choices import PLAYER_RANKS, PLAYER_RANKS_DEFAULT

# **************************************************************************** #

class PlayerManager(models.Manager):
	def create(self, user=None, email=None, **kwargs):
		kwargs['user'] = user
		response = super().create(**kwargs)
		if user and email:
			try:
				instance = EmailVerification.objects.create(user=user, email=email)
				if not instance.send():
					raise Exception('Could not send an email to the given address')
			except Exception as e:
				raise e
		return response

def rename_profile_picture(instance, filename):
	upload_to = 'user_data/profile_picture/'
	extension = filename.split('.')[-1]
	filename = '{}.{}'.format(instance.uid, extension)
	return os.path.join(upload_to, filename)

def validate_profile_picture(image):
	try:
		img = Image.open(image)
		img.verify()
		width, height = img.size
		aspect_ratio = width / height
		if aspect_ratio != 1/1:
			raise ValidationError('Image aspect ratio must be 1:1')
	except Exception as e:
		raise e
	
def validate_username(value):
    forbidden_names = ['me', 'new', 'create', 'read', 'update', 'delete']
    if value.lower() in forbidden_names:
        raise ValidationError(f"Username cannot be part of {forbidden_names}")
	
User._meta.get_field('username').validators.append(validate_username)
	
class Player(models.Model):
	
	uid = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True)

	user = models.OneToOneField(User, null=True, blank=True, unique=True, on_delete=models.CASCADE, related_name='player_user')

	profile_picture = models.ImageField(upload_to=rename_profile_picture, validators=[validate_profile_picture], null=True, blank=True)

	player_status = models.CharField(max_length=needed_length(PLAYER_STATUS), choices=PLAYER_STATUS, default=PLAYER_STATUS_DEFAULT)

	player_elo = models.IntegerField(default=None, null=True, blank=True)

	player_rank = models.CharField(max_length=needed_length(PLAYER_RANKS), choices=PLAYER_RANKS, default=PLAYER_RANKS_DEFAULT)

	total_victories = models.IntegerField(default=0)

	total_defeats = models.IntegerField(default=0)

	total_matches = models.IntegerField(default=0)

	created_at = models.DateTimeField(auto_now_add=True)

	updated_at = models.DateTimeField(auto_now=True)

	objects = PlayerManager()

	# **************************************************************************** #

	def __str__(self):
		return f'{self.user.username if self.user else self.uid}, {self.player_rank}'
	
	def clean(self):
		self.update_all()
		super().clean()

	# **************************************************************************** #

	def update_profile_picture(self):
		if self.pk:
			try:
				old_instance = Player.objects.get(pk=self.pk)
				old_image = old_instance.profile_picture
			except Player.DoesNotExist:
				pass
			else:
				try:
					new_image = self.profile_picture
					if old_image and old_image != new_image:
						if os.path.isfile(old_image.path):
							os.remove(old_image.path)
				except Exception as e:
					raise e

	def update_rank(self):
		if self.player_elo is None:
			self.player_rank = PLAYER_RANKS_DEFAULT
		else:
			min_elo = -1
			for rank in PLAYER_RANKS:
				if min_elo < 0:
					min_elo = 0
				elif min_elo == 0:
					min_elo = 10
				elif self.player_elo >= min_elo:
					min_elo *= 2
				else:
					break
				self.player_rank = rank[1]

	def update_total_matches(self):
		self.total_matches = self.total_victories + self.total_defeats

	def update_user(self):
		if not self.user:
			username = ''.join(secrets.choice(string.ascii_lowercase) for i in range(8))
			password = ''.join(secrets.choice(string.ascii_letters + string.digits + string.punctuation) for i in range(20))
			email = ''
			user = User.objects.create_user(username, email, password)
			self.user = user

	def update_all(self):
		self.update_user()
		self.update_profile_picture()
		self.update_rank()
		self.update_total_matches()

	# **************************************************************************** #

	def set_username(self, username):
		if self.user:
			try:
				self.user.username = username
				self.user.save()
				return True
			except Exception as e:
				pass
		return False
	
	def set_email(self, email):
		if self.user:
			try:
				if not utils.isEmailValid(email):
					raise ValueError('This email is not valid.')
				self.user.email = email
				self.user.save()
				return True
			except Exception as e:
				pass
		return False

	# **************************************************************************** #
	
	def get_profile_picture_url(self, request):
		if self.profile_picture:
			return f'{request.scheme}://{request.get_host()}/api/users/{self.uid}/profile_picture/'
		else:
			return None
		
	def get_username(self):
		return self.user.username if self.user else None
	
	def get_email(self):
		return self.user.email if self.user else None
