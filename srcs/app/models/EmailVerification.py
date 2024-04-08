import os
import mailjet_rest
from django.db import models
from uuid import uuid4
from django.utils import timezone

from app import utils
import secrets
import string
from .choices import needed_length, STATUS, STATUS_DEFAULT, PENDING, IN_PROGRESS, ABANDONED, COMPLETED
from django.contrib.auth.models import User

MAILJET_API_KEY = os.environ['MAILJET_API_KEY']
MAILJET_API_SECRET = os.environ['MAILJET_API_SECRET']
LINK_LIFETIME = timezone.timedelta(hours=1)

# **************************************************************************** #

class EmailVerification(models.Model):
	
	uid = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True)

	user = models.OneToOneField(User, null=True, blank=True, unique=True, on_delete=models.CASCADE)

	email = models.EmailField(null=True, validators=[utils.isEmailValid])

	verification_status = models.CharField(max_length=needed_length(STATUS), choices=STATUS, default=STATUS_DEFAULT)

	verification_link = models.SlugField(null=True, blank=True, unique=True)

	sended_at = models.DateTimeField(null=True, blank=True)

	# **************************************************************************** #

	def __str__(self):
		return f'{self.user.username if self.user else self.uid}'
	
	def clean(self):
		self.update_all()
		super().clean()

	# **************************************************************************** #

	def update_verification_status(self):
		if not self.sended_at:
			self.verification_status = STATUS_DEFAULT
		elif self.verification_status == PENDING:
			self.verification_status = IN_PROGRESS
		if self.verification_status == IN_PROGRESS:
			if timezone.now() >= self.sended_at + LINK_LIFETIME:
				self.verification_status = ABANDONED

	def update_all(self):
		self.update_verification_status()

	# **************************************************************************** #

	def get_verification_status(self):
		self.update_verification_status()
		return self.verification_status

	# **************************************************************************** #

	def is_valid(self):
		self.update_verification_status()
		print(self.verification_status)
		if self.verification_status == IN_PROGRESS:
			return True
		return False

	# **************************************************************************** #
	
	def send(self, resend=False):
		if self.verification_status != STATUS_DEFAULT or not self.user:
			return False
		if not self.verification_link or not resend:
			self.verification_link = utils.randomSlug(42)
		
		parameters = {
			'sender_name' : 'ft_transcendence',
			'sender_email' : 'ft_transcendence@titouanck.fr',
			
			'recipient_name' : self.user.username,
			'recipient_email' : self.email,
			
			'email_subject' : "Confirm your email.",
			'email_text' : "Confirmation email",

			'verification_link' : f'http://127.0.0.1:8000/api/confirm-email/{self.verification_link}/'
		}

		html_content = utils.readStaticFile('html/verification_email.html')
		if not html_content:
			return False
		html_content = utils.replaceVars(html_content, parameters)
		

		mailjet = mailjet_rest.Client(auth=(MAILJET_API_KEY, MAILJET_API_SECRET), version='v3.1')
		data = {
			'Messages': [
				{
					"From": {
						"Email": parameters['sender_email'],
						"Name": parameters['sender_name']
					},
					"To": [
						{
							"Email": parameters['recipient_email'],
							"Name": parameters['recipient_name']
						}
					],
					"Subject": parameters['email_subject'],
					"TextPart": parameters['email_text'],
					"HTMLPart": html_content
				}
			]
		}
		result = mailjet.send.create(data=data)
		if result and result.status_code == 200:
			self.sended_at = timezone.now()
			self.update_all()
			self.save()
			return True
		else:
			return False
