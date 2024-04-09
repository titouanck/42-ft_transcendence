from rest_framework import serializers
from django.contrib.auth.models import User
from app.models.Player import Player
from app.models.EmailVerification import EmailVerification
from django.db.models.query import QuerySet

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['username']

class PlayerSerializer(serializers.ModelSerializer):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		many = True if isinstance(self.instance, QuerySet) else False
		if self.scope() == 'public' or (
			self.requester() and (
				(not self.requester() or not self.requester().is_staff
	 		) 
			and (
				many == True or self.requester() != self.instance.user)
			)
		):
			self.fields.pop('email', None)
			self.fields.pop('email_to_confirm', None)

	username = serializers.SerializerMethodField()
	email = serializers.SerializerMethodField()
	email_to_confirm = serializers.SerializerMethodField()
		
	class Meta:
		model = Player
		fields = ['uid', 'username', 'email', 'email_to_confirm', 'player_rank', 'player_elo', 'total_victories', 'total_defeats', 'total_matches']
		staff_only_fields = ['email', 'player_elo', 'total_victories', 'total_defeats']
		read_only_fields = ['uid', 'player_rank', 'total_matches']

	def is_valid(self, raise_exception=False, is_staff=False):
		valid = super().is_valid(raise_exception=raise_exception)
		for key, value in self.initial_data.items():
			if key not in self.Meta.fields:
				if key not in self._errors:
					self._errors[key] = []
				self.errors[key].append('This field do not exist.')
			if key in self.Meta.read_only_fields:
				if key not in self._errors:
					self._errors[key] = []
				self.errors[key].append('This field cannot be updated.')
			elif key in self.Meta.staff_only_fields and not is_staff:
				if key not in self._errors:
					self._errors[key] = []
				self.errors[key].append('This field can only be modified by a staff member.')
		if self.errors or self._errors:
			return False
		return True

	def update(self, instance, validated_data):
		data = {}
		if 'username' in self.initial_data and instance.user:
			data['username'] = self.initial_data['username']

		user_serializer = UserSerializer(instance.user, partial=True, data=data)
		if user_serializer.is_valid():
			user_serializer.save()

		# if 'email_to_confirm' in self.initial_data and instance.user:
		# 	try:
		# 		email_verification = EmailVerification.objects.get(user=instance.user)
		# 		email_verification.change_email(self.initial_data['email'])
		# 	except EmailVerification.DoesNotExist:
		# 		email_verification = EmailVerification.objects.create(user=instance.user, email=self.initial_data['email'])
		# 		email_verification.send()

		
		return super().update(instance, validated_data)
	
	def get_username(self, obj):
		try:
			return obj.user.username
		except Exception as e:
			return None
		
	def get_email(self, obj):
		try:
			return obj.user.email
		except Exception as e:
			return None

	def get_email_to_confirm(self, obj):
		try:
			email_verification = EmailVerification.objects.get(user=obj.user)
			email_verification.update_all()
			return email_verification.email
		except Exception as e:
			return None
		
	def scope(self):
		if not hasattr(self, 'context') or self.context.get('scope') != 'private':
			return 'public'
		else:
			return self.context['scope']
		
	def requester(self):
		if not hasattr(self, 'context') or self.context.get('user', None) == None:
			return None
		else:
			return self.context['user']


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
	@classmethod
	def get_token(cls, user):
		token = super().get_token(user)
		token['username'] = user.username

		return token
