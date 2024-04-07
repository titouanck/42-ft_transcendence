import os
import mailjet_rest
from django.db import models
from uuid import uuid4
from django.utils import timezone
import secrets
import string

from app import utils

from .choices import needed_length, STATUS, STATUS_DEFAULT, IN_PROGRESS, ABANDONED, COMPLETED
from django.contrib.auth.models import User

# **************************************************************************** #

def generate_slug():
	slug = ''.join(secrets.choice(string.ascii_letters + string.digits) for i in range(42))
	return slug

def generate_expiration_timestamp():
	return timezone.now() + timezone.timedelta(hours=1)

class EmailVerification(models.Model):
	
	uid = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True)

	user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='emailverification_user')

	email = models.EmailField(null=True, validators=[utils.isEmailValid])

	verification_status = models.CharField(max_length=needed_length(STATUS), choices=STATUS, default=STATUS_DEFAULT)

	verification_slug = models.SlugField(default=generate_slug)

	created_at = models.DateTimeField(auto_now_add=True)
	
	expires_at = models.DateTimeField(default=generate_expiration_timestamp)

	# **************************************************************************** #

	def __str__(self):
		return f'{self.user.username if self.user else self.uid}'
	
	def save(self, *args, **kwargs):
		if self.verification_status != COMPLETED:
			if timezone.now() >= self.expires_at:
				self.verification_status = ABANDONED
			elif self.verification_status == STATUS_DEFAULT:
				self.send()
		super().save(*args, **kwargs)

	def is_valid(self):
		if self.verification_status != COMPLETED and timezone.now() >= self.expires_at:
			self.verification_status = ABANDONED
		return True if self.verification_status == IN_PROGRESS else False
	
	# **************************************************************************** #
	
	def send(self):
		if self.verification_status == STATUS_DEFAULT and self.user:
			api_key = os.environ['MAILJET_ID']
			api_secret = os.environ['MAILJET_SECRET']
			mailjet = mailjet_rest.Client(auth=(api_key, api_secret), version='v3.1')
			data = {
				'Messages': [
					{
						"From": {
							"Email": "ft_transcendence@titouanck.fr",
							"Name": "ft_transcendence"
						},
						"To": [
							{
							"Email": f"{self.email}",
							"Name": f"{self.user.username}"
							}
						],
						"Subject": "Confirm your email.",
						"TextPart": "Confirmation email",
						"HTMLPart": f"<span>Dear <strong>{self.user.username}</strong>, please <a href='http://127.0.0.1:8000/api/confirm-email/{self.verification_slug}/'>confirm your email</a>.</span>",
						"CustomID": "AppGettingStartedTest"
					}
				]
			}
			result = mailjet.send.create(data=data)
			if result.status_code == 200:
				self.verification_status = IN_PROGRESS
				return True
		return False

