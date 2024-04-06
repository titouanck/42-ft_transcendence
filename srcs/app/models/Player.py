from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ObjectDoesNotExist
from PIL import Image
import os
from django.db import models
from uuid import uuid4
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from .UserPermission import UserPermission
from django.db.models.signals import post_save
from django.utils import timezone

from .choices import needed_length
from .choices import PLAYER_STATUS, PLAYER_STATUS_DEFAULT
from .choices import PLAYER_RANKS, PLAYER_RANKS_DEFAULT

# **************************************************************************** #

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
		if aspect_ratio < 9/10 or aspect_ratio > 4/3:
			raise ValidationError('Image aspect ratio must be between 1:1 and 4:3')
	except Exception as e:
		raise e

class Player(models.Model):
	
	uid = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True)

	permissions = models.OneToOneField(UserPermission, on_delete=models.CASCADE, editable=False, related_name='permissions_uid')

	username = models.SlugField(max_length=24, unique=True)

	email = models.EmailField(null=True, blank=True)

	profile_picture = models.ImageField(upload_to=rename_profile_picture, validators=[validate_profile_picture], null=True, blank=True)

	profile_picture_url = models.TextField(null=True, blank=True)

	status = models.CharField(max_length=needed_length(PLAYER_STATUS), choices=PLAYER_STATUS, default=PLAYER_STATUS_DEFAULT)

	elo = models.IntegerField(default=-1)

	rank = models.CharField(max_length=needed_length(PLAYER_RANKS), choices=PLAYER_RANKS, default=PLAYER_RANKS_DEFAULT)

	total_victories = models.IntegerField(default=0)

	total_defeats = models.IntegerField(default=0)

	total_matches = models.IntegerField(default=0)

	login_42 = models.SlugField(max_length=12, unique=True, null=True, blank=True)

	password = models.CharField(max_length=255, null=True, blank=True)

	password_hash = models.CharField(max_length=255, null=True, blank=True)

	created_at = models.DateTimeField(auto_now_add=True)

	updated_at = models.DateTimeField(auto_now=True)

	# **************************************************************************** #

	def __str__(self):
		return f'{self.username}, {self.uid} ({self.rank})'

	def save(self, *args, **kwargs):
		if self.password and not self.password_hash:
			self.password_hash = make_password(self.password)
		self.update_all()
		super().save(*args, **kwargs)
	
	def clean(self):
		forbidden_usernames = ['me', 'anonymous', 'guest', 'null', 'none']
		if self.username in forbidden_usernames:
			raise ValidationError("Forbidden username")
		super().clean()

	# **************************************************************************** #

	def update_permissions(self):
		try:
			self.permissions
		except ObjectDoesNotExist:
			self.permissions = UserPermission.objects.create()

	def update_profile_picture(self):
		if self.pk:
			try:
				old_instance = Player.objects.get(pk=self.pk)
				old_image = old_instance.profile_picture
			except Player.DoesNotExist:
				pass
			else:
				new_image = self.profile_picture
				if old_image != new_image:
					if os.path.isfile(old_image.path):
						os.remove(old_image.path)
		if self.profile_picture:
			self.profile_picture_url = f'/api/users/{self.uid}/profile_picture/'

	def update_rank(self):
		min_elo = -1
		for rank in PLAYER_RANKS:
			if min_elo < 0:
				min_elo = 0
			elif min_elo == 0 and self.elo >= 0:
				min_elo = 10
			elif self.elo >= min_elo:
				min_elo *= 2
			else:
				break
			self.rank = rank[1]

	def update_total_matches(self):
		self.total_matches = self.total_victories + self.total_defeats

	def update_password(self):
		if self.password:
			self.password_hash = make_password(self.password)
			self.password = None

	def update_all(self):
		self.update_permissions()
		self.update_profile_picture()
		self.update_rank()
		self.update_password()
		self.update_total_matches()

	# **************************************************************************** #

	def check_password(self, raw_password):
		return check_password(raw_password, self.password_hash)

	# **************************************************************************** #

	def get_profile_picture_url(self, request):
		self.update_profile_picture()
		if self.profile_picture_url:
			if self.profile_picture_url[0] == '/':
				return f'{request.scheme}://{request.get_host()}{self.profile_picture_url}'
			return self.profile_picture_url
		else:
			return None

	# **************************************************************************** #

	def data(self, request):
		self.update_all()
		data = {}
		fields = self._meta.fields
		for field in fields:
			field_name = field.name
			field_value = getattr(self, field_name)
			data[field_name] = field_value
		data['profile_picture_url'] = self.get_profile_picture_url(request)
		del data['permissions']
		del data['profile_picture']
		return data

	def publicData(self, request):
		data = self.data(request)
		del data['email']
		del data['login_42']
		return data
	
# 	def privateData(self, request):
# 		return {
# 			# 'uid' : self.uid,
# 			# 'username' : self.username,
# 			# 'status' : self.status,
# 			# 'image_url' : self.get_image_url(request),
# 			# 'rank' : self.rank,
# 			# 'elo' : self.elo,
# 			# 'victories' : self.victories,
# 			# 'defeats' : self.defeats,
# 			# 'email' :  self.email,
# 			# 'login_42' :  self.login_42,
# 			# 'created_at' :  self.created_at,
# 			# 'updated_at' :  self.updated_at,
# 		}
